import yfinance as yf
import math
from cmu_graphics import *
import pytz
from Date import *
def getDataHistory(ticker, hist, inter):
    stock = yf.Ticker(ticker)
    result = []
    data = stock.history(period = hist, interval = inter)
    for time, (open_price, _) in data[['Open', 'Close']].iterrows():
        result.append((time, open_price))
    return result
# date = Date(4, 26, 2024)
# print(date)
# date.backTime(26, 4, 1)
# print(date)
# start = Date(12, 2, 2024)
# end = start.backTime(1, 0, 0)
# result = getDataHistory('NVDA', '1m')
# for (a,b) in result: print(a, b)
# print(len(result))