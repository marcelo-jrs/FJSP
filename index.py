import streamlit as st
import pandas as pd
from utils import parser
from utils import gantt
from services import db
import algorithm.genetic as gn
import algorithm.simulated_annealing as sa


st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(page_title='Algoritmo Híbrido', page_icon='dna_icon.png', layout="wide", initial_sidebar_state="auto", menu_items={'About': 'Este é um sistema web que fornece um algoritmo híbrido entre algoritmo genético e simulated annealing, desenvolvido por: Marcelo Júnior, em parceria com o NPI - Núcleo de Prática de Informática da Unifil Londrina'})

st.write("""
# Funcionamento de um algoritmo híbrido entre Algoritmo genético e Simulated annealing no domínio FJSP
""")


def user_input_features():
    st.sidebar.subheader('Autor')
    autor = st.sidebar.text_input(label='', label_visibility='collapsed')
    st.sidebar.subheader('Dataset')
    dataset = st.sidebar.selectbox(label='',options=['Kacem 4x5', 'Kacem 10x7'], label_visibility='collapsed')
    st.sidebar.subheader('Parâmetros para o algoritmo genético')
    max_population = st.sidebar.slider('Indivíduos por população', 1, 100, 20)
    max_generation = st.sidebar.slider('Máximo de gerações', 1, 1000, 100)
    tournament_size = st.sidebar.slider('Indivíduos por torneio', 1, max_population, 10)
    st.sidebar.subheader('Parâmetros para o simulated annealing')
    initial_temp = st.sidebar.slider('Temperatura inicial', 100, 2000, 1000)
    alpha = st.sidebar.slider('Parâmetro de redução', 0.0, 1.0, 0.8)
    max_iterations = st.sidebar.slider('Máximo de Iterações', 0, 3000, 1000)
    parameters = {'max_population': max_population,
            'max_generation': max_generation,
            'tournament_size': tournament_size,
            'initial_temp': initial_temp,
            'alpha': alpha,
            'max_iterations': max_iterations}
    return parameters, dataset, autor

def execute(parameters, dataset, autor):
    if dataset == 1:
        data = parser.parse(r"data\Kacem1_4x5.fjs")
    elif dataset == 2:
        data = parser.parse(r"data\Kacem2_10x7.fjs")
    else:
        raise Exception("Dataset inválido") 
    jobsNb = data.get('JobsNb')
    machinesNb = data.get('machinesNb')
    opTotal = data.get('opTotal')
    opMachines = data.get('opMachines')
    jobs = data.get('jobs')

    max_population = parameters.get('max_population')
    max_generation = parameters.get('max_generation')
    tournament_size = parameters.get('tournament_size')
    initial_temp = parameters.get('initial_temp')
    alpha = parameters.get('alpha')
    max_iterations = parameters.get('max_iterations')
    
    id_instance = db.insert_instance(autor, dataset, max_population, max_generation, tournament_size, initial_temp, alpha, max_iterations)

    results_gn = gn.genetic_algorithm(max_generation, max_population, tournament_size, opTotal, opMachines, jobs, machinesNb)
    solution = results_gn[0]

    results_sa = sa.simulated_annealing(solution, jobs, initial_temp, alpha, max_iterations, machinesNb)

    data = results_sa[0]

    id_result = db.insert_result(id_instance, results_sa[1])
    op = db.insert_operation(id_result, data)

    return results_gn, results_sa

parameters, dataset, autor = user_input_features()

st.subheader('Parâmetros do usuário')
df = pd.DataFrame(parameters, index=[0])
st.dataframe(
    df,
    column_config={
        "max_population": st.column_config.Column("Indivíduos por população"),
        "max_generation":st.column_config.Column("Máximo de gerações"),
        "tournament_size": st.column_config.Column("Tamanho do torneio"),
        "initial_temp": st.column_config.Column("Temperatura inicial"),
        "alpha": st.column_config.Column("Parâmetro de redução de temp. (alpha)"),
        "max_iterations": st.column_config.Column("Máximo de iterações"),
    },
    hide_index=True,
    height=40
)

clicked = st.button('START')
if clicked:
    if dataset == 'Kacem 4x5': dataset = 1
    if dataset == 'Kacem 10x7': dataset = 2
    results = execute(parameters, dataset, autor)
    results_gn = results[0]
    sa_solution = results[1]
    sa_score = results[1][1]

    with st.container():
        st.subheader('Solução gerada:')
        st.dataframe(sa_solution[0], width=500, height=450)

        st.subheader('Makespan GA: {x}'.format(x = sa.evaluate_makespan(results_gn[0])))
        st.subheader('Makespan SA: {x}'.format(x = sa_solution[1]))

        st.subheader('Gráfico de Gantt')
        st.pyplot(gantt.plot_gantt_chart(sa_solution[0]))