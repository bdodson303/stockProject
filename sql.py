import sqlite3
conn = sqlite3.connect("stonks.db")
cursor = conn.cursor()
#cursor.execute("CREATE TABLE usersTable ('username','password','firstName','lastName')")
#cursor.execute("CREATE TABLE portfoliosUserTable ('username','portfolioName','portfolioId')")
#cursor.execute("CREATE TABLE portfolios ('portfolioName','portfolioId','firstName','lastName')")
#cursor.execute("CREATE TABLE stockPortfolioTable ('portfolioId','stockTicker','pricePaid','numberOfShares')")
#cursor.execute("CREATE TABLE stock ('ticker','coName','yahooUrl')")
#def createAccount(username,password,firstName,lastName)
#cursor.execute("INSERT INTO usersTable Values ('bdodson303@gmail.com','bld029914','Ben','Dodson')")
#rows = cursor.execute("SELECT * FROM usersTable WHERE lastName='Dodson'")
#print(rows.fetchall())
#cursor.execute("ALTER TABLE stockPortfolioTable ADD watchlist")
def mathYay():
    print('hello')
def createAccount(USERNAME, password, firstName, lastName):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        cursor.execute("INSERT INTO usersTable VALUES (:username,:password,:firstName,:lastName)", {'username': USERNAME, 'password': password, 'firstName': firstName, 'lastName': lastName})
    conn.commit()
    cursor.close()
def getPass(USERNAME):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        userinfo = cursor.execute("SELECT password FROM usersTable WHERE userName=:userName", {'userName': USERNAME}).fetchall()
        if len(userinfo) > 0:
            return userinfo[0]
    conn.commit()
    cursor.close()
def createPortfollio(USERNAME, portfolioName, portfolioId):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        cursor.execute("INSERT INTO portfoliosUserTable VALUES (:username,:portfolioName,:portfolioId)", {'username': USERNAME, 'portfolioName': portfolioName, 'portfolioId': portfolioId})
    conn.commit()
    cursor.close()
def getPortfolio(portfolioId):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        portfolioInfo = cursor.execute("SELECT * FROM portfoliosUserTable WHERE portfolioId=:portfolioId",{'portfolioId': portfolioId}).fetchone()
        return portfolioInfo
    conn.commit()
    cursor.close()
def getAllUserPortfolios(USERNAME):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        portfolioInfo = cursor.execute("SELECT portfolioName FROM portfoliosUserTable WHERE username=:username", {'username': USERNAME}).fetchall()
        return portfolioInfo
    conn.commit()
    cursor.close()
def getAllStockTickers():
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        stockTickers = cursor.execute("SELECT ticker FROM stock").fetchall()
        return stockTickers
    conn.commit()
    cursor.close()
def importStock(ticker,coName,yahooUrl):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        cursor.execute("INSERT INTO stock VALUES (:ticker,:coName,:yahooUrl)",{'ticker': ticker, 'coName': coName,'yahooUrl': yahooUrl})
    conn.commit()
    cursor.close()
def getStockTickersInPortfolio(portfolioId,watchlist):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        portfolioInfo = cursor.execute("SELECT stockTicker FROM stockPortfolioTable WHERE portfolioId=:portfolioId AND watchlist=:watchlist", {'portfolioId': portfolioId, 'watchlist':watchlist}).fetchall()
        return portfolioInfo
    conn.commit()
    cursor.close()
def importStockPortfolioInfo(portfolioId,stockTicker,pricePaid,numberOfShares,watchlist):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        cursor.execute("INSERT INTO stockPortfolioTable VALUES (:portfolioId,:stockTicker,:pricePaid,:numberOfShares,:watchlist)",{'portfolioId': portfolioId, 'stockTicker': stockTicker,'pricePaid': pricePaid,'numberOfShares': numberOfShares,'watchlist':watchlist})
    conn.commit()
    cursor.close()
def deleteRowFromStockPortfolioTable(ticker,portfolioId,watchlist):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        cursor.execute("DELETE FROM stockPortfolioTable WHERE stockTicker=:ticker AND portfolioId=:portfolioId AND watchlist=:watchlist",{'ticker':ticker,'portfolioId':portfolioId,'watchlist':watchlist})
    conn.commit()
    cursor.close()
def getAllStockPortfolioData(portfolioId,watchlist):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        portfolioInfo = cursor.execute("SELECT * FROM stockPortfolioTable WHERE portfolioId=:portfolioId AND watchlist=:watchlist", {'portfolioId': portfolioId, 'watchlist':watchlist}).fetchall()
        return portfolioInfo
    conn.commit()
    cursor.close()
def getStockData(ticker):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        stockInfo = cursor.execute("SELECT * FROM stock WHERE ticker=:ticker", {'ticker': ticker}).fetchone()
        return stockInfo
    conn.commit()
    cursor.close()
def deleteStockPortfolio(portfolioId):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        cursor.execute("DELETE FROM portfoliosUserTable WHERE portfolioId=:portfolioId",{'portfolioId':portfolioId})
        cursor.execute("DELETE FROM stockPortfolioTable WHERE portfolioId=:portfolioId",{'portfolioId':portfolioId})
    conn.commit()
    cursor.close()
def getUsersFirstName(username):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        usersFirstName = cursor.execute("SELECT firstName FROM usersTable WHERE username=:username", {'username': username}).fetchone()
        return usersFirstName
    conn.commit()
    cursor.close()
def getAllUsernames():
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        usernameList = cursor.execute("SELECT username FROM usersTable").fetchall()
        return usernameList
    conn.commit()
    cursor.close()
def getPricePaid(ticker, portfolioId):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        pricePaid = cursor.execute("SELECT pricePaid FROM stockPortfolioTable WHERE stockTicker=:ticker AND portfolioId=:portfolioId AND watchlist=:watchlist",{'ticker': ticker, 'portfolioId':portfolioId, 'watchlist':'no'}).fetchone()
        return pricePaid
    conn.commit()
    cursor.close()
def getNumberOfShares(ticker, portfolioId):
    conn = sqlite3.connect("stonks.db")
    cursor = conn.cursor()
    with conn:
        pricePaid = cursor.execute("SELECT numberOfShares FROM stockPortfolioTable WHERE stockTicker=:ticker AND portfolioId=:portfolioId AND watchlist=:watchlist",{'ticker': ticker, 'portfolioId': portfolioId, 'watchlist': 'no'}).fetchone()
        return pricePaid
    conn.commit()
    cursor.close()
