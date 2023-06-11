from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user,  login_required , logout_user, current_user
from db_manager import db_manager
import requests
about = Blueprint('about',__name__)

@about.route('/about', methods=['GET', 'POST'])
def home():    
    return render_template("about.html", user = current_user)




        
    

