from utils import parser
import streamlit as st



parameters = parser.parse(r'Data\Brandimarte_Data\Text\Mk01.fjs')
st.dataframe(parameters)

print(parameters)