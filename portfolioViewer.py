import yfinance as yf
import math
from cmu_graphics import *
from stockData import *
from portfolio import *


def loadAppDataPortfolioViewer(app):
    app.p = Portfolio()
    app.currSelection = ''
    app.invalid = False
    app.num = 1
    app.price = None
    app.plus = (325, 650)
    app.minus = (350, 650)
    app.plusSell = (725, 650)
    app.minusSell = (750, 650)
    app.Cash = 10000
    app.selected = 0
    app.currSelectionSell = ''
    app.numSell = 1
    app.priceSell = None
    app.invalidSell = False
def drawPortfolioViewer(app):
    drawEmpty(app)
def drawEmpty(app):
    drawLabel('Cash: $' + "{:.2f}".format(app.Cash), 200, 75, size = 40, bold = True)
    if app.p.size() == 0:
        drawLabel('No items added!', 400, 400, size = 30, bold = True)
        drawLabel('Click the + below to add stocks!', 400, 450, size = 30, bold = True)
    else:
        drawLabel('Stock', 100, 150, size = 30, bold=  True)
        drawLabel('Price', 250, 150, size = 30, bold = True)
        drawLabel('Num Shares', 400, 150, size = 30, bold = True)
        drawLabel('Value', 550, 150, size = 30, bold = True)
        drawLabel('%', 700, 150, size = 30, bold = True)
        drawLine(50, 175, 750, 175)
        for i in range(len(app.p.getString())):
            val = app.p.getString()[i]
            for j in range(len(val)):
                currLength = getCurrLength(app.p.getString(), i)
                if j == 0:
                    drawLabel(str(i+1) + ".", 50, 200 + 25 * (currLength), size = 20)
                    drawLabel(val[0], 100, 200 + 25 * (currLength), size = 20)
                    drawLabel("{:.2f}".format(app.p.getStockPerc(val[0])), 700, 200 + 25 * (currLength), size = 20)
                else:
                    #PRICE:
                    drawLabel("{:.2f}".format(val[j][0]), 250, 200 + 25 * (currLength) + 25 * (j-1), size = 20)
                    #NUM SHARES:
                    drawLabel(val[j][1], 400, 200 + 25 * (currLength) + 25 * (j-1), size = 20)
                    drawLabel("${:.2f}".format(val[j][0] * val[j][1]), 550, 200 + 25 * (currLength) + 25 * (j-1), size = 20)
    drawLabel('BUY', 200, 550, bold = True, size = 40)
    drawBuy(app)
    drawLabel('SELL', 600, 550, bold = True, size = 40)
    drawSell(app)
def drawSell(app):
    drawLabel('Current Selection: ' + app.currSelectionSell, 600, 600, size = 16)
    if app.invalidSell:
        drawLabel('Invalid Ticker', 750, 600, fill = 'red')
    if app.priceSell != None:
        drawLabel('Price: ' + "{:.2f}".format(app.priceSell), 565, 625, size = 16)
        drawLabel('Number of Shares: ' + str(app.numSell), 605, 650, size = 16)
    else:
        drawLabel('Number of Shares: ---', 605, 650, size = 16)
        drawLabel('Price: ---', 565, 625, size = 16)
    drawLabel('+', 725, 650, size = 16, fill = 'green')
    drawLabel('-', 750, 650, size = 16, fill = 'red')
    if app.priceSell != None:
        drawLabel('Total: ' + "{:.2f}".format(app.priceSell * app.numSell), 560, 675, size = 16, fill = 'green' if worksWithCash(app, app.numSell, app.priceSell) else 'red')
    else:
        drawLabel('Total: ---', 560, 675, size = 16)
def drawBuy(app):
    drawLabel('Current Selection: ' + app.currSelection, 200, 600, size = 16)
    if app.invalid:
        drawLabel('Invalid Ticker', 400, 600, fill = 'red')
    if app.price != None:
        drawLabel('Price: ' +"{:.2f}".format(app.price), 165, 625, size = 16)
    else:
        drawLabel('Price: ---', 165, 625, size = 16)
    drawLabel('Number of Shares: ' + str(app.num), 205, 650, size = 16)
    drawLabel('+', 325, 650, size = 16, fill = 'green')
    drawLabel('-', 350, 650, size = 16, fill = 'red')
    if isinstance(app.price, float) or isinstance(app.price, int):
        drawLabel('Total: ' + "{:.2f}".format(app.price * app.num), 160, 675, size = 16, fill = 'green' if worksWithCash(app, app.num, app.price) else 'red')
    else:
        drawLabel('Total: ---', 160, 675, size = 16)
