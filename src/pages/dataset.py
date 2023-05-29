import streamlit as st

st.set_page_config(
    page_title="Dataset",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={

    }
)

Kacem4x5 = 'Data\Kacem\Kacem1_4x5.fjs'
Kacem10x7 = 'Data\Kacem\Kacem2_10x7.fjs'
Dauzere1 = 'Data\Dauzere_Data\Text\01a.fjs'
Dauzere2 = 'Data\Dauzere_Data\Text\02a.fjs'
Dauzere3 = 'Data\Dauzere_Data\Text\03a.fjs'
Dauzere4 = 'Data\Dauzere_Data\Text\04a.fjs'
Dauzere5 = 'Data\Dauzere_Data\Text\05a.fjs'
Dauzere6 = 'Data\Dauzere_Data\Text\06a.fjs'
Dauzere7 = 'Data\Dauzere_Data\Text\07a.fjs'
Dauzere8 = 'Data\Dauzere_Data\Text\08a.fjs'
Dauzere9 = 'Data\Dauzere_Data\Text\09a.fjs'
Dauzere10 = 'Data\Dauzere_Data\Text\010a.fjs'
Dauzere11 = 'Data\Dauzere_Data\Text\011a.fjs'
Dauzere12 = 'Data\Dauzere_Data\Text\012a.fjs'
Dauzere13 = 'Data\Dauzere_Data\Text\013a.fjs'
Dauzere14 = 'Data\Dauzere_Data\Text\014a.fjs'
Dauzere15 = 'Data\Dauzere_Data\Text\015a.fjs'
Dauzere16 = 'Data\Dauzere_Data\Text\016a.fjs'
Dauzere17 = 'Data\Dauzere_Data\Text\017a.fjs'
Dauzere18 = 'Data\Dauzere_Data\Text\018a.fjs'

with st.form('dataset'):
    datasetAuthor = st.selectbox("Escolha o autor do dataset", ['Kacem', 'Dauzere'])
    if datasetAuthor == 'Kacem':
        dataset = st.selectbox("", ['4x5', '10x7'])
    elif datasetAuthor == 'Dauzere':
        dataset = st.selectbox("", ['01', '02', '03', '04', '05', '06'])
    submitted = st.form_submit_button("Submit")