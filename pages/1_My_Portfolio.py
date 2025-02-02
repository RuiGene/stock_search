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
from matplotlib.dates import MonthLocator, DateFormatter, YearLocator
from matplotlib import ticker
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()
API_KEY = os.getenv('API_KEY')

st.set_page_config(page_title="Portfolio", layout = "wide", page_icon = '🏦')

def portfolio():
    # Reading in transactional data
    conn = sqlite3.connect("stock_transactions.db")
    query = "SELECT * FROM stock_transactions"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Data cleaning
    df['date'] = pd.to_datetime(df['date'])
    df["date"] = df["date"].dt.tz_localize("America/New_York")

    current_holdings_shares = []
    current_holdings = []

    # Initialising dataframe
    data = pd.DataFrame(columns = ['total_portfolio_value', 'cash_balance'])

    for i in range(len(df)):
        if df['ticker'][i] not in current_holdings:
            current_holdings.append(df['ticker'][i])
            stock = yf.Ticker(df['ticker'][i])
            stock_data = stock.history(start = df['date'][i])
            data[df['ticker'][i]] = stock_data['Close'] * df['units'][i]
        
        else:
            stock = yf.Ticker(df['ticker'][i])
            stock_data = stock.history(start = df['date'][i])
            temp_data = pd.DataFrame()
            if df['action'][i] == 'Buy':
                temp_data[df['ticker'][i]] = stock_data['Close']*df['units'][i]
            else: 
                temp_data[df['ticker'][i]] = stock_data['Close']*df['units'][i]*-1

            data = pd.merge(data, temp_data, left_index=True, right_index=True, how="outer", suffixes = ('_df1', '_df2'))
            data.fillna(0, inplace=True)
            data[df['ticker'][i]] = data[df['ticker'][i] + '_df1'] + data[df['ticker'][i] + '_df2']
            data = data.drop(columns = [df['ticker'][i] + '_df1', df['ticker'][i] + '_df2'])

    data.fillna(0, inplace = True)

    data['total_portfolio_value'] = data.sum(axis=1)

    # Adding cash balance
    for i in range(len(df)):
        cash_to_add = round(df['units'][i] * df['price'][i], 2)
        if df['action'][i] == 'Sell':
            cash_to_add = cash_to_add * -1
        data.loc[data.index >= df['date'][i], "cash_balance"] += cash_to_add

    fig, ax = plt.subplots(figsize=(10, 5)) # set the figsize parameter to increase the width of the plot
    ax.plot(data.index, data['total_portfolio_value'], label='Total Portfolio Value')
    ax.plot(data.index, data['cash_balance'], linestyle='--', color='black', label='Cash Balance')

    # set the x-axis tick locator and formatter to show only the years
    years = YearLocator()
    year_format = DateFormatter('%Y')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(year_format)

    ax.set_xlabel("Date")
    ax.set_ylabel("Value ($)")
    ax.set_title("Portfolio Value Over Time")
    ax.legend()

    return fig

