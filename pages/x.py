import streamlit as st
import fundamentalanalysis as fa
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import date, timedelta
API_KEY = '85fe259a4ec6fad3cbe55a5ddaf7f9b4'

st.set_page_config(page_title="Stocks", layout="wide")
col1, col2, col3, col4  = st.columns([2, 0.1, 0.1, 0.5])
with col4:
    ticker = st.text_input("Ticker", help = "Enter the stock ticker here").upper() # Search bar for stock ticker

# Retrieving information via API
def data(stock_ticker):
    profile = fa.profile(ticker, API_KEY)
    prices = fa.stock_data(ticker, period = "5y", interval = "1d")
    return {
        "company_info": profile.iloc[:, 0],
        "close_price": prices["close"].sort_index()
    }

if ticker != "":
    stock_data = data(ticker)

# Stock ticker title
with col1:
    st.title("{} ({})".format(stock_data["company_info"]["companyName"], stock_data["company_info"]["symbol"]))

st.markdown(stock_data["company_info"]["description"]) # Adding description section
# title_text = f"{stock_data['company_info']['companyName']} price"
time = st.radio(label = ' ', options = ('1 Week', '1 Month', '3 Months', '6 Months', '1 Year', '3 Years', '5 Years'), horizontal = True)

def graph(closing, time_frame):
    today = date.today()
    if time_frame == '1 Week':
        start_date = today - timedelta(days = 7)
    elif time_frame == '1 Month':
        start_date = today - timedelta(days = 30)
    elif time_frame == '3 Months':
        start_date = today - timedelta(days = 90)
    elif time_frame == '6 Months':
        start_date = today - timedelta(days = 180)
    elif time_frame == '1 Year':
        start_date = today - timedelta(days = 365)
    elif time_frame == '3 Years':
        start_date = today - timedelta(days = 1095)
    elif time_frame == '5 Years':
        start_date = today - timedelta(days = 1825)
    else:
        raise ValueError("Invalid time frame")
    fig = px.line(x= closing[start_date:today].index, y = closing.loc[start_date:today])
    fig.update_layout(
        yaxis_title = "Price ($)",
        xaxis_title = "Date"
    )
    return fig

closing = stock_data["close_price"]
fig = graph(closing, time)
st.plotly_chart(fig, use_container_width=True)

sec1, sec2 = st.columns(2)



# Define the pre-defined values
price = '$' + str(stock_data["company_info"]["price"]) + stock_data["company_info"]["currency"]
volume = str(f'{stock_data["company_info"]["volAvg"]:,}')
mcap = str(stock_data["company_info"]["mktCap"])
sector = stock_data["company_info"]["sector"]
country = stock_data["company_info"]["country"]
exchange = stock_data["company_info"]["exchangeShortName"]
industry = stock_data["company_info"]["industry"]

# Define the data as a dictionary with the columns as keys
data = {
    'Metric': ['Price', 'Volume', 'Market Cap', 'Sector', 'Country', 'Exchange', 'Industry'],
    'Value': [price, volume, mcap, sector, country, exchange, industry]
}

# Create a pandas dataframe from the dictionary
df = pd.DataFrame(data)

# Display the dataframe in Streamlit without the index column
st.write(df.set_index('Metric'), index=False)