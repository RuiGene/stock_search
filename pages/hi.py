import streamlit as st
import pandas as pd

# create a DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
})

# display the DataFrame in a table that takes up the full width of the container
st.table(df, use_container_width=True)