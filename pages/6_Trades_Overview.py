import streamlit as st
import sqlite3
import pandas as pd
from helper_functions import calculate_total_value

st.set_page_config(page_title="Trades Overview", layout = "wide", page_icon = '🔎')

st.title("Stock Trade Overview")

def fetch_data_from_db(table_name):
    conn = sqlite3.connect(f"{table_name}.db")
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

stock_df = fetch_data_from_db('stock_transactions')
stock_df = stock_df.drop(columns=['id'])
column_config = {
    'date': 'Date:',
    'ticker': 'Ticker:',
    'units': 'Units:',
    'price': 'Price:',
    'action': 'Action:',
    'total_value': 'Total Value:'
}
data_placeholder = st.empty()
data_placeholder.data_editor(stock_df, use_container_width=True, hide_index=True, disabled=True, column_config=column_config)

st.header("Insert Data")
date_input = st.date_input("Date of Transaction:", value = None, format = 'DD/MM/YYYY')
ticker = st.text_input('Ticker Symbol:', value = None)
units = st.number_input("Number of Units:", value = None, placeholder = "E.g 1 or 2")
price = st.number_input("Price of Unit:", value = None, placeholder = "E.g. 1.9 or 1.2")
action = st.selectbox("Action:", ("Buy", "Sell"))

if st.button("Add Transaction"):
    total_value = calculate_total_value(units, price, action)
    connection = sqlite3.connect('stock_transactions.db')
    cursor_obj = connection.cursor()
    try:
        cursor_obj.execute(
            """
                INSERT INTO STOCK_TRANSACTIONS (date, ticker, units, price, action, total_value)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
            (date_input, ticker, units, price, action, total_value)
        )
        connection.commit()
        st.success("Transaction added successfully")

        stock_df = fetch_data_from_db('stock_transactions')
        stock_df = stock_df.drop(columns=['id'])

        # Display the updated DataFrame
        data_placeholder.data_editor(stock_df, use_container_width=True, hide_index=True, disabled=True, column_config=column_config)

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display stock transactions table
# try:
#     transactions_data = fetch_data_from_db("stock_transactions")

#     # Drop the 'id' column to hide it
#     if 'id' in transactions_data.columns:
#         transactions_data = transactions_data.drop(columns=['id'])

#     transactions_data['total_value'] = transactions_data['units'] * transactions_data['price']

#     # Editable data editor
#     edited_data = st.data_editor(
#         transactions_data,
#         use_container_width=True,
#         disabled=False,  # Enable editing for all columns
#         hide_index=True,  # Hide the DataFrame's index
#         num_rows="dynamic",  # Allow dynamic row resizing
#         column_config = {
#             'date': st.column_config.DateColumn(
#                 'Date',
#                 format = 'YYYY-MM-DD'
#             ),
#             'buy_sell': st.column_config.SelectboxColumn(
#                 'Action',
#                 options = [
#                     'buy',
#                     'sell'
#                 ],
#                 required = True
#             )
#         }
#     )

#     # Add a button to submit changes
#     if st.button("Submit DataFrame"):
#         update_database("stock_transactions", edited_data)
#         st.success("Database updated successfully!")
# except Exception as e:
#     st.error(f"Error fetching transactions data: {e}")

st.title("Crypto Trade Overview")