import pandas as pd
from utils import parser
from algorithm import genetic as gn
from algorithm import simulated_annealing as sa

dataset = parser.parse(r'Data\Kacem\Kacem1_4x5.fjs')
jobsNb = dataset.get('JobsNb')
machinesNb = dataset.get('machinesNb')
opTotal = dataset.get('opTotal')
opMachines = dataset.get('opMachines')
jobs = dataset.get('jobs')

def execute(parameters):
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

