from flask import Blueprint, render_template
from flask_login import login_user,  login_required , logout_user, current_user
from db_manager import db_manager
views = Blueprint('views',__name__)

# Das hier ist die hauptseite, Der Route node des Programs
# Quasi ist das die frontseite der Homepage
@views.route('/home')
def home():
    winners_list = make_winners()
    news_list = print_news()
    return render_template("home.html", user = current_user, winners=winners_list, news=news_list)

@views.route('/')
def home1():
    winners_list = make_winners()
    news_list = print_news()
    return render_template("home.html", user = current_user, winners=winners_list, news=news_list)


def winners():
    cur = db_manager.get_cursor()
    cur.execute("""SELECT stocks1.symbol, COUNT(DISTINCT favorites.user_id) as favorite_count
                    FROM stocks1 
                    LEFT JOIN favorites 
                    ON stocks1.id = favorites.stock_id
                    GROUP BY stocks1.id, stocks1.name""")
    favorite_counts = cur.fetchall()
    return favorite_counts

def make_winners():
    favorite_counts = winners()
    win_list = []   
    for favorite_count in favorite_counts:
        if favorite_count[1] > 0:
            win_list.append(favorite_count)
    return win_list[:5]

from yfinance import Ticker
import requests
import finnhub

api_key="chjka21r01qh5480hn3gchjka21r01qh5480hn40"

def get_news():
    news = requests.get(f"https://finnhub.io/api/v1/news?category=general&token={api_key}")
    news = news.json()
    return news

def print_news():
    news_items = get_news()
    news_list = []
    for i in news_items:
        news_list.append({'headline': i['headline'], 'summary': i['summary'], 'url': i['url']})
    
    return news_list[:5]