st.markdown("<h1 style='text-align: center; color: black; font-size: 35px;'>Portfolio Value Over Time</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
graph = portfolio()
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
    st.write("""**INVESTMENT DATE**<br>August, 2022""", unsafe_allow_html=True)
    st.write("""**TICKER**<br>VOO""", unsafe_allow_html=True)
    st.write("""**INDUSTRY**<br>Fund""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3><a style='color:black;' href='https://www.schwabassetmanagement.com/products/schd'>Schwab U.S. Dividend Equity ETF</a></h3>", unsafe_allow_html=True)
col1, col2 = st.columns([4, 1], gap = "large")
with col1:
    st.write("""Dividends are something that I personally value, as that consistent stream of cash flow is something that is quite undervalued.\
    Purchasing into a dividend ETF was one of my first priorities, as not only would it have capital appreciation it would also come along with quarterly payments.\
    It was hard to decide which dividend fund to invest in but the SCHD fund caught my way due to the continous praise from people on the r/Dividends subreddit.\
    After conducting my own research, I decided to choose SCHD due to its low cost and choice of reputable companies within its portfolio. Within its fund, \
    it consists of companies that have proven to have a reliable dividend track record, with many belonging to the Dividend Aristocrats selection, which are companies within \
    the S&P500 index that have increased and paid their base dividend for at least 25 consecutive years.""")
with col2:
    st.write("""**INVESTMENT DATE**<br>December, 2022""", unsafe_allow_html=True)
    st.write("""**TICKER**<br>SCHD""", unsafe_allow_html=True)
    st.write("""**INDUSTRY**<br>Fund""", unsafe_allow_html=True)


st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3><a style='color:black;' href='https://investors.coca-colacompany.com/'>Coca-Cola</a></h3>", unsafe_allow_html=True)
col1, col2 = st.columns([4, 1], gap = "large")
with col1:
    st.write("""My first piece of investment advice was "invest in a company that you use". This is a piece of advice that has stuck with me and is what I applied here \
    as my choice for investing into Coca Cola. Admittedly so, I am a huge soft drink fan. If I'm out and about, most times I will have a coke, whether it be alongside lunch or dinner.\
    This is when I thought to myself, if I purchase so much of their product, why not purchase into their stock? Coca cola not only has the potential for capital appreciation, \
    it is also a company that pays an consistent, steady dividend. With a huge range of brands under its belt, it has created itself a well diversified portfolio. Coca cola \
    is also exposed to growth markets such as Africa and Asia and with such a strong brand identity and loyalty, it is an investment that can't be passed up.""")
with col2:
    st.write("""**INVESTMENT DATE**<br>March, 2023""", unsafe_allow_html=True)
    st.write("""**TICKER**<br>KO""", unsafe_allow_html=True)
    st.write("""**INDUSTRY**<br>Beverages""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3><a style='color:black;' href='https://ir.tesla.com/#quarterly-disclosure'>Tesla</a></h3>", unsafe_allow_html=True)
col1, col2 = st.columns([4, 1], gap = "large")
with col1:
    st.write("""Many would consider Tesla, a meme stock, something that is heavily influenced by whatever Elon decides to post on a random Wednesday.\
        Although this is true, I believe that Tesla is definitely a long term hold. It has strong brand loyalty and a well established presence within the \
            EV industry. My thesis behind investing in Tesla, rests on the ever increasing demand for EVs. With new laws coming into place, more and more pressure \
                is going to be put onto transitioning from petrol based vehicles to EVs. With such a huge market share, this is something Tesla can capitalise on. \
                    Another reason, is for Teslas impressive free cash flow, something that many automoblie companies don't have. """)
with col2:
    st.write("""**INVESTMENT DATE**<br>March, 2022""", unsafe_allow_html=True)
    st.write("""**TICKER**<br>TSLA""", unsafe_allow_html=True)
    st.write("""**INDUSTRY**<br>Automotive and Energy""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3><a style='color:black;' href='https://contact.co.nz/aboutus/investor-centre'>Contact Energy</a></h3>", unsafe_allow_html=True)
col1, col2 = st.columns([4, 1], gap = "large")
with col1:
    st.write("Contact Energy was the first company that I pitched as a Junior Equity Analyst at the University of Auckland Investment Commmittee.\
             Contact is the 2nd largest electricity generator and retailer in New Zealand. Electricity is a necessity of life, and with high barriers to entry for generation, Contact provides a defensive investment opportunity.\
             It also has a strong dividend yield, one that has been consistent for many years now, something that I personally value. Growth tailwinds include expanding energy demand (introducing EVs) and population increase. \
             Contact displays superior financial performance relative to its industry peers. With their new Tauhara Power Station project underway,\
              Contact proves itself as the leader in low-cost geothermal renewables and takes advantage of decarbonisation demands.")
with col2:
    st.write("""**INVESTMENT DATE**<br>January, 2023""", unsafe_allow_html=True)
    st.write("""**TICKER**<br>CEN.NZX""", unsafe_allow_html=True)
    st.write("""**INDUSTRY**<br>Energy""", unsafe_allow_html=True)