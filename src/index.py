import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import parser
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


def create_gantt(result):
    df = pd.DataFrame(result)
    # Ordenar o DataFrame pela coluna 'opNb' para criar a sequência correta das tarefas
    df = df.sort_values('opNb')

    # Calcular as datas de início e fim com base no tempo de processamento (processingTime)
    df['Início'] = df.groupby('job')['processingTime'].cumsum() - df['processingTime']
    df['Fim'] = df.groupby('job')['processingTime'].cumsum()

    fig = px.timeline(df, x_start='Início', x_end='Fim', y='job', color='machine', title='Gráfico de Gantt - FJSP')
    fig.update_layout(yaxis={'title': 'Job'})
    fig.update_xaxes(title='Tempo')
    fig.show()

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
    st.text(sa_solution[0])

    st.subheader('Makespan:')
    st.text(sa_solution[1])

    df_result = pd.DataFrame(sa_solution[0])

    # Ordenar o DataFrame pela coluna 'opNb' para criar a sequência correta das tarefas
    df_result = df_result.sort_values('opNb')

    # Criar uma lista com as cores para cada job
    job_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    # Criar uma lista com as máquinas presentes no DataFrame
    machines = sorted(df_result['machine'].unique())

    # Criar uma lista com as operações de cada máquina
    machine_operations = []
    for machine in machines:
        machine_df = df_result[df_result['machine'] == machine]
        operations = []
        start_time = 0
        for index, row in machine_df.iterrows():
            operation = {
                'Task': row['machine'],
                'Start': start_time,
                'Finish': start_time + row['processingTime'],
                'Description': f"Job {row['job']}",
                'Resource': f"Job {row['job']}",
                'Color': job_colors[row['job'] - 1]
            }
            operations.append(operation)
            start_time += row['processingTime']
        machine_operations.append(operations)

        # Configurar o gráfico de Gantt
        fig = go.Figure()

        for machine, operations in zip(machines, machine_operations):
            fig.add_trace(go.Bar(
                y=[machine] * len(operations),
                x=[operation['Start'] for operation in operations],
                width=[operation['Finish'] - operation['Start'] for operation in operations],
                base=[machine] * len(operations),
                orientation='h',
                text=[operation['Description'] for operation in operations],
                hovertemplate='Máquina: %{y}<br>' +
                            'Job: %{text}<br>' +
                            'Início: %{x}<br>' +
                            'Término: %{x + width}<br>',
                marker=dict(color=[operation['Color'] for operation in operations]),
                showlegend=False
            ))

        fig.update_layout(
            title='Gráfico de Gantt',
            yaxis=dict(title='Máquinas'),
            xaxis=dict(title='Tempo'),
            barmode='stack',
            height=400
        )

        # Exibir o gráfico de Gantt no Streamlit
        st.plotly_chart(fig, use_container_width=True)
                

