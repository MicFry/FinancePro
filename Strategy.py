from Date import *
from stockData import *
class Strategy():
    def __init__(self, buyRSI = 0, sellRSI = 0, initalCash = 10000, numShares = 15):
        self.sellRSI = sellRSI
        self.currCash = initalCash
        self.amt = 0
        self.numShares = numShares
    def updateNumShares(self, rsi, cash, baseShares):
        alpha = 0.75
        if rsi < 30:
            return max(baseShares, alpha * (35-rsi)**2)
        if rsi > self.sellRSI:
            return max(baseShares, alpha * (self.sellRSI-rsi)**2)
        return 15
    def calculateProfits(self, ticker, start, end):
        date1 = start
        date2 = end
        data = RSIdata(ticker,date1, date2, '1d')
        buy = 0
        sell = 0
        for price, rsi in data:
            self.numShares = self.updateNumShares(rsi, self.currCash, self.numShares)
            if rsi <= self.buyRSI:
                buy += 1
                self.currCash -= self.numShares*price
                if self.currCash < 0:
                    self.currCash += self.numShares*price
                else:
                    self.amt += self.numShares
            if rsi > self.sellRSI and self.amt > self.numShares:
                sell += 1
                self.currCash += self.numShares * price
                self.amt -= self.numShares
        self.currCash += self.amt * price
        return self.currCash
maxProfit = 0
optimalBuy = 0
optimalSell = 0
startingCash = 10000
date1 = Date(1, 1, 2022)
date2 = Date(1, 1, 2024)
for buy in range(30, 43):
    for sell in range(buy+10, 95):
        S1 = Strategy(buy, sell, startingCash, 20)
        val = S1.calculateProfits('NVDA', date1, date2)
        if val > maxProfit:
            maxProfit = val
            optimalBuy = buy
            optimalSell = sell
        print(maxProfit)
date1 = Date(1, 1, 2024)
date2 = Date(11, 21, 2024)
S1 = Strategy(optimalBuy, optimalSell, startingCash, 20)
val = S1.calculateProfits('GOOGL', date1, date2)
retestedProfit = val
print("================")
print(optimalBuy, optimalSell)
percent = (maxProfit - startingCash)/startingCash
percent *= 100
print(str(percent) + '%')
print("================")
print("retested profit:", (retestedProfit - startingCash))
percent = (retestedProfit - startingCash)/startingCash
percent *= 100
print(str(percent) + '%')