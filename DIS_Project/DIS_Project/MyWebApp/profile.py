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
from faves import faves
import time
from stocks import render_stocks

profile = Blueprint('profile', __name__)
def get_user(): 

    cur = db_manager.get_cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (current_user.id,))
    user = cur.fetchone()
    return user

@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def show_profile():
    # if(request.method == 'POST'):
    user = get_user()
    #     if request.form.get("myprofile"):
    stock = render_stocks()    
    return render_template("profile.html", user=current_user.id, stocks=stock)