from tkinter import *
from tkinter import messagebox
from ttkthemes import themed_tk as tk
from tkinter import ttk

import TkinterCreatePortfolio
import sql
import tkinterScroller


def weirdListFormatFix(tist):
    betterTist = []
    for item in tist:
        betterTist.append(item[0])
    return betterTist

def portfolioMenu(username):
    from PIL import ImageTk, Image
    portfolioPage = tk.ThemedTk()
    portfolioPage.iconbitmap('BD(2).ico')
    portfolioPage.title('STONKS!!!!!')
    allUserPortfolios = weirdListFormatFix(sql.getAllUserPortfolios(username))
    def submitButtonClick(username):
        submitButtonReturn = radioButtonVar.get()
        if submitButtonReturn == 1:
            #Create Portfolio
            def createPortfolioSubmitButtonClick(username):
                #this is what happens when you click the create button in the portfolio page
                portfolio = portfolioNameInput.get()
                print(portfolio)

                if portfolio not in allUserPortfolios:
                    sql.createPortfollio(username)
            createPortfolioPage = Toplevel()
            createPortfolioPage.iconbitmap('BD(2).ico')

            ttk.Label(createPortfolioPage,text="Create Portfolio").grid(column="1", row="0", sticky="w")
            ttk.Label(createPortfolioPage,text="Portfolio Name:").grid(row="1", column="0")
            ttk.Label(createPortfolioPage,text="Your Portfolios:", font="impact").grid(column="2", row='0')
            portfolioNameInput = ttk.Entry(createPortfolioPage)
            submitButton = Button(createPortfolioPage,text="Create", command= lambda: createPortfolioSubmitButtonClick(username))
            submitButton.grid(row="2", column="1")
            portfolioNameInput.grid(row="1", column="1")
            portfolioCounter = 0
            # function that lists users portfolios
            for portfolio in sql.getAllUserPortfolios(username):
                if len(portfolio) > 0:
                    portfolioCounter = portfolioCounter + 1
                    labelText = str(portfolioCounter) + '. ' + str(portfolio[0])
                    Label(createPortfolioPage,text=str(labelText)).grid(row=str(portfolioCounter), column='2')

            createPortfolioPage.mainloop()

        elif submitButtonReturn == 2:
            #Open a current Portfolio
            def portfolioSelection():
                portfolioPage.destroy()
                tkinterScroller.stockPage(portfolioSelectionVar.get(), username)

            openPortfolioPage = Toplevel()
            openPortfolioPage.iconbitmap('BD(2).ico')
            ttk.Label(openPortfolioPage, text="Which portfolio would you like to open?").grid(row="0", column="1")
            portfolioCounter = 0
            portfolioSelectionVar = StringVar()
            for portfolio in sql.getAllUserPortfolios(username):
                if len(portfolio) > 0:
                    portfolioCounter = portfolioCounter + 1
                    portfolioName= str(portfolio[0])
                    labelText = str(portfolioCounter) + '. ' + str(portfolio[0])
                    ttk.Radiobutton(openPortfolioPage,text=str(labelText), value=portfolioName, variable=portfolioSelectionVar).grid(row=str(portfolioCounter+1), column='1')
            openPortfolioPageSelectButton = ttk.Button(openPortfolioPage, text="Select", command=portfolioSelection)
            openPortfolioPageSelectButton.grid(row=str(portfolioCounter + 2), column="1")
        elif submitButtonReturn == 3:
            #Delete a Portfolio
            deletePortfolioPage=Toplevel()
            deletePortfolioPage.iconbitmap('BD(2).ico')

            deletePortfolioPage.mainloop()
        elif submitButtonReturn == 4:
            #Exit to login screen
            print('hi')
    radioButtonVar = IntVar()

    ttk.Radiobutton(portfolioPage, text ="Create Portfolio", variable=radioButtonVar, value=1).grid(row="2",column="1")
    ttk.Radiobutton(portfolioPage, text ="Open a current Portfolio", variable=radioButtonVar, value=2).grid(row="3",column="1")
    ttk.Radiobutton(portfolioPage, text ="Delete a Portfolio", variable=radioButtonVar, value=3).grid(row="4",column="1")
    ttk.Radiobutton(portfolioPage, text ="Exit to login screen", variable=radioButtonVar, value=4).grid(row="5",column="1")
    ttk.Label(portfolioPage, text='Portfolio Menu', font="Trajan").grid(row="0",column="1")
    ttk.Label(portfolioPage, text='Your Portfolios', font="impact").grid(row="0",column="2")


    submitButton = ttk.Button(portfolioPage, text="GO----->",command= lambda: submitButtonClick(username))
    submitButton.grid(row="6", column="1")
    portfolioCounter = 0
    for portfolio in sql.getAllUserPortfolios(username):
        if len(portfolio)>0:
            portfolioCounter = portfolioCounter + 1
            labelText=str(portfolioCounter) + '. ' + str(portfolio[0])
            ttk.Label(portfolioPage,text=str(labelText)).grid(row=str(portfolioCounter + 1), column='2')
    portfolioPage.mainloop()