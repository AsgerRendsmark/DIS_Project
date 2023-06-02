from flask import Blueprint, render_template, request, flash, redirect, url_for

from User import User
from UserOperations import UserOperations
import yfinance as yf
from yfinance import Ticker
from flask_login import login_user,  login_required , logout_user, current_user, LoginManager
from views import views
from db_manager import db_manager
from yahoofinance import BalanceSheet,HistoricalPrices
from UserOperations import UserOperations

faves  = Blueprint('faves',__name__)
login_manager = LoginManager()

def add_favorite(stock_id):
    db_manager.add_favorite(current_user.id, stock_id)
    

def remove_favorite(stock_id):
    db_manager.remove_favorite(current_user.id, stock_id)
    


        

@faves.route("/faves", methods = ['GET', 'POST'])
@login_required
def render_faves():
    favorites = db_manager.get_user_favorites(current_user.id)
    cur = db_manager.get_cursor()
    faves = cur.execute("""select stocks1.id
                        from favorites join stocks1 on 
                        stocks1.id=favorites.stock_id """)
    
    faves = cur.fetchall()
    fave = []
    for i in faves:
        fave.append(i[0])
    if "POST":

        delete = request.form.get("remove")
        if delete: 
            remove_favorite(delete)
            flash("This stock has been removed from your favorites", category = 'success')
            return redirect(url_for('faves.render_faves'))

    return render_template("favorites.html", user = current_user, favorites = favorites)


    # # Update favorites after adding the new favorite
    #     favorites = db_manager.get_user_favorites(user.id)
    #     stocks = UserOperations.get_stock()
    #     
    #     stock_ids = [stock.id for stock in stocks]  # This creates a list of all stock IDs
    #     user_ids = [current_user.id for stock in stocks] # This creates a list of all user IDs
    #     db_manager.add_favorite(user.id, stock_ids.id)
    #     # This creates a list of all the stock IDs that the user has favorited
    #     db_manager.get_favorites(current_user.id)
    #     # This creates a list of all the stock IDs that the user has not favorited
    #     db_manager.get_user_favorites(current_user.id)


# @faves.route("/faves", methods = ['GET', 'POST'])
# @login_required
# def view_favorites():
#     user = UserOperations.get_user_by_id(current_user.id)
#     favorites = db_manager.get_user_favorites(user.id)

#     if request.method == 'POST':
#         stock_id = UserOperations.get_stock_by_all()  # Get the stock ID from the clicked button
#         db_manager.add_favorite(user.id, stock_id.id)

#         # Update favorites after adding the new favorite
#         favorites = db_manager.get_user_favorites(user.id)

#     stocks = UserOperations.get_stock_by_all()
#     return stock
# print(view_favorites())
# def test(): 
#     u = User(1,"janjohannsenjan@gmail.com","jan","Jan")
#     stocks = UserOperations.get_stock_by_all()
#     user = UserOperations.get_user_by_id(u.id)
#     stock_ids = [stock.id for stock in stocks]  # This creates a list of all stock IDs
#     # user_ids = [user.id for stock in stocks] # This creates a list of all user IDs
#     whih = db_manager.add_favorite(u.id, stock_ids[0])

    
#     return whih



