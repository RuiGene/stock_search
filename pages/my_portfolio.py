# https://site.financialmodelingprep.com/developer/docs/
import streamlit as st
import fundamentalanalysis as fa
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta, datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
from matplotlib import ticker
API_KEY = '85fe259a4ec6fad3cbe55a5ddaf7f9b4'

st.set_page_config(page_title="Stocks", layout = "wide")

tickers = ["VOO", "VOO", "SCHB", "VOOV", "SCHD", "KO", "TSLA"]
shares = [2.499, 3, 21.185, 6.961, 13.1406, 8.437, 2.4786]
date_purchased = ['2022-08-03', '2022-09-07', '2022-11-16', '2022-12-07', '2023-01-24', '2023-03-07',
                  '2023-03-07']
date_purchased = pd.to_datetime(date_purchased)

def portfolio(tickers, shares, date_purchased):
    data = pd.DataFrame()
    for i in range(len(tickers)):
        stock = yf.Ticker(tickers[i])
        stock_data = stock.history(start = date_purchased[i])
        stock_data['portfolio_value'] = stock_data['Close'] * shares[i]
        data = pd.concat([data, stock_data['portfolio_value']], axis = 1)

    data['total_portfolio_value'] = data.sum(axis=1)
    fig, ax = plt.subplots(figsize=(10, 5)) # set the figsize parameter to increase the width of the plot
    ax.plot(data.index, data['total_portfolio_value'], label='Total Portfolio Value')
 
    months = MonthLocator(bymonth = [1, 4, 7, 10])
    month_format = DateFormatter('%b %Y')
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(month_format)

    month_format = DateFormatter('%b %y')
    ax.xaxis.set_major_formatter(month_format)

    return fig

