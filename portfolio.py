import math
from Date import *
import copy
from stockData import *

class Portfolio():
    def __init__(self):
        self.stocks = dict()
        self.value = 0
    def addStock(self, ticker, shares, price):
        self.stocks[ticker] = self.stocks.get(ticker, []) + [(shares, price)]
        self.value += shares * price
    def deleteStock(self, ticker, index):
        L = copy.copy(self.stocks[ticker])
        self.value -= latestData(ticker)*self.stocks[ticker][index][1]
        L = L[:index] + L[index+1:]
        self.stocks[ticker] = L
    def getString(self):
        result = []
        for val in self.stocks:
            result.append([val] + self.stocks[val])
        return result
    def size(self):
        count = 0
        for val in self.stocks:
            count += len(self.stocks[val])
        return count
    def getValue(self):
        total = 0
        for val in self.stocks:
            for x in self.stocks[val]:
                total += x[0]*x[1]
        return total
    def getStockVal(self, s):
        if s not in self.stocks:
            return 0
        total = 0
        for x in self.stocks[s]:
            total += x[0]*x[1]
        return total
    def getStockPerc(self, s):
        perc = self.getStockVal(s)/self.getValue()
        perc *= 100
        return perc
    def sell(self, stock, shares, price):
        for val in self.stocks[stock]:
            if self.almostEqual(val[0],shares) and self.almostEqual(val[1],price):
                self.stocks[stock].remove(val)
                self.value -= latestData(stock) * shares
                return 'SUCCESS'
        return None
    def cleanUp(self):
        for val in self.getString():
            if len(val) == 1:
                self.stocks.pop(val[0])
    def sellShares(self, stock, shares):
        remaining = shares
        i = 0
        if stock not in self.stocks:
            return 0
        while i < len(self.stocks[stock]):
            val = self.stocks[stock][i]
            if val[1]-remaining < 0:
                remaining -= val[1]
                self.stocks[stock].remove(val)
            elif val[1] - remaining == 0:
                self.stocks[stock].remove(val)
                self.cleanUp()
                self.value -= latestData(stock) * shares
                return shares
            else:
                self.stocks[stock][i] = (val[0], val[1]-remaining)
                self.cleanUp()
                self.value -= latestData(stock) * shares
                return shares
        if shares == remaining:
            self.cleanUp()
            self.value -= latestData(stock) * shares
            return shares
        self.cleanUp()
        self.value -= latestData(stock) * (shares-remaining)
        return shares-remaining
    def almostEqual(self, x, y):
        return abs(x - y) < 10**-5
    def getTickers(self):
        result = []
        for val in self.stocks:
            result += [val]
        return result
p = Portfolio()
p.addStock('NVDA', 145.13999938964844, 1)
p.deleteStock('NVDA', 0)