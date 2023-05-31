from flask import Blueprint, render_template, session, request, flash, redirect, url_for
import yfinance as yf
from flask_login import login_user,  login_required , logout_user, current_user
from db_manager import db_manager

hist  = Blueprint('hist',__name__)

@hist.route("/history", methods = ['GET', 'POST'])
@login_required
def fetch_history_of_stocks():        
    cur = db_manager.get_cursor()

  # Retrieve both id and symbol

    stocks = cur.execute("""SELECT id,symbol FROM stocks1;""")
    stocks = cur.fetchall()


    for stock in stocks:
        stock_id = stock[0]
        sym = stock[1]
        
        ticker = yf.Ticker(sym)
        hist = ticker.history(period="1mo")

        open_prices = hist['Open'].tolist()
        close_prices = hist['Close'].tolist()
        high_prices = hist['High'].tolist()
        low_prices = hist['Low'].tolist()
        volume = hist['Volume'].tolist()
        print("1")
        for i in range(len(open_prices)):
            open_price = round(open_prices[i], 8)
            close_price = round(close_prices[i], 8)
            high_price = round(high_prices[i], 8)
            low_price = round(low_prices[i], 8)
            volume_value = round(volume[i], 8)

    
            db_manager.insert_stock_history(stock_id, sym, "1mo", open_price, high_price, low_price, close_price, volume_value)

        stock_history = db_manager.get_stock_history(stock_id)

    return render_template("history.html", user=current_user, stock_history=stock_history)
    
