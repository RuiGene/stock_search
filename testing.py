# Need to add cash balance
# Need to initialise DF
# Convert to NZD 
# Read in from database
# Update curretn database holdings

import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter, YearLocator
import sqlite3
import pandas as pd

conn = sqlite3.connect("stock_transactions.db")
query = "SELECT * FROM stock_transactions"
df = pd.read_sql_query(query, conn)
conn.close()

# Data cleaning
df['date'] = pd.to_datetime(df['date'])

current_holdings_shares = []
current_holdings = []

data = pd.DataFrame(columns = ['total_portfolio_value', 'cash_balance'])
for i in range(len(df)):
    if df['ticker'][i] not in current_holdings:
        current_holdings.append(df['ticker'][i])
        current_holdings_shares.append(df['units'][i])
        stock = yf.Ticker(df['ticker'][i])
        stock_data = stock.history(start = df['date'][i])
        data[df['ticker'][i]] = stock_data['Close'] * df['units'][i]
    
    else:
        # current_holdings_shares['AAPL'] += update to correct number of shares
        stock = yf.Ticker(df['ticker'][i])
        stock_data = stock.history(start = df['date'][i])
        temp_data = pd.DataFrame()
        temp_data[df['ticker'][i]] = stock_data['Close']*df['units'][i]
        data = pd.merge(data[df['ticker'][i]], temp_data[df['ticker'][i]], left_index = True, right_index = True, how = 'left', suffixes = ('_df1', '_df2'))
        data.fillna(0, inplace=True)
        data[df['ticker'][i]] = data[df['ticker'][i] + '_df1'] + data[df['ticker'][i] + '_df2']
        data = data.drop(columns = [df['ticker'][i] + '_df1', df['ticker'][i] + '_df2'])
    
data['total_portfolio_value'] = data.sum(axis=1)
fig, ax = plt.subplots(figsize=(10, 5)) # set the figsize parameter to increase the width of the plot
ax.plot(data.index, data['total_portfolio_value'], label='Total Portfolio Value')

# set the x-axis tick locator and formatter to show only the years
years = YearLocator()
year_format = DateFormatter('%Y')
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(year_format)