def mousePress(app, mouseX, mouseY):
    if inBoundsBuy(app, mouseX, mouseY):
        app.selected = 0
    if inBoundsSell(app, mouseX, mouseY):
        app.selected = 1
    if inBoundsPortfolioPlus(app, mouseX, mouseY):
        app.num += 1
    if inBoundsPortfolioMinus(app, mouseX, mouseY):
        app.num = max(1, app.num-1)
    if inBoundsPortfolioPlusSell(app, mouseX, mouseY):
        app.numSell += 1
    if inBoundsPortfolioMinusSell(app, mouseX, mouseY):
        app.numSell = max(1, app.numSell-1)
def worksWithCash(app, share, cost):
    return app.Cash - share*cost >= 0
def inBoundsBuy(app, x, y):
    return 0 <= x <= 400 and 500 <= y <= 800
def inBoundsSell(app, x, y):
    return 400 <= x <= 800 and 500 <= y <= 800
def inBoundsPortfolioSell(app, x, y):
    for i in range(len(app.p.getString())):
            val = app.p.getString()[i]
            for j in range(len(val)):
                currLength = getCurrLength(app.p.getString(), i)
                (x1,y1) = 750, 200 + 25 * (currLength) + 25 * (j-1)
                if inBounds(x, y, x1, y1, 15):
                    return (i,j)
    return None
    if app.plus[0] - 5 <= x <= app.plus[0] + 5 and app.plus[1] - 5 <= y <= app.plus[1] + 5:
        return True
    return False
def sell(app, i, j):
    stock = app.p.getString()[i][0]
    (price, shares) = app.p.getString()[i][j]
    if app.p.sell(stock, shares, price) != None:
        app.Cash += app.price * app.shares
def sellAmt(app):
    stock = app.currSelectionSell
    shares = app.numSell
    price = app.priceSell
    if isValidTicker(stock) and price != None and isinstance(shares, int) and shares > 0:
        amtSold = app.p.sellShares(stock, shares)
        app.Cash += amtSold * price
def inBounds(x, y, x1, y1, b):
    return x1-b <= x <= x1 + b and y1-b <= y <= y1 + b
def inBoundsPortfolioPlus(app, x, y):
    if app.plus[0] - 5 <= x <= app.plus[0] + 5 and app.plus[1] - 5 <= y <= app.plus[1] + 5:
        return True
    return False
def inBoundsPortfolioMinus(app, x, y):
    if app.minus[0] - 5 <= x <= app.minus[0] + 5 and app.minus[1] - 5 <= y <= app.minus[1] + 5:
        return True
    return False
def inBoundsPortfolioPlusSell(app, x, y):
    if app.plusSell[0] - 5 <= x <= app.plusSell[0] + 5 and app.plusSell[1] - 5 <= y <= app.plusSell[1] + 5:
        return True
    return False
def inBoundsPortfolioMinusSell(app, x, y):
    if app.minusSell[0] - 5 <= x <= app.minusSell[0] + 5 and app.minusSell[1] - 5 <= y <= app.minusSell[1] + 5:
        return True
    return False
def KeyPress(app, key):
    if key == 'backspace':
        if app.selected == 0:
            app.invalid = False
            if len(app.currSelection) > 0:
                app.currSelection = app.currSelection[:-1]
            if isValidTicker(app.currSelection):
                app.price = latestData(app.currSelection)
            if not isValidTicker(app.currSelection):
                app.price = None
        else:
            app.invalidSell = False
            if len(app.currSelectionSell) > 0:
                app.currSelectionSell = app.currSelectionSell[:-1]
            if isValidTicker(app.currSelectionSell):
                app.priceSell = latestData(app.currSelectionSell)
            if not isValidTicker(app.currSelectionSell):
                app.priceSell = None
    elif key == 'enter':
        if app.selected == 0:
            if isValidTicker(app.currSelection):
                add(app)
                app.currSelection = ''
                app.price = None
                app.num = 1
            else:
                app.invalid = True
        if app.selected == 1:
            if isValidTicker(app.currSelectionSell):
                sellAmt(app)
                app.currSelectionSell = ''
                app.priceSell = None
                app.numSell = 1
            else:
                app.invalidSell = True

    else:
        if app.selected == 0:
            app.invalid = False
            app.currSelection += key.upper()
            if isValidTicker(app.currSelection):
                app.price = latestData(app.currSelection)
            if not isValidTicker(app.currSelection):
                app.price = None
        else:
            app.invalidSell = False
            app.currSelectionSell += key.upper()
            if isValidTicker(app.currSelectionSell):
                app.priceSell = latestData(app.currSelectionSell)
            else:
                app.priceSell = None
def add(app):
    symbol = app.currSelection
    if worksWithCash(app, app.num, app.price):
        app.Cash -= app.num*app.price
        if isValidTicker(symbol):
            app.p.addStock(symbol, app.price, app.num)
