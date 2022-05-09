from tkinter import *
from tkinter import messagebox
import sql
import stockMenu
def createAccount():
    from PIL import ImageTk, Image
    createAccountPage = Toplevel()
    createAccountPage.iconbitmap('BD(2).ico')
    createAccountPage.geometry('427x285')
    stonksImage = Image.open("STONKS.jpg")
    resized_image = stonksImage.resize((int(1280 / 3), int(853 / 3)))
    stonksImage = ImageTk.PhotoImage(resized_image)
    stonksImageWidget = Label(createAccountPage, image=(stonksImage))
    stonksImageWidget.place(x=0, y=0)
    creatingAccountInfoHeader = Label(createAccountPage,text='Creating Account Info', font=('Stencil Std',17))
    creatingAccountInfoHeader.grid(row='0',column='0')
    creatingAccountUsername = Label(createAccountPage,text='Username:')
    creatingAccountUsername.grid(row='1',column='0',sticky='w',pady='5')
    creatingAccountPassword = Label(createAccountPage,text='Password:')
    creatingAccountPassword.grid(row='2',column='0',sticky='w',pady='5')
    creatingAccountFirstName = Label(createAccountPage,text='First Name:')
    creatingAccountFirstName.grid(row='3',column='0',sticky='w',pady='5')
    creatingAccountLastName = Label(createAccountPage,text='Last Name:')
    creatingAccountLastName.grid(row='4',column='0',sticky='w',pady='5')
    username = Entry(createAccountPage)
    username.grid(row=1, column=0, sticky='e')
    password = Entry(createAccountPage)
    password.grid(row=2, column=0, sticky='e')
    firstName = Entry(createAccountPage)
    firstName.grid(row=3, column=0, sticky='e')
    lastName = Entry(createAccountPage)
    lastName.grid(row=4, column=0, sticky='e')
    def submitButtonClick():

        usernameList = sql.getAllUsernames()
        betterUsernameList = stockMenu.fixWeirdSQLFormatedList(usernameList)
        print(betterUsernameList)
        if username.get() not in betterUsernameList:
            sql.createAccount(str(username.get()), str(password.get()), str(firstName.get()), str(lastName.get()))
            messagebox.showinfo(title='Success', message='Account ' + username.get() + ' succesfully created')
            createAccountPage.destroy()
        else:
            messagebox.showerror(title='Error', message='Account ' + username.get() + ' already created')
    submitButton = Button(createAccountPage, text='Submit', command=submitButtonClick)
    submitButton.grid(row=5,column=0)

    createAccountPage.mainloop()
