# This is the watch list 

import numpy as np 
import pandas as pd
from pandas_datareader import data as pdr 

# Market Data 
import yfinance as yf

# Graphing / Visualization 
import plotly.graph_objs as go 
from flask import Blueprint, render_template
from flask_login import login_user,  login_required , logout_user, current_user
import yfinance as yf
from datetime import datetime
from yfinance import Ticker
import requests
from yahoofinance import BalanceSheet,HistoricalPrices

watchlist = Blueprint('watchlist',__name__)

# Das hier ist die hauptseite, Der Route node des Programs
# Quasi ist das die frontseite der Homepage
@watchlist.route('/watchlist',methods = ['GET', 'POST'])
@login_required
def set():
    return render_template("watchlist.html")


def fig ():
    stock = 'TSLA'    
    df = yf.download(tickers=stock,period='1d',interval='1m')

    
    fig=go.Figure()

    fig.add_trace(go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'], name = 'market data'))

    fig.update_layout(
        title= str(stock)+' Live Share Price:',
        yaxis_title='Stock Price (USD per Shares)')               

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    return fig.show()


def get_watch_list(): 
    # Techstocks 
    tech_stocks = ['AAPL', 'AMZN', 'GOOG', 'META', 'MSFT', 'TSLA', 'NVDA', 'PYPL', 'SQ', 'CRM']

    for i in tech_stocks: 
        
        stock = Ticker(i)
        prices = stock.history(start="2023-01-01", end = datetime.today())

        
        ## hier wohl einfach in die database? 
    
    return prices



