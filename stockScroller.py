
import requests
import time
from colorama import Fore
def getColor(value):
    if value < 0:
        return Fore.RED
    if value >= 0:
        return Fore.GREEN
def getColorWithGainLoss(value):
    if value < 0:
        return 'Loss Of' + Fore.RED
    if value >= 0:
        return 'Gain Of' + Fore.GREEN
from bs4 import BeautifulSoup
class stock:
    def __init__(self,pricePaid,ticker,coName,yahooUrl,numberOfShares):
        self.numberOfShares = numberOfShares
        self.pricePaid = pricePaid
        self.ticker = ticker
        self.coName = coName
        self.yahooUrl = yahooUrl
        Source = requests.get(self.yahooUrl).text
        Soup = BeautifulSoup(Source, 'lxml')
        openPriceHtml = Soup.find("div", id="quote-summary")
        rawOpenPrice = openPriceHtml.div.table.tbody.find("span", class_="Trsdu(0.3s)").text
        self.openPrice = float(rawOpenPrice.replace(',',''))

        currentPriceHtml = Soup.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")
        self.currentPrice = float(currentPriceHtml.text.replace(',',''))

        self.daysChange = self.currentPrice - self.openPrice
        if self.numberOfShares > 0:
            self.currentStockValue = self.currentPrice * self.numberOfShares

            self.daysChangeOnAccount = self.daysChange * self.numberOfShares
            self.moneyMadeOnStock = self.currentStockValue - self.pricePaid
            self.openPriceAccountValue = self.numberOfShares * self.openPrice
        self.daysChangePercent = (self.daysChange / self.openPrice) * 100




    def getStockPrice(self):
        #this attribute returns the stock price
        return self.currentPrice
    def getStockValue(self):
        #this attribute returns the stock price multiplied by the number of shares owned
        return self.currentStockValue
    def getDaysChange(self):
        return self.daysChange
    def getDaysChangeOnAccount(self):
        #this returns the ammount of money the stock has made us today
        return self.daysChangeOnAccount
    def getDaysChangePercent(self):
        return self.daysChangePercent
    def getMoneyMadeOnStock(self):
        return self.moneyMadeOnStock

    def getOpenPriceAccountValue(self):
        return self.openPriceAccountValue
    def getTicker(self):
        return self.ticker
    def getName(self):
        return self.coName
def printStocks(portfolioId,watchlist,delay):
    import sql
    userPortfolioTable = sql.getAllStockPortfolioData(portfolioId,watchlist)
    stockScrollerList = []
    for item in userPortfolioTable:
        currentStockValue = 0
        daysChangeOnAccount = 0
        moneyMadeOnStock = 0
        openPriceAccountValue = 0
        stockPriceBubbleSort = []
        stockNameBubbleSort = []
        stockTicker = item[1]
        pricePaid = float(item[2])
        numberOfShares = int(item[3])
        stockTable = sql.getStockData(stockTicker)
        coName = stockTable[1]
        yahooUrl = stockTable[2]
        Source = requests.get(yahooUrl).text
        Soup = BeautifulSoup(Source, 'lxml')
        openPriceHtml = Soup.find("div", id="quote-summary")
        rawOpenPrice = openPriceHtml.div.table.tbody.find("span", class_="Trsdu(0.3s)").text
        openPrice = float(rawOpenPrice.replace(',',''))

        currentPriceHtml = Soup.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")
        currentPrice = float(currentPriceHtml.text.replace(',',''))

        daysChange = currentPrice - openPrice
        if numberOfShares > 0:
            currentStockValue = currentPrice * numberOfShares

            daysChangeOnAccount = daysChange * numberOfShares
            moneyMadeOnStock = currentStockValue - pricePaid
            openPriceAccountValue = numberOfShares * openPrice
        daysChangePercent = (daysChange / openPrice) * 100

        stockPriceBubbleSort.append(currentPrice)
        stockNameBubbleSort.append(stockTicker)
        stockScrollerList.append([stockTicker,currentPrice,daysChangePercent,moneyMadeOnStock])
    for i in range(len(stockScrollerList)):
        for j in range(len(stockScrollerList) - 1):
            if stockScrollerList[j][2] < stockScrollerList[j + 1][2]:
                stockScrollerList[j], stockScrollerList[j + 1] = stockScrollerList[j + 1], stockScrollerList[j]
    for tist in stockScrollerList:
        print(Fore.LIGHTMAGENTA_EX + tist[0], Fore.LIGHTYELLOW_EX, "$",
              tist[1], Fore.LIGHTWHITE_EX, "Days Change: ",
              getColor(tist[2]),
              round(tist[2], 2), '%', Fore.LIGHTWHITE_EX, 'Total',
              getColorWithGainLoss(tist[3]), '$',
              round(tist[3], 2))
        time.sleep(delay)
def printStocksWithTotals(portfolioId):
    import sql
    userPortfolioTable = sql.getAllStockPortfolioData(portfolioId,'no')
    stockScrollerList = []
    totalAccountValue = 0
    for item in userPortfolioTable:
        currentStockValue = 0
        daysChangeOnAccount = 0
        moneyMadeOnStock = 0
        openPriceAccountValue = 0
        stockPriceBubbleSort = []
        stockNameBubbleSort = []
        stockTicker = item[1]
        pricePaid = float(item[2])
        numberOfShares = int(item[3])
        stockTable = sql.getStockData(stockTicker)
        coName = stockTable[1]
        yahooUrl = stockTable[2]
        Source = requests.get(yahooUrl).text
        Soup = BeautifulSoup(Source, 'lxml')
        openPriceHtml = Soup.find("div", id="quote-summary")
        rawOpenPrice = openPriceHtml.div.table.tbody.find("span", class_="Trsdu(0.3s)").text
        openPrice = float(rawOpenPrice.replace(',',''))

        currentPriceHtml = Soup.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")
        currentPrice = float(currentPriceHtml.text.replace(',',''))

        daysChange = currentPrice - openPrice
        totalAccountValue = totalAccountValue + numberOfShares * currentPrice
        print(totalAccountValue)
        if numberOfShares > 0:
            currentStockValue = currentPrice * numberOfShares

            daysChangeOnAccount = daysChange * numberOfShares
            moneyMadeOnStock = currentStockValue - pricePaid
            openPriceAccountValue = numberOfShares * openPrice
        daysChangePercent = (daysChange / openPrice) * 100

        stockPriceBubbleSort.append(currentPrice)
        stockNameBubbleSort.append(stockTicker)
        stockScrollerList.append([stockTicker,currentPrice,daysChangePercent,moneyMadeOnStock])
    for i in range(len(stockScrollerList)):
        for j in range(len(stockScrollerList) - 1):
            if stockScrollerList[j][2] < stockScrollerList[j + 1][2]:
                stockScrollerList[j], stockScrollerList[j + 1] = stockScrollerList[j + 1], stockScrollerList[j]
    for tist in stockScrollerList:
        print(Fore.LIGHTMAGENTA_EX + tist[0], Fore.LIGHTYELLOW_EX, "$",
              tist[1], Fore.LIGHTWHITE_EX, "Days Change: ",
              getColor(tist[2]),
              round(tist[2], 2), '%', Fore.LIGHTWHITE_EX, 'Total',
              getColorWithGainLoss(tist[3]), '$',
              round(tist[3], 2))
        time.sleep(1)
