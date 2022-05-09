from tkinter import *
from tkinter import messagebox
from ttkthemes import themed_tk as tk
from tkinter import ttk
import sql
def createPortfolio(username):
    createPortfolioPage = Toplevel()
    createPortfolioPage.iconbitmap('BD(2).ico')

    Label(text="Create Portfolio").grid(column="1",row="0",sticky="w")
    Label(text="Portfolio Name:").grid(row="1",column="0")
    Label(text="Your Portfolios:",font="impact").grid(column="2",row='0')
    portfolioNameInput = Entry(createPortfolioPage)
    submitButton = Button(text="Create", command="submitButtonClick")
    submitButton.grid(row="2",column="1")
    portfolioNameInput.grid(row="1",column="1")
    portfolioCounter = 0
    #function that lists users portfolios
    for portfolio in sql.getAllUserPortfolios(username):
        if len(portfolio)>0:
            portfolioCounter = portfolioCounter + 1
            labelText=str(portfolioCounter) + '. ' + str(portfolio[0])
            Label(text=str(labelText)).grid(createPortfolioPage,row=str(portfolioCounter), column='2')
    createPortfolioPage.mainloop()
