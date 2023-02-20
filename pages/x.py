import streamlit as st
import fundamentalanalysis as fa
API_KEY = '85fe259a4ec6fad3cbe55a5ddaf7f9b4'

st.set_page_config(page_title="Stocks", layout="wide")
col1, col2, col3, col4  = st.columns([2, 0.1, 0.1, 0.3])


with col4:
    ticker = st.text_input("Ticker", help = "Enter the stock ticker here").upper()

def data(stock_ticker):
    profile = fa.profile(ticker, API_KEY)

    return {
        "company_info": profile.iloc[:, 0]
    }

if ticker != "":
    stock_data = data(ticker)

with col1:
    # enter stock ticker title here
    st.title("{} ({})".format(stock_data["company_info"]["companyName"], stock_data["company_info"]["symbol"]))

st.markdown(stock_data["company_info"]["description"])

# to do list:
# Widen the title for large company names
# company overview under title

