import streamlit as st
import sys

sys.path.insert(0, "../../utils/") 

from predict import predict

st.title('StocksAI')

predictions_df = predict()

st.dataframe(predictions_df.to_pandas())
