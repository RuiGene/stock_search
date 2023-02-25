import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import fundamentalanalysis as fa
from datetime import datetime
FA_API_KEY = '85fe259a4ec6fad3cbe55a5ddaf7f9b4'

st.set_page_config(page_title="Stock searcher", layout="wide")
ticker = st.columns(4)[0].text_input("Ticker")

TIME_DIFFS = {
    "1 week": pd.DateOffset(weeks=1),
    "1 month": pd.DateOffset(months=1),
    "3 months": pd.DateOffset(months=3),
    "1 year": pd.DateOffset(years=1),
    "3 years": pd.DateOffset(years=3),
    "5 years": pd.DateOffset(years=5)
}


# save for 3 hours
@st.cache(ttl=60*60*3)
def load_data(ticker):
    # load data
    profile = fa.profile(ticker, FA_API_KEY)
    key_metrics_annually = fa.key_metrics(ticker, FA_API_KEY, period="annual")
    stock_data = fa.stock_data(ticker, period="5y", interval="1d")
    financial_ratios_annually = fa.financial_ratios(ticker, FA_API_KEY, period="annual")
    income_statement_annually = fa.income_statement(ticker, FA_API_KEY, period="annual")
    try:
        dividends = fa.stock_dividend(ticker, FA_API_KEY)
        dividends.index = pd.to_datetime(dividends.index)
        dividends = dividends["adjDividend"].resample("1Y").sum().sort_index()
    except:
        dividends = pd.Series(0, name="Dividends")

    # return information of interest
    return {
        "stock_closings": stock_data["close"].sort_index(),
        "historical_PE": key_metrics_annually.loc["peRatio"].sort_index(),
        "payout_ratio": financial_ratios_annually.loc["payoutRatio"].sort_index(),
        "dividend_yield": 100*financial_ratios_annually.loc["dividendYield"].sort_index(),
        "cash_per_share": key_metrics_annually.loc["cashPerShare"].sort_index(),
        "debt_to_equity": key_metrics_annually.loc["debtToEquity"].sort_index(),
        "free_cash_flow_per_share": key_metrics_annually.loc["freeCashFlowPerShare"].sort_index(),
        "dividends": dividends,
        "earnings_per_share": income_statement_annually.loc["eps"].sort_index(),
        "info": profile.iloc[:, 0]
    }

if ticker != "":
    stock_data = load_data(ticker)

info = stock_data["info"]
currency = info["currency"]

# Add changes for different periods
close = stock_data["stock_closings"]
latest_price = close.iloc[-1]
# should all be displayed on the same row
change_columns = st.columns(len(TIME_DIFFS))
today = pd.to_datetime("today").floor("D")
for i, (name, difference) in enumerate(TIME_DIFFS.items()):
    # go back to the date <difference> ago
    date = (today - difference)
    # if there is no data back then, then use the earliest
    if date < close.index[0]:
        date = close.index[0]
    # if no match, get the date closest to it back in time, e.g. weekend to friday
    previous_price = close.iloc[close.index.get_loc(date,method='ffill')]
    # calculate change in percent
    change = 100*(latest_price - previous_price) / previous_price
    # show red if negative, green if positive
    color = "red" if change < 0 else "green"

    # color can be displayed as :red[this will be red] in markdown
    change_columns[i].markdown(f"{name}: :{color}[{round(change, 2)}%]")

overview_columns = st.columns([1, 3])

overview_columns[0].markdown("<br/>"*4, unsafe_allow_html=True)
# text will be displayed and key is the key in info
for text, key in [
    ("Current price", "price"),
    ("Country", "country"),
    ("Exchange", "exchange"),
    ("Sector", "sector"),
    ("Industry", "industry"),
    ("Full time employees", "fullTimeEmployees")
]:
    overview_columns[0].markdown("")
    overview_columns[0].markdown(f"- {text}: **{info[key]}**")

graph_placeholder = overview_columns[1].empty()
graph_placeholder.plotly_chart(go.Figure(), use_container_width=True)

# options that will dictate the graph:

# radio buttons for what time window to display the stock price
time_window_key = overview_columns[1].radio("Time window", TIME_DIFFS.keys(), index=len(TIME_DIFFS)-1, horizontal=True)
# select the value from the key, i.e. the pd.DateOffset
time_window = TIME_DIFFS[time_window_key]

# slider to select the moving average to display in the graph
moving_average = overview_columns[1].slider("Moving average", min_value=2, max_value=500, value=30)

# Use above to construct the graph:

def get_price_data_fig(srs, moving_average, time_window, currency):
    # create moving average
    ma = srs.rolling(window=moving_average).mean().dropna()
    # only in time window
    start = (pd.to_datetime("today").floor("D") - time_window)
    srs = srs.loc[start:]
    ma = ma.loc[start:]
    # create figures for normal and moving average
    fig1 = px.line(y=srs, x=srs.index)
    fig1.update_traces(line_color="blue", name="Price", showlegend=True)
    fig2 = px.line(y=ma, x=ma.index)
    fig2.update_traces(line_color="orange", name=f"Moving average price ({moving_average})", showlegend=True)
    # combine and add layout
    fig = go.Figure(data = fig1.data + fig2.data)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=currency,
        title_x = 0.5,
        # align labels top-left, side-by-side
        legend=dict(y=1.1, x=0, orientation="h"),
        showlegend=True
    )
    return fig

# show the graph
fig = get_price_data_fig(stock_data["stock_closings"], moving_average, time_window, time_window_key, currency)
# add to placeholder to be displayed before options
graph_placeholder.plotly_chart(fig, use_container_width=True)