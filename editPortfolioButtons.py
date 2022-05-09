import sql
from tkinter import *
from tkinter import messagebox
from ttkthemes import themed_tk as tk
from tkinter import ttk
from tkinter import messagebox
import mplfinance as mpf
import yfinance as yf
def tickerCheck(ticker):
    test = yf.Ticker(ticker)
    print(test.info['regularMarketPrice'])
    if test.info['regularMarketPrice'] == None:
        return 0
    else:
        return 1
def addStockPage(portfolioId,stockTickerList):
    try:
        addStockPageTK = tk.ThemedTk()
        def addStockButtonClick():
            #sql.importStockPortfolioInfo()
            pricePaidInput = float(pricePaidObj.get())
            stockTickerInput = stockTickerObj.get()
            numberOfSharesInput = int(numberOfSharesObj.get())
            if tickerCheck(stockTickerObj.get()) == 1:
                if stockTickerInput not in stockTickerList:
                    sql.importStockPortfolioInfo(portfolioId,stockTickerInput,pricePaidInput,numberOfSharesInput,'no')
                    messagebox.showinfo('Success','Stock '+str(stockTickerInput)+' successfully imported')
                    addStockPageTK.destroy()
                else:
                    messagebox.showerror('Error','Stock '+str(stockTickerInput)+' already in portfolio' )
            else:
                messagebox.showerror("Ticker Error","Ticker regMarketPrice Returned None please re-enter")

        stockTickerLabel = ttk.Label(addStockPageTK,text='stock ticker:')
        stockTickerLabel.grid(row=1,column=0)
        pricePaidLabel = ttk.Label(addStockPageTK, text='Price you paid for stock:')
        pricePaidLabel.grid(row=2,column=0)
        numberOfSharesLabel=ttk.Label(addStockPageTK, text='Number of Shares You Own:')
        numberOfSharesLabel.grid(row=3,column=0)
        stockTickerObj = StringVar()
        pricePaidObj = StringVar()
        numberOfSharesObj = StringVar()

        stockTickerEntry = ttk.Entry(addStockPageTK,textvariable=stockTickerObj)
        pricePaidEntry= ttk.Entry(addStockPageTK,textvariable=pricePaidObj)
        numberOfSharesEntry = ttk.Entry(addStockPageTK,textvariable=numberOfSharesObj)
        addStockButton=Button(addStockPageTK,text='Add',command=addStockButtonClick)
        addStockButton.grid(row=4,column=1)
        pricePaidEntry.grid(row=2,column=1)
        stockTickerEntry.grid(row=1,column=1)
        numberOfSharesEntry.grid(row=3,column=1)
        addStockPageTK.mainloop()
    except:
        messagebox.showerror(ERROR,'error with entry please retry')
def deleteStockPage(portfolioId,stockTickerList):
    deleteStockPage = tk.ThemedTk()
    def deleteStockSubmitClick():
        deleteStockInput = deleteStockInputObj.get()
        if deleteStockInput in stockTickerList:
            sql.deleteRowFromStockPortfolioTable(deleteStockInputObj.get(),portfolioId,'no')
            messagebox.showinfo('success ','Stock '+deleteStockInput+' deleted')
            deleteStockPage.destroy()
        else:
            messagebox.showerror('ERROR','Ticker '+deleteStockInput+' not in portfolio')
    deleteStockLabel=Label(deleteStockPage,text='Please input Stock To Be Deleted:')
    deleteStockLabel.grid(row=1,column=0)
    deleteStockInputObj = StringVar()
    deleteStockInput = Entry(deleteStockPage,textvariable=deleteStockInputObj)
    deleteStockInput.grid(row=1,column=1)
    deleteStockSubmitButton = Button(deleteStockPage,command= deleteStockSubmitClick,text='Delete')
    deleteStockSubmitButton.grid(row=2,column=1)
    deleteStockPage.mainloop()
def createGraphPage(portfolioId,stockTickerList):
    createGraphPage = tk.ThemedTk()
    dropDownStrVar = StringVar()
    dayOYearLengthInputVar = StringVar()
    dayOYearIntervalInputVar = StringVar()
    intervalInputVar = StringVar()
    stylesInputVar = StringVar()
    periodInputVar = StringVar()
    stylesList=["classic","charles","mike","blueskies","starsandstripes","brasil","yahoo"]
    def submitButtonClick():
        timeInputDictionary={"Days":"d","Years":"y","Months":"m","Hours":"h","Weeks":"wk"}
        supportedIntervals=["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
        kwargs = dict(type='candle', mav=(2, 4, 6), volume=True, figratio=(11, 8), figscale=0.85)
        period=periodInputVar.get()
        periodDayOrYear=dayOYearLengthInputVar.get()
        interval=intervalInputVar.get()
        #interval=2d is not supported. Valid intervals:
        intervalDayOrYear=dayOYearIntervalInputVar.get()
        periodCombinedInput = period + timeInputDictionary[periodDayOrYear]
        print(periodCombinedInput)
        time = "100" + "d"
        try:
            int(period)
        except:
            messagebox.showerror("ERROR","please only enter integers")
        yfTicker = yf.Ticker(dropDown.get())
        yfTickerHist = yfTicker.history(period=periodCombinedInput, interval=interval)
        print(periodCombinedInput,interval)

        mpf.plot(yfTickerHist, **kwargs, style=stylesInputVar.get())

    #['MNST', 'MUX', 'SAN', 'INTC', 'TSM', 'F', 'AMD', 'CRSR']

    dropDownStrVar.set(stockTickerList[0])
    dropDown = ttk.Combobox(createGraphPage, value=stockTickerList)
    submitButton = ttk.Button(createGraphPage, text="Submit", command=submitButtonClick)
    header = ttk.Label(createGraphPage,text="Please input info for graph",font="sans-serif")
    tickerLabel = ttk.Label(createGraphPage,text="Ticker")
    lengthLabel = ttk.Label(createGraphPage,text="Period(int)")
    intervalLabel = ttk.Label(createGraphPage, text="Interval")
    styleLabel = ttk.Label(createGraphPage, text="Styles")
    periodInput=ttk.Entry(createGraphPage, width=6, textvariable=periodInputVar)
    dayOrYearLengthInput=ttk.OptionMenu(createGraphPage,dayOYearLengthInputVar,"Years",*["Days","Years"])
    intervalInput = ttk.OptionMenu(createGraphPage, intervalInputVar,"1d",*["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"])
    stylesInput = ttk.OptionMenu(createGraphPage, stylesInputVar,"mike",*stylesList)


    dropDown.current(0)
    intervalLabel.grid(row=4, column=1, sticky="w",padx="2px")
    dropDown.grid(row=2,column=2, columnspan=2)
    tickerLabel.grid(row=2, column=1, sticky="w",padx="2px")
    lengthLabel.grid(row=3, column=1, sticky="w",padx="2px")
    submitButton.grid(row=6, column=2,columnspan=2)
    intervalInput.grid(row=4, column=2, columnspan=2)
    stylesInput.grid(row=5, column=2, columnspan=2)
    styleLabel.grid(row=5, column=1, sticky="w",padx="2px")
    header.grid(row=0,column=1,rowspan=2, columnspan=3, padx="10px")
    periodInput.grid(row=3, column=2)
    dayOrYearLengthInput.grid(row=3, column=3)


    createGraphPage.mainloop()
