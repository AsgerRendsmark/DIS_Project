from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user,  login_required , logout_user, current_user, LoginManager
# from models import User, Notes
from flask import current_app   
import psycopg2.extras 
from UserOperations import UserOperations
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth',__name__)
login_manager = LoginManager()

# Sets all the user interactions 
@auth.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST': 

        email = request.form.get('email')
        id = request.form.get('id')
        password = request.form.get('password')
        user = UserOperations.get_user_by_email(email=email)
        if user :
                
                if check_password_hash(user.password, password):
                    flash('Logged in succesfully', category = 'success')
                    login_user(user)
                
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect Password', category = 'error')
        else:
            flash('Email does not Exist', category = 'error' )
            
    
    return render_template("login.html", user = current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# Get and Post are HTTP mehtods that get and retrieve data 
@auth.route("/sign-up",  methods = ['GET', 'POST'])
def sign_up():    
    if request.method == 'POST':  
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        user = UserOperations.get_user_by_email(email)
        print("user", user)
        if user:
            flash('Email Already exists', category = 'error')
            return redirect(url_for('auth.login'))
        else: 
            UserOperations.add_user(email, first_name, generate_password_hash(password1, method = 'sha256'))
            flash('Account created', category = 'success')
            return redirect(url_for('views.home'))        
    return  render_template("signup.html", user = current_user)




## Could have ; password safety 