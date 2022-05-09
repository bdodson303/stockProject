import sql
import stockScroller


def getTickerList():
    tickerList = sql.getAllStockTickers()
    betterTickerList = []
    for ticker in tickerList:
        betterTickerList.append(ticker[0])
    return betterTickerList
def getStocksInPortfolioFormatedList(portfolioId,watchlist):
    portfolioTickerList = sql.getStockTickersInPortfolio(portfolioId,watchlist)
    betterTickerList=[]
    if len(portfolioTickerList) > 0:
        for tist in portfolioTickerList:
            betterTickerList.append(tist[0])
        return betterTickerList




def fixWeirdSQLFormatedList(weirdList):
    formatedList = []
    for item in weirdList:
        formatedList.append(item[0])
    return formatedList


def checkYahooUrl(yahooUrl):
    import requests
    from bs4 import BeautifulSoup
    try:
        Source = requests.get(yahooUrl).text
        Soup = BeautifulSoup(Source, 'lxml')
        openPriceHtml = Soup.find("div", id="quote-summary")
        rawOpenPrice = openPriceHtml.div.table.tbody.find("span", class_="Trsdu(0.3s)").text
        openPrice = float(rawOpenPrice.replace(',', ''))
        currentPriceHtml = Soup.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")
        currentPrice = float(currentPriceHtml.text.replace(',', ''))
        return 1
    except:
        return 0