st.markdown("<h1 style='text-align: center; color: black; font-size: 35px;'>Portfolio Value Over Time</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
graph = portfolio(tickers, shares, date_purchased)
st.plotly_chart(graph, use_container_width = True)

st.markdown("<h1 style='text-align: center; color: black; font-size: 35px;'>Current Holdings</h1>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3><a style='color:black;' href='https://investor.vanguard.com/investment-products/etfs/profile/voo'>Vanguard S&P 500 ETF</a></h3>", unsafe_allow_html=True)
col1, col2 = st.columns([4, 1], gap = "large")
with col1:
    st.write("""Purchasing into the S&P 500 was one of the first pieces of advice I received on investing.
             This was during an Investing 101 webinar, led by Raymond Webb who stated that your first $10,000 should go directly into the S&P 500. 
             On top of this, it was also Warren Buffet who mentioned that hardly anyone is able to consistently beat the S&P 500 index, something that still stands true to this day.
             Investing into the VOO fund, provides me with exposure to 500 biggest companies in the United States, without the need for active management.
             Something that has been constantly emphasised throughout my study in Finance, is the need for diversification.
             Ensuring that your portfolio is exposed to a diverse range of sectors and companies, shields you against unsystematic risks meaning extreme events have less of an impact on your portfolio.""")
with col2:
    st.write("""**INVESTMENT DATE**<br>September, 2022""", unsafe_allow_html=True)
    st.write("""**TICKER**<br>VOO""", unsafe_allow_html=True)
    st.write("""**INDUSTRY**<br>Software Application""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3><a style='color:black;' href='https://www.schwabassetmanagement.com/products/schd'>Schwab U.S. Dividend Equity ETF</a></h3>", unsafe_allow_html=True)
col1, col2 = st.columns([4, 1], gap = "large")
with col1:
    st.write("""Purchasing into the S&P 500 was one of the first pieces of advice I received on investing.
             This was during an Investing 101 webinar, led by Raymond Webb who stated that your first $10,000 should go directly into the S&P 500.
             On top of this, it was also Warren Buffet who mentioned that hardly anyone is able to consistently beat the S&P 500 index, something that still stands true to this day.
             Investing into the VOO fund, provides me with exposure to 500 biggest companies in the United States, without the need for active management.
             Something that has been constantly emphasised throughout my study in Finance, is the need for diversification.
             Ensuring that your portfolio is exposed to a diverse range of sectors and companies, shields you against unsystematic risks meaning extreme events have less of an impact on your portfolio.""")
with col2:
    st.write("""**INVESTMENT DATE**<br>September, 2022""", unsafe_allow_html=True)
    st.write("""**TICKER**<br>SCHD""", unsafe_allow_html=True)
    st.write("""**INDUSTRY**<br>Software Application""", unsafe_allow_html=True)


st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3><a style='color:black;' href='https://investors.coca-colacompany.com/'>Coca-Cola</a></h3>", unsafe_allow_html=True)
col1, col2 = st.columns([4, 1], gap = "large")
with col1:
    st.write("Purchasing into the S&P 500 was one of the first pieces of advice I received on investing. \
             This was during an Investing 101 webinar, led by Raymond Webb who stated that your first $10,000 should go directly into the S&P 500. \
             On top of this, it was also Warren Buffet who mentioned that hardly anyone is able to consistently beat the S&P 500 index, something that still stands true to this day.\
             Investing into the VOO fund, provides me with exposure to 500 biggest companies in the United States, without the need for active management.\
             Something that has been constantly emphasised throughout my study in Finance, is the need for diversification.\
             Ensuring that your portfolio is exposed to a diverse range of sectors and companies, shields you against unsystematic risks meaning extreme events have less of an impact on your portfolio.")
with col2:
    st.write("""**INVESTMENT DATE**<br>September, 2022""", unsafe_allow_html=True)
    st.write("""**TICKER**<br>KO""", unsafe_allow_html=True)
    st.write("""**INDUSTRY**<br>Software Application""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3><a style='color:black;' href='https://ir.tesla.com/#quarterly-disclosure'>Tesla</a></h3>", unsafe_allow_html=True)
col1, col2 = st.columns([4, 1], gap = "large")
with col1:
    st.write("Purchasing into the S&P 500 was one of the first pieces of advice I received on investing. \
             This was during an Investing 101 webinar, led by Raymond Webb who stated that your first $10,000 should go directly into the S&P 500. \
             On top of this, it was also Warren Buffet who mentioned that hardly anyone is able to consistently beat the S&P 500 index, something that still stands true to this day.\
             Investing into the VOO fund, provides me with exposure to 500 biggest companies in the United States, without the need for active management.\
             Something that has been constantly emphasised throughout my study in Finance, is the need for diversification.\
             Ensuring that your portfolio is exposed to a diverse range of sectors and companies, shields you against unsystematic risks meaning extreme events have less of an impact on your portfolio.")
with col2:
    st.write("""**INVESTMENT DATE**<br>September, 2022""", unsafe_allow_html=True)
    st.write("""**TICKER**<br>TSLA""", unsafe_allow_html=True)
    st.write("""**INDUSTRY**<br>Software Application""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3><a style='color:black;' href='https://contact.co.nz/aboutus/investor-centre'>Contact Energy</a></h3>", unsafe_allow_html=True)
col1, col2 = st.columns([4, 1], gap = "large")
with col1:
    st.write("Purchasing into the S&P 500 was one of the first pieces of advice I received on investing. \
             This was during an Investing 101 webinar, led by Raymond Webb who stated that your first $10,000 should go directly into the S&P 500. \
             On top of this, it was also Warren Buffet who mentioned that hardly anyone is able to consistently beat the S&P 500 index, something that still stands true to this day.\
             Investing into the VOO fund, provides me with exposure to 500 biggest companies in the United States, without the need for active management.\
             Something that has been constantly emphasised throughout my study in Finance, is the need for diversification.\
             Ensuring that your portfolio is exposed to a diverse range of sectors and companies, shields you against unsystematic risks meaning extreme events have less of an impact on your portfolio.")
with col2:
    st.write("""**INVESTMENT DATE**<br>September, 2022""", unsafe_allow_html=True)
    st.write("""**TICKER**<br>CEN.NZX""", unsafe_allow_html=True)
    st.write("""**INDUSTRY**<br>Software Application""", unsafe_allow_html=True)


# Retrieving information via API
def data(stock_ticker):
    profile = fa.profile(stock_ticker, API_KEY)
    prices = fa.stock_data(stock_ticker, period = "5y", interval = "1d")
    dividends = fa.stock_dividend(stock_ticker, API_KEY)
    return {
        "company_info": profile.iloc[:, 0],
        "close_price": prices["close"].sort_index(),
        "dividends": dividends
    }

stock_data = data("VOO")