def isValidTicker(symbol):
    array = ["AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "TSLA", "NVDA", "META", "BRK-B", "BRK-A", 
"V", "JNJ", "WMT", "PG", "XOM", "UNH", "JPM", "LLY", "MA", "HD", 
"PEP", "ABBV", "KO", "CVX", "MRK", "ORCL", "COST", "AVGO", "MCD", "TSM", 
"ADBE", "T", "PFE", "NFLX", "DIS", "BAC", "CSCO", "CRM", "WFC", "NKE", 
"TMO", "LIN", "AMD", "ABT", "SCHW", "TMUS", "PM", "RTX", "COP", "VZ", 
"QCOM", "DHR", "AMGN", "HON", "BMY", "UPS", "AXP", "TXN", "CAT", "GS", 
"DE", "MDT", "IBM", "AMT", "ELV", "INTU", "NEE", "SPGI", "C", "CHTR", 
"LMT", "BLK", "MMM", "GILD", "BKNG", "PLD", "LOW", "UNP", "ADP", "MO", 
"CL", "USB", "ZTS", "NOW", "MU", "F", "MRVL", "PANW", "TFC", "SO", 
"PAYX", "KHC", "SBUX", "REGN", "ISRG", "MAR", "EA", "KDP", "EBAY", "LRCX", 
"APD", "EOG", "FDX", "SNOW", "CMCSA", "ROST", "EXC", "OXY", "PGR", "HUM", 
"AIG", "LULU", "VFC", "STZ", "NKE", "WFC", "TGT", "LMT", "FIS", "AMT", 
"CVS", "SYY", "TROW", "BK", "HCA", "PYPL", "MCO", "T", "UPS", "PLD", 
"TSLA", "AIG", "RTX", "FISV", "PRU", "MS", "GS", "BKNG", "AON", "ZTS", 
"COF", "WMB", "DHR", "TJX", "XLNX", "CHTR", "TMO", "SYK", "FIS", "HLT", 
"SPGI", "COST", "TXN", "STT", "DD", "CTSH", "ANTM", "USB", "SBUX", "LULU", 
"VZ", "CSX", "VLO", "LHX", "AAPL", "CME", "NEM", "LLY", "APD", "OXY", 
"F", "MSCI", "NOC", "NAVI", "REGN", "GS", "NKE", "RMD", "T", "MNST", 
"JNJ", "WMT", "BRK-B", "TRV", "MSFT", "GS", "WFC", "KO", "V", "OXY", 
"ALL", "PEP", "COP", "MCD", "AMGN", "EXC", "WBA", "TMUS", "QCOM", "FTNT", 
"ROST", "MA", "BAX", "VLO", "MMM", "BMY", "NVAX", "OXY", "HCA", "VZ", 
"BA", "TFC", "HPQ", "SYY", "C", "MCO", "VRSN", "SBUX", "TROW", "DG", 
"NSC", "AXP", "TMO", "HUM", "RJF", "ADP", "PGR", "CL", "COST", "OXY", 
"FFIV", "MS", "AXP", "IQV", "AVGO", "MDT", "CSCO", "AMT", "MRK", "HCA", 
"AMGN", "FB", "MCD", "ORCL", "BIDU", "UNH", "GOOG", "AMZN", "COF", "JNJ", 
"LLY", "KHC", "SCHW", "COF", "RTX", "PYPL", "ANTM", "ETSY", "V", "GS", 
"CVS", "CLX", "PEP", "WMT", "UPS", "DUK", "UAL", "FB", "SYY", "WBA", 
"CI", "SPG", "KMI", "MMM", "EXC", "MCK", "MRO", "HPE", "TWTR", "AAPL", 
"FTNT", "AMZN", "FIS", "PFE", "INTU", "MRK", "CSCO", "CVX", "BA", "RTX", 
"QCOM", "REGN", "PYPL", "LOW", "PLD", "NEE", "AVGO", "ABT", "TXN", "LMT", 
"SNAP", "VZ", "NKE", "STT", "HUM", "AON", "BA", "TSLA", "PLD", "TMUS", 
"BMY", "TXN", "CVX", "T", "AIG", "WFC", "DIS", "AAPL", "CVS", "GE", 
"CX", "C", "VZ", "HCA", "TROW", "AON", "KO", "XOM", "PRU", "SPGI", 
"ADM", "LVS", "UNP", "BA", "FFIV", "KMB", "PG", "VZ", "DIS", "MCD", 
"MSFT", "MMM", "UNH", "NKE", "CI", "JNJ", "ABT", "BMY", "SYY", "LLY", "COIN", "GXO", "TOST", "XLK", "XLRE", "XLF"]
#chatGPT generated list of 1000 major stock companies
    return symbol in array
def getCurrLength(L, i):
    count = 0
    for j in range(len(L)):
        if j >= i:
            return count
        else:
            count += len(L[j])-1
    return count