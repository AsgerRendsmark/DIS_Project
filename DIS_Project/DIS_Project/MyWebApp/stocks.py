from flask import Blueprint, render_template, request, flash, redirect, url_for
import numpy as np 
import pandas as pd
from pandas_datareader import data as pdr 
from UserOperations import UserOperations
import yfinance as yf
from flask_login import login_user,  login_required , logout_user, current_user
from yfinance import Ticker
from views import views
from app import db 
from db_manager import db_manager
import finnhub
import requests
from yahoofinance import BalanceSheet,HistoricalPrices
from UserOperations import UserOperations

import time
stock = Blueprint('stock', __name__, url_prefix='/stocks')

finnhub_client = finnhub.Client(api_key="chjka21r01qh5480hn3gchjka21r01qh5480hn40")
# Stock candles

# Das hier ist die hauptseite, Der Route node des Programs
# Quasi ist das die frontseite der Homepage

# Fetch real time data from finnhub
def get_stock(ticker):
    response = requests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker}&token=chjka21r01qh5480hn3gchjka21r01qh5480hn40')
    return response.json()['c']  # 'c' corresponds to the current price

def portfolio(): 
    # db_manager.insert_stock(fins, fins, 1, price, price)
    pass 

def prep_portfolio():
    fins = ['IFNNY', 'CUBE', 'FCOB', 'MBC', 'SEYMF', 'CTKB', 'EATR', 'MNKD', 'HWKZ.U', 'ICPT', 'TOVX', 'VMTG', 'DOCRF', 'PBDM', 'MCFT', 'ANCTF', 'TOACU', 'PTMC', 'BITCF', 'BCV.PRA', 'FTCI', 'AKZOY', 'SPMYY', 'BUDZ', 'DKSC', 'XMLV', 'RAIN', 'TSGTF', 'XRT', 'CLAD', 'VEII', 'GIKLY', 'HTIA', 'WRDEF', 'ALLY', 'CNBB', 'FSBC', 'CALF', 'CHZQ', 'SGGSF', 'ETCK', 'DGIV', 'GLNLF', 'GRYCF', 'RDN', 'EFA', 'MMTIF', 'BHVN', 'BCNHF', 'GWSFF', 'VISM', 'CNP', 'POL', 'KEYUF', 'ABOS', 'GOSY', 'CCWF', 'AMAL', 'GHIXW', 'CCOJY', 'CDJM', 'OABI', 'IBHD', 'NBCT', 'SMWFF', 'TSVT', 'CHMI', 'DHBUF', 'TGRR', 'JNDAF', 'NLVVF', 'WEBNF', 'LFLYW', 'QTUM', 'NXSGD', 'CRC', 'PH', 'PPHPW', 'GQRE', 'PEO', 'HYHY', 'SNAXW', 'COCSF', 'JGGCU', 'AVPI', 'PSGR', 'GBERY', 'ICLN', 'TBMC', 'GWRS', 'INSE', 'OCEAW', 'OOAG', 'MCN', 'CBAF', 'XEL', 'CKALF', 'HFBL', 'SLKEF', 'MALG']
    
    stocks = []
    # for fins in fin:
    try:
        current_price = get_stock(fins)
        stock = Ticker(fins)
        stock_name = stock.info['longName']
        open = stock.info['open']
        close = stock.info['previousClose']
        high = stock.info['dayHigh']
        low = stock.info['dayLow']
        stocks.append((fins, stock_name, open, current_price, high))
        
    except Exception as e:
        print(f"Error occurred with stock {fins}: {e}")    
    
@stock.route('/stocks', methods=['GET', 'POST'])
@login_required     
def render_stocks_from_db():
    cur = db_manager.get_cursor()

    if request.method == 'POST':
        stock_id = request.form.get("add")  # Get the stock ID from the form
        if stock_id: 
            db_manager.add_favorite(current_user.id, stock_id)  # Add the favorite
            # Redirect to the same page to update the displayed favorites
            return redirect(url_for('stock.render_stocks_from_db'))

    # For GET requests, display the current stocks
    cur.execute("SELECT * FROM stocks1")
    stocks = cur.fetchall()
    return render_template("stock2.html", stocks=stocks, user=current_user)

    # else:
    #     stocks =  UserOperations.get_stock(symbol, name, open_price, current_price, total)
    #     return render_template("stock2.html", stocks=stocks, user=current_user)
# @stock.route("/stock", methods = ['GET', 'POST'])
# @login_required
# def add_to_favorites():
#     user = UserOperations.get_user_by_id(current_user.id)
    
#     if request.method == 'POST':
#         print("here!! ")    
        
#         stock_id = request.form.get("add")  # Get the stock ID from the form
#         if stock_id: 
#             print("here!!! ")
#             db_manager.add_favorite(user.id, stock_id)  # Add the favorite
#             # Redirect to the same page to update the displayed favorites
#             print(stock_id)
#             return redirect(url_for('stocks'))
        

#     # For GET requests, display the current favorites
#     favorites = db_manager.get_user_favorites(user.id)
#     return render_template("stock2.html", user=current_user, favorites=favorites)

# @stock.route('/faves', methods=['POST'])
# @login_required
# def add_to_favorites():
#     if request.method == 'POST':
#         # Get the symbol from the request
#         symbol = request.form.get('symbol')
#         # Add the stock to the current user's favorites
#         db_manager.add_favorites(current_user.id, symbol)
#         return redirect(url_for('favorites.html'))

def get_all_stocks(): 
    stocks = []
    api_key = 'chjka21r01qh5480hn3gchjka21r01qh5480hn40'
    response = requests.get(f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={api_key}")
    data = response.json()
    more_data = data[0:100]
    for i in more_data:
        stocks.append(i['symbol'])
        
    return stocks




# Extract the top 100 stock symbols








