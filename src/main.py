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

solution = genetic.genetic_algorithm(maxGeneration, maxPopulation, tournamentSize, opTotal, opMachines, jobs)

best_solution = solution[0]
best_score = simulated_annealing.evaluate_makespan(solution[0])
print(best_score)
initial_temp = 100.0
alpha = 0.95
max_iterations = 1000


print(simulated_annealing.simulated_annealing(best_solution, jobs,  initial_temp, alpha, max_iterations))
