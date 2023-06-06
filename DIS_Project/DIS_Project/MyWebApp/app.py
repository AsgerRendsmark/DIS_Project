# from stocks import get_stock
import psycopg2
from flask import Flask 
from flask_login import LoginManager, login_manager,login_required
from os import path



def create_app ():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
 
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from views import views
    from auth import auth
    from stocks import stock
    from faves import faves
    from stock_hist import hist
    from stock_info import info
    from searchbar import search
    
    app.register_blueprint(search, url_prefix = '/')
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(stock, url_prefix = '/')
    # app.register_blueprint(profile, url_prefix = '/')
    app.register_blueprint(hist, url_prefix = '/')
    app.register_blueprint(faves, url_prefix = '/')
    app.register_blueprint(info, url_prefix = '/')



   
    from UserOperations import UserOperations
    
    @login_manager.user_loader
    def load_user(user_id):
        print(user_id)
        return UserOperations.get_user_by_id(user_id)

  

    return app


    

