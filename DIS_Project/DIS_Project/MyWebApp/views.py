from flask import Blueprint, render_template
from flask_login import login_user,  login_required , logout_user, current_user

views = Blueprint('views',__name__)

# Das hier ist die hauptseite, Der Route node des Programs
# Quasi ist das die frontseite der Homepage
@views.route('/home')
def home():
    return render_template("home.html", user = current_user)

@views.route('/')
def home1():
    return render_template("home.html", user = current_user)

