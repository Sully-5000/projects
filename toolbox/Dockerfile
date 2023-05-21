# For creating an image from a local helm chart
# Use a base image compatible with Helm and your desired Linux distribution
FROM alpine:latest

# Set the working directory
WORKDIR /helm-charts

# Define a build argument for the path to the charts
ARG CHARTS_PATH

# Copy the local Helm charts into the image. Use docker build -t <image-name>:<tag> --build-arg CHARTS_PATH=<chart-path> <path-to-build-context>
COPY ${CHARTS_PATH}/* /helm-charts


