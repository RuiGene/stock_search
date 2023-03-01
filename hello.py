# https://site.financialmodelingprep.com/developer/docs/
import streamlit as st
import fundamentalanalysis as fa
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta, datetime
API_KEY = '85fe259a4ec6fad3cbe55a5ddaf7f9b4'

st.set_page_config(page_title="Stocks", layout = "wide")
col1, col2, col3, col4  = st.columns([2, 0.1, 0.1, 0.5])
with col4:
    ticker = st.text_input("Ticker", help = "Enter the stock ticker here").upper() # Search bar for stock ticker

# Retrieving information via API
def data(stock_ticker):
    profile = fa.profile(ticker, API_KEY)
    prices = fa.stock_data(ticker, period = "5y", interval = "1d")
    key_metrics_annually = fa.key_metrics(ticker, API_KEY, period = 'annual')
    dividends = fa.stock_dividend(ticker, API_KEY)
    return {
        "company_info": profile.iloc[:, 0],
        "close_price": prices["close"].sort_index(),
        "key_metrics": key_metrics_annually.iloc[:, 0],
        "dividends": dividends
    }

if ticker != "":
    stock_data = data(ticker)

# Stock ticker title
with col1:
    st.title("{} ({})".format(stock_data["company_info"]["companyName"], stock_data["company_info"]["symbol"]))

st.markdown(stock_data["company_info"]["description"]) # Adding description section
# title_text = f"{stock_data['company_info']['companyName']} price"
st.markdown("""
    <style>
    .stRadio [role=radiogroup]{
        align-items: center;
        justify-content: center;
    }
    </style>
""",unsafe_allow_html=True)
options = ['1 Week', '1 Month', '3 Months', '6 Months', '1 Year', '3 Years', '5 Years']
time = st.radio(label = ' ', options = options, horizontal = True)

def convert_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d").date()
if stock_data["dividends"].empty == False:
    dividend_dates = stock_data["dividends"]["paymentDate"].values
    dividend_dates = dividend_dates[dividend_dates != ""]   
    dividend_dates = np.vectorize(convert_date)(dividend_dates)

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
    fig.update_traces(line_color = "blue", name = "Price", showlegend = True)
 
    # Add crosses for the dividend payout dates
    if stock_data["dividends"].empty == False:
        past_dates = dividend_dates[dividend_dates > start_date]
        dividend_trace = go.Scatter(
            x = past_dates,
            y = closing.loc[past_dates],
            mode = 'markers',
            marker = dict(
                symbol = 'circle',
                size = 7,
                color = 'black',
                line = dict(width = 1, color = 'black')
            ),
            name = 'Dividend Payouts'
        )
        fig.add_trace(dividend_trace)
        fig.update_layout(
            yaxis_title = "Price ($)",
            xaxis_title = "Date",
            showlegend = True
        )
        return fig
    else:
        fig.update_layout(
        yaxis_title = "Price ($)",
        xaxis_title = "Date",
        showlegend = True
        )
        return fig

closing = stock_data["close_price"]
fig = graph(closing, time)
st.plotly_chart(fig, use_container_width=True)

# Define the pre-defined values
price = '$' + str(stock_data["company_info"]["price"]) + ' ' + stock_data["company_info"]["currency"]
volume = str(f'{stock_data["company_info"]["volAvg"]:,}')
mcap = '$' + str(f'{round(stock_data["company_info"]["mktCap"]/1000000, 2):,}')  +  'M'
sector = stock_data["company_info"]["sector"]
country = stock_data["company_info"]["country"]
exchange = stock_data["company_info"]["exchangeShortName"]
industry = stock_data["company_info"]["industry"]
pe = str(round(stock_data["key_metrics"]["peRatio"], 2))
pb = str(round(stock_data["key_metrics"]["pbRatio"], 2))
eps = str(round(stock_data["key_metrics"]["netIncomePerShare"], 2))
ev_ebitda = str(round(stock_data["key_metrics"]["enterpriseValueOverEBITDA"], 2))
ev_revenue = str(round(stock_data["key_metrics"]["evToSales"], 2))
if stock_data['key_metrics']["dividendYield"] == None:
    dividend_yield = 'None'
else:
    dividend_yield = str(round(stock_data["key_metrics"]["dividendYield"], 4) * 100) + '%'
debt_to_equity = str(round(stock_data["key_metrics"]["debtToEquity"], 2))

table = {
    'Company Summary': ['Price', 'Volume', 'Market Cap', 'Sector', 'Country', 'Exchange', 'Industry'],
    'Metrics:': [price, volume, mcap, sector, country, exchange, industry],
    'Comparable Metrics': ['P/E', 'P/B', 'EPS', 'EV/EBITDA', 'EV/Revenue', 'Dividend yield', 'Debt/Equity'],
    'Values:': [pe, pb, eps, ev_ebitda, ev_revenue, dividend_yield, debt_to_equity]      
}
df2 = pd.DataFrame(table)
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
# Display a static table
st.table(df2)

if stock_data["dividends"].empty == False:
    payout = stock_data["dividends"]["adjDividend"][0:5]
    fig = go.Figure(go.Bar(x = payout.index, y = payout))
    fig.update_layout(xaxis_title = 'Date', yaxis_title = 'Payout ($)', title = {"text": "Dividend History", "x": 0.5, "xanchor": 'center'})
    st.plotly_chart(fig, use_container_width = True)