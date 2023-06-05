from flask import Blueprint, render_template, request, flash, redirect, url_for
from UserOperations import UserOperations
from flask_login import login_user,  login_required , logout_user, current_user
from db_manager import db_manager
import finnhub
import requests
#from yahoofinance import BalanceSheet,HistoricalPrices
from UserOperations import UserOperations
from stock_hist import hist

stock = Blueprint('stock', __name__)

finnhub_client = finnhub.Client(api_key="chjka21r01qh5480hn3gchjka21r01qh5480hn40")
def render_stocks():
    cur = db_manager.get_cursor()
    cur.execute("""SELECT id, 
                    name, price, symbol, total
                    FROM stocks1
                    ORDER BY name ASC;""")
    
    stocks = cur.fetchall()
        

    return render_template("stock2.html", stocks=stocks, user=current_user)


###########
# refactor#
###########
@stock.route('/stocks', methods=['GET', 'POST'])
@login_required
def render_stocks_from_db():
    cur = db_manager.get_cursor()
    in_list = cur.execute("""select favorites.stock_id from favorites join stocks1 on stocks1.id=favorites.stock_id where favorites.user_id = %s""", (current_user.id,))
    in_list = cur.fetchall()
    if request.method == 'POST':
        stock_id = request.form.get("add")
        view_id = request.form.get("symbol")
        if stock_id: 
            db_manager.add_favorite(current_user.id, stock_id)
            if in_list:
                for i in in_list:
                    if i[0] == int(stock_id):
                        flash("This stock is already in your favorites", category = 'error' )
                        return render_stocks()
            flash("This stock has been added to your favorites", category = 'success')
            return render_stocks()
        elif view_id:
            cur.execute("SELECT  * FROM stocks1 WHERE symbol = %s", (view_id,))
            stock_name = cur.fetchall()
            if stock_name:
                
                return redirect(url_for('hist.render_stock_history',  symbol=view_id))
                
    
    return render_stocks()


@stock.route('/stocks/update', methods=['GET', 'POST'])
def update_stocks(): 
    cur = db_manager.get_cursor()
    cur.execute("SELECT symbol FROM stocks1")
    tickers = cur.fetchall()

    for ticker in tickers: 
        response = requests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker[0]}&token=your_token_here')
        stock_data= response.json() 
        stock_data = stock_data.get('c')

        if stock_data is not None:
            cur.execute("UPDATE stocks1 SET price = %s WHERE symbol = %s", (stock_data, ticker[0]))
            db_manager.commit()

    return render_stocks()


@stock.route('/stocks/delete', methods=['GET', 'POST'])
def remove_stocks_that_are_0(): 
    cur = db_manager.get_cursor()
    cur.execute("SELECT id FROM stocks1 WHERE price =0")
    ids = cur.fetchall()
    for i in ids:
        cur.execute("DELETE FROM stocks1 WHERE  price = 0")
        cur.execute("DELETE FROM stock_history WHERE stock_id = %s", (i[0],))
        db_manager.commit()
    return render_stocks()
    
# def test():
#     cur = db_manager.get_cursor()
#     total = cur.execute("SELECT total FROM stocks1")
#     s = cur.fetchall()
#     ticker = yf.Ticker("AAPL")

#     ss = finnhub_client.quote('AAPL')

#     return ss.get("t")*100
    
# print(test())
# def portfolio(): 
#     # db_manager.insert_stock(fins, fins, 1, price, price)
#     pass 

# def prep_portfolio():
#     fins = ['IFNNY', 'CUBE', 'FCOB', 'MBC', 'SEYMF', 'CTKB', 'EATR', 'MNKD', 'HWKZ.U', 'ICPT', 'TOVX', 'VMTG', 'DOCRF', 'PBDM', 'MCFT', 'ANCTF', 'TOACU', 'PTMC', 'BITCF', 'BCV.PRA', 'FTCI', 'AKZOY', 'SPMYY', 'BUDZ', 'DKSC', 'XMLV', 'RAIN', 'TSGTF', 'XRT', 'CLAD', 'VEII', 'GIKLY', 'HTIA', 'WRDEF', 'ALLY', 'CNBB', 'FSBC', 'CALF', 'CHZQ', 'SGGSF', 'ETCK', 'DGIV', 'GLNLF', 'GRYCF', 'RDN', 'EFA', 'MMTIF', 'BHVN', 'BCNHF', 'GWSFF', 'VISM', 'CNP', 'POL', 'KEYUF', 'ABOS', 'GOSY', 'CCWF', 'AMAL', 'GHIXW', 'CCOJY', 'CDJM', 'OABI', 'IBHD', 'NBCT', 'SMWFF', 'TSVT', 'CHMI', 'DHBUF', 'TGRR', 'JNDAF', 'NLVVF', 'WEBNF', 'LFLYW', 'QTUM', 'NXSGD', 'CRC', 'PH', 'PPHPW', 'GQRE', 'PEO', 'HYHY', 'SNAXW', 'COCSF', 'JGGCU', 'AVPI', 'PSGR', 'GBERY', 'ICLN', 'TBMC', 'GWRS', 'INSE', 'OCEAW', 'OOAG', 'MCN', 'CBAF', 'XEL', 'CKALF', 'HFBL', 'SLKEF', 'MALG']
    
#     stocks = []
#     # for fins in fin:
#     try:
#         current_price = get_stock(fins)
#         stock = Ticker(fins)
#         stock_name = stock.info['longName']
#         open = stock.info['open']
#         close = stock.info['previousClose']
#         high = stock.info['dayHigh']
#         low = stock.info['dayLow']
#         stocks.append((fins, stock_name, open, current_price, high))
        
#     except Exception as e:
#         print(f"Error occurred with stock {fins}: {e}")    



