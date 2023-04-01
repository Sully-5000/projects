# pass_gen

"""A password generation app"""

import random
import string
import pyperclip 
from tkinter import *
from tkinter import ttk

# window
root = Tk()
root.title("My Password Generator")
root.geometry("400x200") 
root.resizable(width=False, height=False)
frameType = ttk.Frame(root, padding=10)
root.eval('tk::PlaceWindow . center')

# clean up entry box

def clean():
	passbox.delete(0, END)

# ascii variables

uc = string.ascii_uppercase
lc = string.ascii_lowercase
num = string.digits
ch = string.punctuation
all = uc + lc + num + ch 

prompt_label = Label(root, text= "Click arrows to select number of characters.\n (Range available: 10-30)", font= ('Arial', 18))
prompt_label.pack()

selection = ttk.Spinbox(root, from_=10, to=30, state='readonly') 
selection.pack()

# generate password

def generate():
    clear_box = clean()
    choose_length = selection.get()
    password = "".join(random.sample(all, int(choose_length)))
    passbox.insert(0, password)

# copy password

def copy_b():
	random_password = passbox.get()
	pyperclip.copy(random_password)

# buttons and entry box variable
    
button = Button(root, text = "Generate", command = generate)
button.pack()

passbox = Entry(root, width=25)
passbox.pack()

copy_button = Button(root, text="Copy", command=copy_b)
copy_button.pack()

root.mainloop()


