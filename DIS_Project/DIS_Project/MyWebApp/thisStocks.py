def lst_of_stocks():
    fin_tech_companies = ['AAPL','MSFT','CSCO','AMZN','INTC','META']
    new_lst = {}
    for fin in fin_tech_companies:
        try:
            p = get_stock_price(fin)
            if p is not None:
                new_lst.update({fin:p})
                
            else:
                print(f'Got None for {fin}')
        except Exception as e:
            print(f'Error getting price for {fin}: {e}')
    try: 
        df= pd.DataFrame(new_lst.items(), columns=['Stock','Price'])
        df.to_csv('stock.csv', index=False)
        UserOperations.add_stock(current_user.id,new_lst["Name"],df["Stock"],df["Price"])
    except Exception as e:
        print(f'Error writing to csv:  {e}')
    
    return df

def get_portfolio():
    pass

def get_stock_history():
    lst = lst_of_stocks()
    stock = lst['Stock']
    try: 
        for i in stock:
            ticker = yf.Ticker(i)
            hist = ticker.history(period="max")
            hist.to_csv('stock_history.csv', index=False)    
    except Exception as e:
        print(f'Error getting stock history: {e}')
        
    return hist

print(get_stock_history())

def plot_stock_info():
    g = get_stock_history()
    fig = go.Figure(data=[go.Candlestick(x=g.index,
                open=g['Open'],
                high=g['High'],
                low=g['Low'],
                close=g['Close'])])
    
    fig.update_layout(
        title='Stock Price',
        yaxis_title='Price',
        shapes = [dict(
            x0='2020-01-01', x1='2020-01-01', y0=0, y1=1, xref='x', yref='paper',
            line_width=2)],
        annotations=[dict(
            x='2020-01-01', y=0.05, xref='x', yref='paper',
            showarrow=False, xanchor='left', text='Increase Period Begins')]
        
    )
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.show()
    return fig
print(plot_stock_info())
def stock_info(ticker_symbol):
    pass

def get_all_stocks(): 
    pass


def lst_of_stocks():
    fin_tech_companies = ['AAPL','MSFT','CSCO','AMZN','INTC','META']
    new_lst = {}
    for fin in fin_tech_companies:
        try:
            p = get_stock_price(fin)
            if p is not None:
                new_lst.update({fin:p})
                
            else:
                print(f'Got None for {fin}')
        except Exception as e:
            print(f'Error getting price for {fin}: {e}')
    try: 
        df= pd.DataFrame(new_lst.items(), columns=['Stock','Price'])
        df.to_csv('stock.csv', index=False)
        price = get_stock_price(fin)
        db_manager.insert_stock(stock, 'unknown', 0,price,0)

    except Exception as e:
        print(f'Error writing to csv:  {e}')
    
    return df



