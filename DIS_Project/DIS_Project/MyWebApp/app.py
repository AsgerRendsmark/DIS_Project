# from stocks import get_stock
import psycopg2
from flask import Flask 
from flask_login import LoginManager, login_manager
from os import path
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import Table, Column, String, MetaData
db = SQLAlchemy() 


def create_app ():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    
    conn = psycopg2.connect(
        database="UID",
        user = "janjohannsen",  
        password = "password",
        host = "localhost",
            )

    cur = conn.cursor()
    app.config['UID_CONNECTION'] = conn    
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from views import views
    from auth import auth
    from stocks import stock
    from faves import faves
    # from models import User, Notes

    
    
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(stock, url_prefix = '/')
    app.register_blueprint(faves, url_prefix = '/')


   
    from UserOperations import UserOperations
    
    @login_manager.user_loader
    def load_user(user_id):
        return UserOperations.get_user_by_id(user_id)


    return app

    

