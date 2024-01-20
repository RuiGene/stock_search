import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, DateFormatter

tickers = ["AAPL", "MSFT", "AAPL"]
shares = [3, 2, -6]
date_purchased = ['2020-05-01', '2021-08-01', '2022-11-01']
date_purchased = pd.to_datetime(date_purchased)

data = pd.DataFrame()
for i in range(len(tickers)):
    stock = yf.Ticker(tickers[i])
    stock_data = stock.history(start = date_purchased[i])
    stock_data[tickers[i]] = stock_data['Close'] * shares[i]
    data = pd.concat([data, stock_data[tickers[i]]], axis=1)

data['total_portfolio_value'] = data.sum(axis=1)
fig, ax = plt.subplots(figsize=(10, 5)) # set the figsize parameter to increase the width of the plot
ax.plot(data.index, data['total_portfolio_value'], label='Total Portfolio Value')

# set the x-axis tick locator and formatter to show only the years
years = YearLocator()
year_format = DateFormatter('%Y')
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(year_format)

st.plotly_chart(fig, use_container_width=True)