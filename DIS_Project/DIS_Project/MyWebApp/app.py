from flask import Flask, session
from flask_login import LoginManager
from views import views
from auth import auth
from stocks import stock
from faves import faves
from stock_hist import hist
from stock_info import info
from sort_on_sector import cat
from About import about
from UserOperations import UserOperations
from prep_stocks import put_into_db
from stock_info import put_info_into_db
from threading import Thread
import time
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(stock, url_prefix='/')
app.register_blueprint(faves, url_prefix='/')
app.register_blueprint(info, url_prefix='/')
app.register_blueprint(cat, url_prefix='/')
app.register_blueprint(about, url_prefix='/')
app.register_blueprint(hist, url_prefix='/')

@login_manager.user_loader
def load_user(user_id):
    return UserOperations.get_user_by_id(user_id)

@app.route('/clearsession')
def clearsession():
    session.clear()
    return "Session has been cleared"

def update_database():
    try:
        print("Updating database")
        put_into_db()
        put_info_into_db()
        print("Database updated")
        print("Running on http://127.0.0.1:5000") 
    except Exception as e:
        print(f"Error updating database: {e}")

if __name__ == '__main__':
    thread = Thread(target=update_database)
    thread.start()  
    app.run(debug=True)
