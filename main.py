import yfinance as yf
import math
from cmu_graphics import *
from Chart import *
from stockData import *
from Date import *

def onAppStart(app):
    app.testData2 = [50, 40, 35, 38, 45, 60, 50, 35, 30, 20]
    app.bottomLeftX = 150
    app.bottomLeftY = 150
    app.length = 100
    app.tickCount = 5
    app.tickSize = 5
    app.size1 = app.width*0.45
    app.Charts = []
    app.maxCash = 10000
    app.buyRSI = 30
    app.sellRSI = 45
    app.buyPlus = (app.width//4 + 10, app.height * 0.5 + 130)
    app.sellPlus = (3*app.width//4 + 10, app.height * 0.5 + 130)
    app.buyMinus = (app.width//4 + 30, app.height * 0.5 + 130)
    app.sellMinus = (3*app.width//4 + 30, app.height * 0.5 + 130)
    app.plus = (app.width*0.2 + 100, app.height*0.8)
    app.minus = (app.width*0.2 + 130, app.height*0.8)
    loadData(app, ['AAPL', 'META', 'NVDA'])
    #app.chart1 = Chart('Chart1', app.testData, 50, 50, int(app.size1), int(app.height * 0.90), app.tickCount, app.tickSize)
    #app.chart2 = Chart('Chart2', app.testData2, int(app.width*0.52), 50, int(app.width*0.96), int(app.height*0.9), app.tickCount, app.tickSize)
    app.buttonSize = 30
    app.buttons = [(app.width/2 + app.buttonSize*2.5, app.buttonSize), (app.width/2 + app.buttonSize*2.5, app.buttonSize), (app.width/2 + app.buttonSize*4.5, app.buttonSize)]
def redrawAll(app):
    #drawButtons(app)
    for i in app.Charts:
        i.draw()
    strategy(app)
def strategy(app):
    drawLabel('Current Strategy', app.width/2, app.height*0.5 + 50, size = 30, bold = True)
    drawLabel('Buy', app.width//4, app.height*0.5 + 100, size = 30, bold = True)
    drawLabel('Sell', 3*app.width//4, app.height*0.5 + 100, size = 30, bold = True)
    drawLabel(f'RSI: {app.buyRSI}', app.width//4 - 30, app.height * 0.5 + 130, size = 16)
    drawLabel(f'RSI: {app.sellRSI}', 3*app.width//4 - 30, app.height * 0.5 + 130, size = 16)
    drawLabel('+', app.width//4 + 10, app.height * 0.5 + 130, size = 16, bold = True, fill = 'green')
    drawLabel('-', app.width//4 + 30, app.height * 0.5 + 130, size = 16, bold = True, fill = 'red')
    drawLabel('+', 3*app.width//4 + 10, app.height * 0.5 + 130, size = 16, bold = True, fill = 'green')
    drawLabel('-', 3*app.width//4 + 30, app.height * 0.5 + 130, size = 16, bold = True, fill = 'red')
    drawLabel(f'Max cash: {app.maxCash}', app.width*0.2, app.height*0.8, size = 20)
    drawLabel('+', app.width*0.2 + 100, app.height*0.8, size = 20, bold = True, fill = 'green')
    drawLabel('-', app.width*0.2 + 130, app.height*0.8, size = 20, bold = True, fill = 'red')
def onMousePress(app, mouseX, mouseY):
    if inBounds(mouseX, mouseY, app.plus, 15):
        app.maxCash += 1000
        app.maxCash = min(1000000, app.maxCash)
        app.maxCash = max(1000, app.maxCash)
    if inBounds(mouseX, mouseY, app.minus, 15):
        app.maxCash -= 1000
        app.maxCash = min(1000000, app.maxCash)
        app.maxCash = max(1000, app.maxCash)
    if inBounds(mouseX, mouseY, app.buyPlus, 10):
        app.buyRSI += 1
        app.buyRSI = min(90, app.buyRSI)
        app.buyRSI = max(10, app.buyRSI)
    if inBounds(mouseX, mouseY, app.buyMinus, 10):
        app.buyRSI -= 1
        app.buyRSI = min(90, app.buyRSI)
        app.buyRSI = max(10, app.buyRSI)
    if inBounds(mouseX, mouseY, app.sellPlus, 10):
        app.sellRSI += 1
        app.sellRSI = min(90, app.sellRSI)
        app.sellRSI = max(10, app.sellRSI)
    if inBounds(mouseX, mouseY, app.sellMinus, 10):
        app.sellRSI -= 1
        app.sellRSI = min(90, app.sellRSI)
        app.sellRSI = max(10, app.sellRSI)
    
def inBounds(x, y, t1, border):
    x1 = t1[0] - border
    x2 = t1[0] + border
    y1 = t1[1] - border
    y2 = t1[1] + border
    return x1 <= x <= x2 and y1 <= y <= y2
def loadData(app, tickers):
    totalCharts = len(tickers) #at max 4
    app.coords = []
    for i in range(totalCharts):
        t = (int(30 + i * app.width/totalCharts), 50, int(app.width-(totalCharts-i-1)*app.width/totalCharts-25), int(app.height*0.5))
        app.coords.append(t)
    for j in range(len(tickers)):
        if j > 4:
            break
        curr = Data(tickers[j])
        d = []
        for i in curr: d.append(i[1])
        chart = Chart(tickers[j], d, app.coords[j][0], app.coords[j][1], app.coords[j][2], app.coords[j][3], app.tickCount, app.tickSize)
        app.Charts.append(chart)
def main():
    runApp(width = 800, height = 800)
main()