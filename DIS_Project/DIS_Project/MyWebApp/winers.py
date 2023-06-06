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

api_key="chjka21r01qh5480hn3gchjka21r01qh5480hn40"

def get_news():
    news = requests.get(f"https://finnhub.io/api/v1/news?category=general&token={api_key}")
    news = news.json()
    return news

def print_news():
    news = get_news()
    for i in news:
        headline = i['headline']
        summary = i['summary']
        url = i['url']
    return headline, summary, url

