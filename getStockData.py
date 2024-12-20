import yfinance as yf
import math
from cmu_graphics import *
from Chart import *
from stockData import *
from portfolio import *
import datetime
from datetime import datetime

def loadChartValues(app):
    app.bottomLeftX = 150
    app.bottomLeftY = 150
    app.length = 100
    app.firstView = 0
    app.tickCount = 5
    app.tickSize = 5
    app.size1 = app.width*0.45
    app.Charts = []
    app.currTime = '1mo'
    app.currentButton = (200, 70)
    app.maxButton = (300, 70)
    app.minButton = (400, 70)
    loadTickerData(app)
    app.buttonSize = 30
    app.numChartPoints = 104
    app.buttons = [(app.width/2 + app.buttonSize*2.5, app.buttonSize), (app.width/2 + app.buttonSize*2.5, app.buttonSize), (app.width/2 + app.buttonSize*4.5, app.buttonSize)]
    app.bold = [False, False, True, False, False]
def drawChartView(app):
    drawButtons(app)
    for i in range(min(4,len(app.Charts))):
        app.Charts[i].draw()
def keyPressCharts(app, key):
    if key == 'right':
        app.firstView += 4
        if len(app.p.getTickers())%4 == 0:
            app.firstView =min(app.firstView, len(app.p.getTickers())-4)
        else:
            app.firstView = min(app.firstView, len(app.p.getTickers())-len(app.p.getTickers())%4)
        loadTickerData(app)
    if key == 'left':
        app.firstView -= 4
        app.firstView = max(0, app.firstView)
        loadTickerData(app)
def drawButtons(app):
    center = app.width/2
    drawLabel('Timeframe:', 325, 30, size = 25)
    drawLabel('1d', 425, 30, size = 25, bold = app.bold[0])
    drawLabel('5d', 475, 30, size = 25, bold = app.bold[1])
    drawLabel('1mo', 525, 30, size = 25, bold = app.bold[2])
    drawLabel('1y', 575, 30, size = 25, bold = app.bold[3])
    drawLabel('5y', 625, 30, size = 25, bold = app.bold[4])
    drawLabel('Current', app.currentButton[0], app.currentButton[1], size = 20, bold = app.showEnd)
    drawLabel('Max', app.maxButton[0], app.maxButton[1], size = 25, bold = app.showMin)
    drawLabel('Min', app.minButton[0], app.minButton[1], size = 25, bold = app.showMax)
    if 1 < len(app.p.getTickers()) <= 4:
        drawLabel(f'Page: {int(app.firstView/4) + 1} of 1', 400, 780, size = 16, bold = True)
    if len(app.p.getTickers()) > 4:
        drawLabel(f'Page: {int(app.firstView/4) + 1} of {math.floor(len(app.p.getTickers())/4) + 1}', 400, 780, size = 16, bold = True)
def mousePressCharts(app, x, y):
    if 400 <= x <= 450 and 0 <= y <= 60:
        app.currTime = '1d'
        loadTickerData(app)
    if 450 <= x <= 500 and 0 <= y <= 60:
        app.currTime = '5d'
        loadTickerData(app)
    if 500 <= x <= 550 and 0 <= y <= 60:
        app.currTime = '1mo'
        loadTickerData(app)
    if 550 <= x <= 600 and 0 <= y <= 60:
        app.currTime = '1y'
        loadTickerData(app)
    if 600 <= x <= 650 and 0 <= y <= 60:
        app.currTime = '5y'
        loadTickerData(app)
    if app.currentButton[0]-50 <= x <= app.currentButton[0]+50 and 60 <= y <= 80:
        app.showEnd = not app.showEnd
        for i in app.Charts:
            i.endLine = app.showEnd
    if app.maxButton[0]-50 <= x <= app.maxButton[0] + 50 and 60 <= y <= 80:
        app.showMin = not app.showMin
        for i in app.Charts:
            i.minLine = app.showMin
    if app.minButton[0]-50 <= x <= app.minButton[0] + 50 and 60 <= y <= 80:
        app.showMax = not app.showMax
        for i in app.Charts:
            i.maxLine = app.showMax
def loadCoords(num):
    if num == 1:
        return [(50, 100, 700, 735)]
    if num == 2:
        return [(50, 275, 375, 625), (450, 275, 775, 625)]
    if num == 3:
        return [(50, 100, 375, 400), (450, 100, 775, 400), (238, 450, 562, 735)]
    if num == 4:
        return [(50, 95, 375, 375), (450, 95, 775, 375), (50, 450, 375, 735), (450, 450, 775, 735)]
def loadTickerData(app):
    app.Charts = []
    tickers = app.p.getTickers()
    start = app.firstView
    coords = loadCoords(min(4, len(tickers)))
    for i in range(start, min(start+4,len(tickers))):
        today = datetime.today()
        end = Date(today.month, today.day, today.year)
        freq = '1h'
        if app.currTime == '1d':
            app.bold = [False, False, False, False, False]
            app.bold[0] = True
            app.numChartPoints = 50
            freq = '1m'
        if app.currTime == '5d':
            app.bold = [False, False, False, False, False]
            app.bold[1] = True
            freq = '2m'
        if app.currTime == '1mo':
            app.bold = [False, False, False, False, False]
            app.bold[2] = True
            freq = '5m'
        if app.currTime == '1y':
            app.bold = [False, False, False, False, False]
            app.bold[3] = True
            freq = '1h'
        if app.currTime == '5y':
            app.bold = [False, False, False, False, False]
            app.bold[4] = True
            freq = '1d'
        data = getDataHistory(tickers[i], app.currTime, freq)
        chart = Chart(tickers[i], data, coords[i-start][0], coords[i-start][1], coords[i-start][2], coords[i-start][3], app.tickCount, app.tickSize)
        chart.endLine = app.showEnd
        chart.maxLine = app.showMax
        chart.minLine = app.showMin
        if len(tickers) > 0:
            chart.fontSizeY = 15
        if len(tickers) > 1:
            chart.fontSizeY = 10
        if len(tickers) > 2:
            chart.fontSizeY = 8
        if len(tickers) > 3:
            chart.fontSizeY = 6
        app.Charts += [chart]