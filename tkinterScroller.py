import requests
from tkinter import ttk

import ttkthemes
from bs4 import BeautifulSoup
import sql
import concurrent.futures
from tkinter import *
from tkinter import messagebox
from ttkthemes import themed_tk as tk
from tkinter import ttk
import yfinance as yf
import wolfImage
import time
from wolfImage import ImageLabel
import editPortfolioButtons
def stockPage(portfolio,username):
    progressBar = tk.ThemedTk()
    tkinterScroller = tk.ThemedTk()
    start = time.perf_counter()
    progressBar.config(background="black")

    tkinterScroller.config(background="black")
    stockTickerList = []
    portfolioId = username + "-" + portfolio
    refreshFlag=0
    def refreshButtonClick():
        tkinterScroller.destroy()
        stockPage(portfolio,username)
    def addStockButtonClick():
        editPortfolioButtons.addStockPage(portfolioId, stockTickerList)
        tkinterScroller.destroy()
    def deleteStockButtonClick():
        editPortfolioButtons.deleteStockPage(portfolioId,stockTickerList)
    def createGraphButtonClick():
        editPortfolioButtons.createGraphPage(portfolioId, stockTickerList)

    portfolioDataList= sql.getAllStockPortfolioData(portfolioId,'no')
    #want to grab all data here and then send it into the label printing loop
    #we also want to bubble sort it so our list is ordered from worst performing to best
    stockObjDict=[]
    indexObjDict=[]
    indexList=['^DJI','^IXIC']
    def grabOpenAndClose(ticker):
        stockInfo = yf.Ticker(ticker).info
        chngPercent = (stockInfo['regularMarketPrice']-stockInfo['previousClose'])/stockInfo['previousClose']
        print(ticker, chngPercent)
        return [stockInfo,ticker, chngPercent]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(grabOpenAndClose, stock[1]) for stock in portfolioDataList]
        results2 = [executor.submit(grabOpenAndClose, index) for index in indexList]

        for f in concurrent.futures.as_completed(results):
            stockObjDict.append(f.result())
        for f in concurrent.futures.as_completed(results2):
            indexObjDict.append(f.result())
    #now we will bubble sort the dictionaries
    n = len(stockObjDict)

    # Traverse through all array elements
    for i in range(n - 1):
        # range(n) also work but outer loop will repeat one time more than needed.

        # Last i elements are already in place
        for j in range(0, n - i - 1):

            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if stockObjDict[j][2] < stockObjDict[j + 1][2]:
                stockObjDict[j], stockObjDict[j + 1] = stockObjDict[j + 1], stockObjDict[j]
    counter = 1
    currentPortfolioValue = float(0)
    totalAccountValue = 0
    portfolioValueAtOpen = 0
    totalInitialPortfolioValue = 0
    #code for headings in stock Table
    stockName = ttk.Label(tkinterScroller, text="Ticker", relief=RAISED, font="Cambria")
    stockCurPrice = ttk.Label(tkinterScroller, text="Current Price", relief=RAISED, font="Cambria")
    stockDaysChange = ttk.Label(tkinterScroller, text="Days Change % and $", relief=RAISED, font="Cambria")
    stockTotalChangeLbl = ttk.Label(tkinterScroller, text="Stock Total $ Change on Account", relief=RAISED, font="Cambria")
    stockDaysChangeOnAccount = ttk.Label(tkinterScroller, text="Days $ Change on Portfolio", relief=RAISED,
                                         font="Cambria")
    stockName.grid(row=1, column=0, padx="5px")
    stockTotalChangeLbl.grid(row=1,column=4,columnspan=2)
    stockDaysChange.grid(row=1, column=2, padx="5px", columnspan=2)
    #stockDaysChangeOnAccount.grid(row=1, column=3, padx="5px")
    stockCurPrice.grid(row=1, column=1, padx="5px")

    #progress bar stuff
    lbl = ImageLabel(progressBar)
    lbl.grid(row=1, column=0)
    loadinglbl = Label(progressBar, text="Loading Portfolio Please Wait", font=("impact", 30), background="black", foreground="white")
    loadinglbl.grid(row=0, column=0)
    lbl.load('money.jpg')
    myProgress=ttk.Progressbar(progressBar, orient=HORIZONTAL, length=700, mode='determinate')
    myProgress.grid(row=2,column=0)
    progressBarStep = 100/(len(portfolioDataList)+2)
    for stockInfoDict in stockObjDict:
        myProgress['value'] += progressBarStep
        progressBar.update()

        Source = 0
        #grabs info we need from database and iterates through row stock by stock in the portfolio
        counter=counter+1
        stockTicker = stockInfoDict[1]
        stockTickerList.append(stockTicker)
        pricePaid = float(sql.getPricePaid(stockTicker, portfolioId)[0])
        numberOfShares = float(sql.getNumberOfShares(stockTicker, portfolioId)[0])
        print(stockTicker, numberOfShares, pricePaid)
        #requests info we need from yahoo
        openPrice = float(stockInfoDict[0]['previousClose'])
        currentPrice = float(stockInfoDict[0]['currentPrice'])
        # keeps track of portfolio value
        currentPortfolioValue = (currentPrice*float(numberOfShares))+currentPortfolioValue
        portfolioValueAtOpen = (openPrice*numberOfShares)+portfolioValueAtOpen


        #Calculations for stock table
        daysChange = currentPrice - openPrice
        daysChangePercent = round((daysChange/openPrice)*100,2)
        daysChangeOnAccount = float(daysChange) * float(numberOfShares)

        totalChangeOnAccount = (currentPrice*numberOfShares)-(pricePaid*numberOfShares)
        totalChangeOnAccountPercent = (totalChangeOnAccount/(pricePaid*numberOfShares))*100

        currPriceLabel = ttk.Label(tkinterScroller, text=currentPrice, font='sans-serif', foreground="white", background="black")
        currPriceLabel.grid(column=1, row=counter)

        # calculations for your account table
        totalAccountValue = (currentPrice*numberOfShares)+totalAccountValue
        totalInitialPortfolioValue = (pricePaid*numberOfShares)+totalInitialPortfolioValue
        #openPriceLabel = ttk.Label(tkinterScroller, text=openPrice)
        #openPriceLabel.grid(column=1, row=counter)

        stockTickerLabel = ttk.Label(tkinterScroller, text=stockTicker, foreground="#F300FF", background="black", font="georgia")
        stockTickerLabel.grid(column=0, row=counter)
        #code for diplaying total $ change on account
        if totalChangeOnAccount > 0:
            totalChangeOnAccountLbl = ttk.Label(tkinterScroller, text=str(round(totalChangeOnAccount, 2))+"$", font='sans-serif',background="black",foreground="green")
            totalChangeOnAccountPercentLbl = ttk.Label(tkinterScroller, text=str(round(totalChangeOnAccountPercent, 2))+"%", font='sans-serif',background="black",foreground="green")
        elif totalChangeOnAccount < 0:
            totalChangeOnAccountLbl = ttk.Label(tkinterScroller, text=str(round(totalChangeOnAccount, 2))+"$", font='sans-serif',background="black",foreground="red")
            totalChangeOnAccountPercentLbl = ttk.Label(tkinterScroller, text=str(round(totalChangeOnAccountPercent, 2))+"%", font='sans-serif',background="black",foreground="red")
        totalChangeOnAccountLbl.grid(row=counter, column=4)
        totalChangeOnAccountPercentLbl.grid(row=counter, column=5)
        # code for diplaying days change and days change on account the if statment makes it green if its greater than 0
        if daysChangePercent >= 0:
            dayChangeLabel = ttk.Label(tkinterScroller, text=str(daysChangePercent)+"%", font='sans-serif',background="black",foreground="green")
            dayChangeOnAccountLabel = ttk.Label(tkinterScroller, text="$"+str(round(daysChangeOnAccount, 2)), font='sans-serif',background="black",foreground="green")
        elif daysChangePercent < 0:
            dayChangeLabel = ttk.Label(tkinterScroller, text="$"+str(daysChangePercent)+"%", font='sans-serif',background="black",foreground="red")
            dayChangeOnAccountLabel = ttk.Label(tkinterScroller, text="$"+str(round(daysChangeOnAccount, 2)), font='sans-serif',background="black",foreground="red")


        dayChangeLabel.grid(column=2, row=counter)

        dayChangeOnAccountLabel.grid(column=3, row=counter)
    refreshButton = ttk.Button(tkinterScroller, text="Refresh", command=refreshButtonClick)
    refreshButton.grid(column=6, row=0)

    addStockButton = ttk.Button(tkinterScroller,text="Add Stock", command=addStockButtonClick)
    addStockButton.grid(column=6,row=1)

    deleteStockButton = ttk.Button(tkinterScroller,text="Delete Stock", command=deleteStockButtonClick)
    deleteStockButton.grid(column=6, row=2)

    createGraphButton = ttk.Button(tkinterScroller, text="Create Graph", command=createGraphButtonClick)
    createGraphButton.grid(column=6, row=3)

    #code for displaying the current portfolio
    portfolioLabelText = "Current Portfolio:  "+portfolio
    portfolioName = ttk.Label(tkinterScroller, text=portfolioLabelText, font="impact", background="black",foreground="white")
    portfolioName.grid(column="1", row="0", columnspan="2")
    # code for market indexes heading
    marketIndexsLabel = Label(tkinterScroller, text="Market Indexes", font="impact", background="black", foreground="white")
    marketIndexsLabel.grid(row=counter + 1, column=0, columnspan="2")

    #code for getting market indexs
    #indexTist will have lists in it with the index info
    #[ticker,yahooURL,Name]
    indexTist=[['^DJI','https://finance.yahoo.com/quote/%5EDJI?p=%5EDJI','Dow'],['^IXIC','https://finance.yahoo.com/quote/%5EIXIC?p=%5EIXIC','NASDAQ']]
    indexCounter = 0
    indexObjDict
    for index in indexObjDict:
        indexCounter = indexCounter + 1
        #indexTicker = index['symbol']
        indexName = index[1]
        #yfIndexObj = yf.Ticker(indexTicker)
        openPrice = index[0]['open']
        currentPrice = index[0]['regularMarketPrice']

        daysChange = currentPrice - openPrice
        daysChangePercent = round((daysChange/openPrice)*100,2)

        indexNameLabel = ttk.Label(tkinterScroller, text=indexName, background='black', foreground='#F300FF', font="georgia")
        indexNameLabel.grid(row=counter+indexCounter+2, column=0)

        if daysChange >= 0:
            indexDaysChangeLabel = ttk.Label(tkinterScroller, text=str(daysChangePercent)+'%', background="black", foreground="green",font='sans-serif')
        elif daysChange < 0:
            indexDaysChangeLabel = ttk.Label(tkinterScroller, text=str(daysChangePercent)+'%', background="black",foreground="red",font='sans-serif')
        indexDaysChangeLabel.grid(row=counter+indexCounter+2,column=1)
    #code for your account info
    if len(stockTickerList) > 0:
        totalAccountChange = currentPortfolioValue - totalInitialPortfolioValue
        totalAccountChangePercent = (totalAccountChange/totalInitialPortfolioValue)*100
        accountDaysChange = currentPortfolioValue - portfolioValueAtOpen
        accountDaysChangePercent = ((accountDaysChange / portfolioValueAtOpen)*100)
    else:
        totalAccountChange = 0
        totalAccountChangePercent = 0
        accountDaysChange = 0
        accountDaysChangePercent = 0

    marketIndexsLabel = Label(tkinterScroller, text="Your Portfolio:", font="impact", background="black",foreground="gold")
    marketIndexsLabel.grid(row=counter + 1, column=2, columnspan="2")
    portfolioDayChangePercentHeading = Label(tkinterScroller, text="Days Change %", relief=RAISED, font="Cambria", background="yellow")
    portfolioDayChangePercentHeading.grid(row=counter + 2, column=2,columnspan=2)
    portfolioDayChangeHeading = Label(tkinterScroller, text="Days Change $", relief=RAISED, font="Cambria",
                                      background="yellow")
    portfolioDayChangeHeading.grid(row=counter + 4, column=2,columnspan=2)
    portfolioTotalChangeLabel = Label(tkinterScroller, text="Total Account Change $", relief=RAISED, font="Cambria", background="yellow")
    portfolioTotalChangeLabel.grid(row=counter + 4, column=4, columnspan=2)

    portfolioTotalChangePercentLabel = Label(tkinterScroller, text="Total Account Change %", relief=RAISED, font="Cambria",
                                      background="yellow")
    portfolioTotalChangePercentLabel.grid(row=counter + 2, column=4, columnspan=2)

    if totalAccountChangePercent >=0:
        totalAccountChangePercentValue =Label(tkinterScroller, text=str(round(totalAccountChangePercent,2))+"%", background="black", foreground="green",font='sans-serif')
        totalAccountChangePercentValue.grid(row=counter + 3, column=4, columnspan=2)
    elif totalAccountChangePercent < 0:
        totalAccountChangePercentValue = Label(tkinterScroller, text=str(round(totalAccountChangePercent, 2)) + "%",
                                               background="black", foreground="red", font='sans-serif')
        totalAccountChangePercentValue.grid(row=counter + 3, column=4, columnspan=2)



    if totalAccountChange >=0:
        totalAccountChangeValue =Label(tkinterScroller, text=str(round(totalAccountChange,2))+"$", background="black", foreground="green",font='sans-serif')
        totalAccountChangeValue.grid(row=counter + 5, column=4, columnspan=2)
    elif totalAccountChange < 0:
        totalAccountChangeValue = Label(tkinterScroller, text=str(round(totalAccountChange, 2)) + "$",
                                        background="black", foreground="green", font='sans-serif')
        totalAccountChangeValue.grid(row=counter + 5, column=4, columnspan=2)
    if accountDaysChange >=0:
        portfolioDaysChange =Label(tkinterScroller, text=str(round(accountDaysChange,2))+"$", background="black", foreground="green",font='sans-serif')
        portfolioDaysChange.grid(row=counter + 5, column=2,columnspan=2)
    elif accountDaysChange < 0:
        portfolioDaysChange = Label(tkinterScroller, text=str(round(accountDaysChange, 2)) + "$", background="black",
                                    foreground="red", font='sans-serif')
        portfolioDaysChange.grid(row=counter + 5, column=2,columnspan=2)
    if accountDaysChangePercent >=0:
        portfolioDaysChangePercent=Label(tkinterScroller, text=str(round(accountDaysChangePercent,2))+"%", background="black", foreground="green",font='sans-serif')
        portfolioDaysChangePercent.grid(row=counter + 3, column=2,columnspan=2)
    elif accountDaysChangePercent <0:
        portfolioDaysChangePercent = Label(tkinterScroller, text=str(round(accountDaysChangePercent, 2)) + "%",
                                           background="black", foreground="red", font='sans-serif')
        portfolioDaysChangePercent.grid(row=counter + 3, column=2,columnspan=2)
    totalAccountValueHeading = Label(tkinterScroller, text="Total Portfolio Value", relief=RAISED, font="Cambria",background="yellow")
    totalAccountValueHeading.grid(row=counter + 4, column=6)
    totalAccountValueLabel = Label(tkinterScroller, text=str(round(totalAccountValue,2))+"$", background="black", foreground="gold",font='sans-serif')
    totalAccountValueLabel.grid(row=counter + 5, column=6)
    totalInitialInvestment = Label(tkinterScroller, text="Total Initial Investment", relief=RAISED, font="Cambria",background="yellow")
    totalInitialInvestment.grid(row=counter + 2, column=6)
    totalInitialInvestmentLabel = Label(tkinterScroller, text=str(round(totalInitialPortfolioValue,2))+"$", background="black", foreground="gold", font='sans-serif')
    totalInitialInvestmentLabel.grid(row=counter + 3, column=6)
    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} seconds')
    #code for Heading for the index table
    indexTickerLabel=Label(tkinterScroller, text="Name",relief=RAISED,font="Cambria")
    indexTickerLabel.grid(row=counter+2,column=0)
    indexDayChangeHeading = Label(tkinterScroller, text="Days Change %",relief=RAISED,font="Cambria")
    indexDayChangeHeading.grid(row=counter+2,column=1)


    #code for Headings for the stock table
    progressBar.destroy()
    progressBar.mainloop()
    tkinterScroller.mainloop()
stockPage('Ben', 'bld029914')