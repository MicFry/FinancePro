import yfinance as yf
import math
from Date import *
import ta
import pandas as pd
import datetime
from datetime import datetime
from stockPractice import *
def getData(ticker, start1, end1, inter):
    s = start1.getDateFormat()
    e = end1.getDateFormat()
    if end1 < start1:
        temp = s
        s = e
        e = temp
    result = []
    data = yf.download(ticker, start = s, end = e, interval = inter)
    for time, (open_price, _) in data[['Open', 'Close']].iterrows():
        result.append((time, open_price))
    return result
def Data(ticker):
    start = Date(11, 29, 2023)
    end = start.backTime(0, 1, 0)
    result = getData(ticker, start, end, '1d')
    return result
def latestData(ticker):
    today = datetime.today()
    day1 = Date(today.month, today.day, today.year).backTime(1, 0, 0)
    day2 = Date(today.month, today.day, today.year)
    r = getDataHistory(ticker, '1d', '1m')
    try:
        return r[-1][1]
    except:
        return 'ERROR'
def chartData(ticker, p, inter):
    result = []
    data = yf.Ticker(ticker).history(period = p, interval = inter)
    for time, (open_price, _) in data[['Open', 'Close']].iterrows():
        result.append(open_price)
    return result
def RSIdata(ticker, start1, end1, inter):
    s = start1.getDateFormat()
    e = end1.getDateFormat()
    if end1 < start1:
        temp = s
        s = e
        e = temp
    period = 14
    df = yf.Ticker(ticker).history(start=s, end=e, interval=inter)
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window = 14).rsi()
    df = df[['Close', 'RSI']]
    result = []
    df = df.dropna(axis=0)
    for time, (price, r) in df[['Close', 'RSI']].iterrows():
        result.append((price, r))
    return result