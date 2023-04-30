import streamlit as st

from predict import predict

st.title('StocksAI')

predictions_df = predict()

st.dataframe(predictions_df.to_pandas())
