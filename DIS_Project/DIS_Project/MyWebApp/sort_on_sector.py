import yfinance as yf
from flask import Blueprint, render_template, request, flash, redirect, url_for

from flask_login import login_user,  login_required , logout_user, current_user
from db_manager import db_manager
import finnhub
import requests
#from yahoofinance import BalanceSheet,HistoricalPrices
from UserOperations import UserOperations
from stock_hist import hist
import pandas as pd
import websocket 
from flask import Flask, jsonify
import _thread
import time
import rel
import csv
import concurrent.futures
import random
from yfinance import Ticker

cat = Blueprint('cat', __name__)

def get_sector():
    cur = db_manager.get_cursor()
    cur.execute("""SELECT sector FROM stock_details GROUP BY sector ORDER BY sector;""")
    sectors = cur.fetchall()
    return [sector[0] for sector in sectors]

def get_stocks_by_sector(sector):
    cur = db_manager.get_cursor()
    cur.execute("""SELECT stocks1.name, stocks1.symbol FROM stocks1 JOIN stock_details 
                ON stocks1.symbol = stock_details.symbol WHERE stock_details.sector = %s 
                ORDER BY stocks1.name ASC;""", (sector,))
    stocks = cur.fetchall()
    
    return stocks


@cat.route('/sector', methods=['GET', 'POST'])
@login_required
def render_sector():
    sectors = get_sector()
    sector_stocks = {}
    for sector in sectors:
        stocks = get_stocks_by_sector(sector)
        sector_stocks[sector] = stocks
    return render_template('categories.html',user = current_user, sectors=sectors, sector_stocks=sector_stocks)



