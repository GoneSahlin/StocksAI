import streamlit as st
import polars as pl


st.title('StocksAI')

def make_table():
    df = pl.DataFrame({"A": [1,2,3], "B": [4,5,6]})

    return df

st.table(make_table())
