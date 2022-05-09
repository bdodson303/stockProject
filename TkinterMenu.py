from tkinter import *
from tkinter import messagebox

from PIL import ImageTk, Image
import Userlogin
import TkinterCreateAccountPage
import tkinterPortfolioMenu
from ttkthemes import themed_tk as tk
from tkinter import ttk

scale = 3

root = tk.ThemedTk()
root.get_themes()
root.set_theme('breeze')

root.iconbitmap('BD(2).ico')
root.geometry('427x285')
root.title('STONKS!!!!!')
stonksImage = Image.open("STONKS.jpg")
resized_image = stonksImage.resize((int(1280 / scale), int(853 / scale)))


def submitButtonClick():
    userl = username.get()
    passs = password.get()
    loginAttempt = Userlogin.userLogin(userl, passs)
    if loginAttempt == 0:

        messagebox.showerror('Error', 'Invalid Username please Re-Enter')
    elif loginAttempt == 1:
        root.destroy()
        tkinterPortfolioMenu.portfolioMenu(userl)

    elif loginAttempt == 2:
        messagebox.showerror('Error', 'Invalid Password Please Re-enter')


def createAccountButtonClick():
    TkinterCreateAccountPage.createAccount()


stonksImage = ImageTk.PhotoImage(resized_image)
stonksImageWidget = ttk.Label(root, image=(stonksImage))
Header = ttk.Label(root, text='STONKS!!!', font=('Arial', '30', 'bold'))
Header.grid(row='1', column='1')
ttk.Label(root, text='Username:', relief='groove').grid(row='2', column='0')
username = ttk.Entry(root, width=20)
username.grid(row='2', column='1', padx=20, pady=10)
loginPasswordLabel = ttk.Label(text='Password:', relief='groove')
loginPasswordLabel.grid(row='3', column='0')
password = ttk.Entry(root, width=20)
password.grid(row='3', column='1', padx=20, pady=10)
submitButton = ttk.Button(root, text='Submit', command=submitButtonClick)
submitButton.grid(row='5', column='1', pady=10)
createAccountButton = ttk.Button(root, text='Create Account', command=createAccountButtonClick)
createAccountButton.grid(row='4', column='1')
stonksImageWidget.place(x=0, y=0)
root.mainloop()
