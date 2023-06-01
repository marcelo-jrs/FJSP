from utils import parser
from algorithm import genetic
from algorithm import simulated_annealing


dataset = parser.parse(r'Data\Kacem\Kacem1_4x5.fjs')
jobsNb = dataset.get('JobsNb')
machinesNb = dataset.get('machinesNb')
opTotal = dataset.get('opTotal')
opMachines = dataset.get('opMachines')
jobs = dataset.get('jobs')

maxPopulation = 10
maxGeneration = 100
tournamentSize = 5
generation = 0

population = genetic.generate_population(maxPopulation, opTotal, opMachines, jobs)
currSolution = population[0]
# Executar o algoritmo genético
for generation in range(100):
    # Avaliar a aptidão de cada indivíduo na população
    
    fitness_scores = []
    for individual in population:
        fitness = genetic.fitnes_function(individual)
        fitness_scores.append({'fitScore': fitness, 'individual': individual})

    # Selecionar os pais para reprodução
    parent1, parent2 = genetic.tournament_selection(population, tournamentSize)

    if genetic.fitnes_function(currSolution) < genetic.fitnes_function(parent1):
        currSolution = parent1

    counter = 0
    while len(population) > counter:
        # Aplicar crossover
        child = genetic.order_crossover(parent1, parent2)

        # Verificar as restrições do filho gerado
        if genetic.check_constraints(child):
            # Substituir um indivíduo na população pelo filho gerado
            population = genetic.replace(population, child)
            counter += 1

    # Aplicar mutação

# Obter a melhor solução da população final
best_solution = max(population, key=lambda x: genetic.fitnes_function(x))

print(genetic.fitnes_function(best_solution))
print(genetic.fitnes_function(currSolution))
