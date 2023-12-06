#!/usr/bin/env python3

"""
This API counts the number of Azure Key Vaults in a specific subscription across all resource groups the sp has acces to in Azure Government cloud.
"""

from flask import Flask, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

AZURE_AUTHORITY_HOST = "https://login.microsoftonline.com"
AZURE_RESOURCE = "https://management.azure.com"

CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
TENANT_ID = os.getenv('AZURE_TENANT_ID')
SUBSCRIPTION_ID = os.getenv('AZURE_SUBSCRIPTION_ID')

def get_azure_token():
    url = f"{AZURE_AUTHORITY_HOST}/{TENANT_ID}/oauth2/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'resource': AZURE_RESOURCE
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['access_token']

@app.route("/liveness-check")
def liveness():
    return "OK", 200

@app.route("/readiness-check")
def readiness():
    return "OK", 200

@app.route("/startup-check")
def startup():
    return "OK", 200

@app.route('/count-keyvaults', methods=['GET'])
def count_keyvaults():
    try:
        token = get_azure_token()
        headers = {'Authorization': f'Bearer {token}'}

        resource_groups_url = f"{AZURE_RESOURCE}/subscriptions/{SUBSCRIPTION_ID}/resourcegroups?api-version=2019-09-01"
        rg_response = requests.get(resource_groups_url, headers=headers)
        rg_response.raise_for_status()
        resource_groups = rg_response.json()['value']

        rg_keyvault_count = []

        for rg in resource_groups:
            rg_name = rg['name']
            keyvaults_url = f"{AZURE_RESOURCE}/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{rg_name}/providers/Microsoft.KeyVault/vaults?api-version=2019-09-01"
            kv_response = requests.get(keyvaults_url, headers=headers)
            kv_response.raise_for_status()
            keyvaults = kv_response.json()['value']

            rg_keyvault_count.append({
                'resource_group_name': rg_name,
                'keyvault_count': len(keyvaults)
            })

        return jsonify(rg_keyvault_count)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
