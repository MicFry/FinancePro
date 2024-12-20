import yfinance as yf
import math
from cmu_graphics import *
from Chart import *
from stockData import *
from Date import *
from portfolioViewer import *
from getStockData import *

def onAppStart(app):
    loadAppDataPortfolioViewer(app)
    app.showEnd = True
    app.showMin = True
    app.showMax = True
    loadChartValues(app)
    app.page = 'home'
    #options are: 'home', 'Portfolio', 'Chart'
def redrawAll(app):
    drawLabel("Account Value: ${:.2f}".format(app.p.value + app.Cash), 650, 70, size = 20, bold = True)
    if app.page != 'home':
        drawLabel('<', 25, 25, size = 40, bold = True)
    if app.page == 'home':
        drawLabel('Welcome!', 400, 50, size = 40, bold = True)
        drawLabel('Cash: $' + "{:.2f}".format(app.Cash), 200, 150, size = 40)
        drawRect(100, 275, 600, 150, fill = None, border = 'black')
        drawLabel('View Charts', 400, 350, size = 40)
        drawRect(100, 475, 600, 150, fill = None, border = 'black')
        drawLabel('Edit Portfolio', 400, 550, size = 40)
    if app.page == 'Chart':
        drawChartView(app)
    elif app.page == 'Portfolio':
        drawPortfolioViewer(app)
def onMousePress(app, mouseX, mouseY):
    if inBoundsBack(app, mouseX, mouseY):
        app.page = 'home'
    elif app.page == 'home':
        mousePressHome(app, mouseX, mouseY)
    elif app.page == 'Portfolio':
        mousePress(app, mouseX, mouseY)
    if app.page == 'Chart':
        mousePressCharts(app, mouseX, mouseY)
def inBoundsBack(app, x, y):
    return 0 <= x <= 50 and 0 <= y <= 50
def onKeyPress(app, key):
    if app.page == 'Portfolio':
        KeyPress(app, key)
    if app.page == 'Chart':
        keyPressCharts(app, key)
def mousePressHome(app, mouseX, mouseY):
    if inBoundsPort(mouseX, mouseY):
        app.page = 'Portfolio'
    elif inBoundsChart(mouseX, mouseY):
        loadChartValues(app)
        app.page = 'Chart'

def inBoundsPort(x, y):
    return 100 <= x <= 700 and 475 <= y <= 625
def inBoundsChart(x, y):
    return 100 <= x <= 700 and 275 <= y <= 425
def main():
    runApp(width = 800, height = 800)
main()