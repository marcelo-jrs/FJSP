from utils import parser
import streamlit as st

import streamlit as st

st.set_page_config(
    page_title="Algoritmo Genético",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Esta página tem o intuito de receber os parâmetros para rodar o algoritmo genético!"
    }
)

st.title('Algoritmo Genético')

with st.form('parameters'):
    maxPopulation = st.number_input("Número de indivíduos em uma população")
    maxGeneration = st.number_input("Número máximo de gerações")
    torunamentSize = st.number_input("Número de indivíduos por torneio")

    submitted = st.form_submit_button("Submit")