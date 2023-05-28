from flask import Blueprint, render_template, request
from flask_login import login_user,  login_required , logout_user, current_user
from form import searchForm
from stocks import stock
from db_manager import db_manager

search = Blueprint('search',__name__)

@search.context_processor
def base():
    form = searchForm()
    return dict(form = form)

@search.route('/search', methods = ['GET', 'POST'])
@login_required
def searched():
    
    form = searchForm()
    cur = db_manager.get_cursor()
    stock= cur.execute("SELECT * FROM stocks1")
    stock = cur.fetchone()


    if request.method == 'POST':
        if form.validate_on_submit():
            print("jan") 
            search = form.search.data
            return render_template("search.html", user = current_user,searched = stock, form = form)
    return render_template("search.html", user = current_user)
