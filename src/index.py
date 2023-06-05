import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import parser
from utils import gantt
import algorithm.genetic as gn
import algorithm.simulated_annealing as sa

st.write("""
# Funcionamento de um algoritmo híbrido entre Algoritmo genético e Simulated annealing no domínio FJSP
""")

st.sidebar.header('User Input Parameters')

def user_input_features():
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
    return parameters

def execute(parameters):
    data = parser.parse(r"Kacem1_4x5.fjs")
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

    results_gn = gn.genetic_algorithm(max_generation, max_population, tournament_size, opTotal, opMachines, jobs)
    solution = results_gn[0]

    results_sa = sa.simulated_annealing(solution, jobs, initial_temp, alpha, max_iterations)

    return results_gn, results_sa

parameters = user_input_features()

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
)

clicked = st.button('START')
if clicked:
    results = execute(parameters)
    sa_solution = results[1]
    sa_score = results[1][1]

    st.subheader('Solução gerada:')
    st.dataframe(sa_solution[0])

    st.subheader('Makespan:')
    st.text(sa_solution[1])

    st.pyplot(gantt.plot_gantt_chart(sa_solution[0]))