def stockMenu(portfolioId,portfolioName):
    stockMenuLoopExitFlag = 0
    from colorama import Fore
    while stockMenuLoopExitFlag == 0:
        stockImportExitFlag = 0
        yahooChecker = 0
        tickerList = getTickerList()
        print('Main Portfolio')
        stockScroller.printStocks(portfolioId,'no',.25)
        print('Watchlist')
        print(Fore.YELLOW + 'Stock Menu Options')
        print(Fore.MAGENTA + '1: Import Stock Into Portfolio')
        print('2: Import Stock Into Portfolio Watchlist')
        print('3: Delete stock from Portfolio')
        print('4: Delete stock from Portfolio Watchlist')
        print('5: Display Portfolio')
        print('5: Exit Program')
        print('Current Portfolio:', portfolioName)
        menuOption = input()
        if menuOption == '1':
            while stockImportExitFlag == 0:
                watchlist = 'no'
                print('Please input the following data to Import Stock into portfolio:')
                print('ticker symbol')
                ticker = input()
                portfolioStockList = [getStocksInPortfolioFormatedList(portfolioId,watchlist)]
                if ticker not in tickerList and ticker not in portfolioStockList:
                    print('yahoo finance URL')
                    yahooUrl = input()
                    yahooChecker = checkYahooUrl(yahooUrl)
                    if yahooChecker == 1:
                        print('price paid for stock')
                        pricePaid = input()

                        print('company name:')
                        coName = input()
                        print('please enter the number of shares of ', coName, ' you own:')
                        numberOfShares = input()
                        sql.importStock(ticker, coName, yahooUrl)
                        sql.importStockPortfolioInfo(portfolioId, ticker, pricePaid, numberOfShares, watchlist)




                    else:
                        print("error with yahoo url you can 1: re-enter data 2: exit")
                        errorMenuOption = input()
                        if errorMenuOption == '2':
                            stockImportExitFlag = 1
                elif ticker in portfolioStockList:
                    print('this stock is already in portfolio:', portfolioName)
                elif ticker in tickerList:
                    print('please enter the price you paid for',ticker)
                    pricePaid = input()
                    print('please enter the number Of Shares you own')
                    numberOfShares = input()
                    sql.importStockPortfolioInfo(portfolioId, ticker, pricePaid, numberOfShares, watchlist)
                    print('Import Succesful')
                if stockImportExitFlag != 1:
                    stockScroller.printStocks(portfolioId,watchlist,.1)
                    print('Would you like to import another stock?')
                    print('1:yes')
                    print('2:no')
                    if input() == '2':
                        stockImportExitFlag = 1
        elif menuOption == '2':
            while stockImportExitFlag == 0:
                watchlist = 'yes'
                print('Please input the following data to Import Stock into portfolio watchlist:')
                print('ticker symbol')
                ticker = input()
                portfolioStockList = getStocksInPortfolioFormatedList(portfolioId,watchlist)
                if ticker not in tickerList and ticker not in portfolioStockList:
                    print('yahoo finance URL')
                    yahooUrl = input()
                    yahooChecker = checkYahooUrl(yahooUrl)
                    if yahooChecker == 1:
                        pricePaid = 0
                        print('company name:')
                        coName = input()
                        numberOfShares = 0
                        sql.importStock(ticker, coName, yahooUrl)
                        sql.importStockPortfolioInfo(portfolioId, ticker, pricePaid, numberOfShares, watchlist)
                        print(coName,' imported into Portfolio Watchlist')




                    else:
                        print("error with yahoo url you can 1: re-enter data 2: exit")
                        errorMenuOption = input()
                        if errorMenuOption == '2':
                            stockImportExitFlag = 1
                elif ticker in portfolioStockList:
                    print('this stock is already in portfolio:', portfolioName,' watchlist')
                elif ticker in tickerList:
                    pricePaid = 0
                    numberOfShares = 0
                    sql.importStockPortfolioInfo(portfolioId, ticker, pricePaid, numberOfShares, watchlist)
                    print('Stock ',ticker,' imported into portfolio watchlist')
                if stockImportExitFlag != 1:
                    print('Would you like to import another stock?')
                    print('1:yes')
                    print('2:no')
                    if input() == '2':
                        stockImportExitFlag = 1
        elif menuOption == '3':
            deleteStockTickerLoopExitFlag = 0
            watchlist = 'no'
            while deleteStockTickerLoopExitFlag == 0:
                stockTickerToBeDeleted = input('please input the ticker of the stock that will be deleted from this portfolio')
                portfolioStockList = [getStocksInPortfolioFormatedList(portfolioId, watchlist)]
                if stockTickerToBeDeleted in portfolioStockList:
                    print('are you sure you want to delete ',stockTickerToBeDeleted,' 1:yes 2:no')
                    if input() == '1':
                        sql.deleteRowFromStockPortfolioTable(stockTickerToBeDeleted,portfolioId,watchlist)
                        print(stockTickerToBeDeleted,' DELETED')
                        print('Would You Like To Delete Another? 1:yes 2:no')
                        deleteStockTickerMenuOption = input()
                        if deleteStockTickerMenuOption == '2':
                            deleteStockTickerLoopExitFlag = 1
                            stockScroller.printStocks(portfolioId, watchlist, .1)
                else:
                    print('Stock Not in your portfolio')
        elif menuOption == '4':
            deleteStockTickerLoopExitFlag = 0
            while deleteStockTickerLoopExitFlag == 0:
                watchlist = 'yes'
                stockTickerToBeDeleted = input('please input the ticker of the stock that will be deleted from this portfolios watchlist')
                portfolioStockList = [getStocksInPortfolioFormatedList(portfolioId, watchlist)]
                if stockTickerToBeDeleted in portfolioStockList:
                    print('are you sure you want to delete ', stockTickerToBeDeleted, ' 1:yes 2:no')
                    if input() == '1':
                        sql.deleteRowFromStockPortfolioTable(stockTickerToBeDeleted, portfolioId,watchlist)
                        print(stockTickerToBeDeleted, ' DELETED')
                        print('Would You Like To Delete Another? 1:yes 2:no')
                        deleteStockTickerMenuOption = input()
                        if deleteStockTickerMenuOption == '2':
                            deleteStockTickerLoopExitFlag = 1
                            stockScroller.printStocks(portfolioId, watchlist, .1)
                else:
                    print('Stock is not in your portfolio watchlist')
        elif menuOption == '5':
            stockMenuLoopExitFlag = 1










