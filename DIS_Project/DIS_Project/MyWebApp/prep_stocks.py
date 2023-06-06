import yfinance as yf
from flask import Blueprint, render_template, request, flash, redirect, url_for
from UserOperations import UserOperations
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

finnhub_client = finnhub.Client(api_key="chjka21r01qh5480hn3gchjka21r01qh5480hn40")
app = Flask(__name__)

# @app.route("/stocks")
def get_stock_symbols_from_csv():
    with open('stocks.csv', 'r') as f:

        reader = csv.reader(f)

        next(reader, None)
        listofstocks = []
        for row in reader :
            ticker = row[0]
            listofstocks.append(ticker)
        return listofstocks
    
def trim_list_random():
    l = get_stock_symbols_from_csv()
    new_list = []
    for i in l:
        if '^' in i : 
            continue
        else:
            new_list.append(i)
        
    new_list = random.sample(new_list, 100)
    
    return new_list

def get_stock(ticker):
    response = requests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker}&token=chjka21r01qh5480hn3gchjka21r01qh5480hn40')
    return response.json()


def get_stock_price(ticker):
    stock = get_stock(ticker)
    price = stock['c']
    return price

def get_stock_name(ticker):
    l = get_stock_symbols_from_csv()
    for i in l:
        if i == ticker:
            ticker = Ticker(i)
            stock = ticker.info
            
    name = stock['longName']
    return name

def get_stock_highprice(ticker):
    stock = get_stock(ticker)
    price = stock['h']
    return price    
def get_stock_lowprice(ticker):
    stock = get_stock(ticker)
    price = stock['l']
    return price    

def get_stock_openprice(ticker):
    stock = get_stock(ticker)
    price = stock['o']
    return price    

def get_stock_closeprice(ticker):
    stock = get_stock(ticker)
    price = stock['pc']
    return price



def get_stock_change(ticker):
    stock = get_stock(ticker)
    price = stock['c']
    return price

def get_stock_changepercent(ticker):    
    stock = get_stock(ticker)
    price = stock['dp']
    return price


def info(ticker):
    price = get_stock_price(ticker)
    name = get_stock_name(ticker)
    high = get_stock_highprice(ticker)
    low = get_stock_lowprice(ticker)
    open_price = get_stock_openprice(ticker)
    close = get_stock_closeprice(ticker)
    change = get_stock_change(ticker)
    change_percent = get_stock_changepercent(ticker)
    return price, name, high, low, open_price, close, change, change_percent


def put_into_db():
    stock = trim_list_random()
    try:
        for i in stock:
            price, name, high, low, open_price, close, change, change_percent = info(i)
            db_manager.insert_stock_without_id(i, name, open_price, price, high, close, low)
            db_manager.commit()
            print(i, name, open_price, price, high, close, low)
            print("inserted into db")
            time.sleep(1)
    except Exception as e:
        return e
    return "done"
        
print("starting")
print(put_into_db())

    




