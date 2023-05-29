import random
from utils import parser


dataset = parser.parse(r'Data\Kacem\Kacem1_4x5.fjs')
jobsNb = dataset.get('JobsNb')
machinesNb = dataset.get('machinesNb')
opTotal = dataset.get('opTotal')
opMachines = dataset.get('opMachines')
jobs = dataset.get('jobs')


def checkIfFits(index, individual, opJob, opNb):
    spotOpen = 0
    for i in range(index, len(individual)):
        if individual[i] == 0:
           spotOpen += 1
    if spotOpen > opJob - opNb:
        return True
    else:
        return False

def generate_individual(opTotal, opMachines, jobs):
    individual = [0] * opTotal
    lastIndex = 0
    occupiedIndex = []
    x = 1
 
    for i in range(len(jobs)):
        opJob = len(jobs[i])
        x = 1
        for j in range(len(jobs[i])):
            x = 1
            while(x == 1):
                currIndex = random.randint(0, opTotal - 1)
                currOperation = jobs[i][j][random.randint(0, opMachines - 1)]
                if individual[currIndex] == 0:
                    if currOperation != individual[currIndex]:
                        if currIndex + opJob - currOperation.get('opNb') < opTotal:
                            if lastIndex < currIndex | (lastIndex == 0 & currIndex == 0):
                                if checkIfFits(currIndex, individual, opJob, currOperation.get('opNb')) == True:
                                    individual[currIndex] = currOperation
                                    lastIndex = currIndex
                                    occupiedIndex.append(lastIndex)
                                    x = 0
        lastIndex = 0

    return individual

def generate_population(max_population, opTotal, opMachines, jobs):
    population = []

    for i in range(max_population):
        population.append(generate_individual(opTotal, opMachines, jobs))
    return population

def fitnes_function(individual):
    # Initialize variables
    job_completion_times = {}
    machine_completion_times = {}
    total_completion_time = 0

    # Iterate over each chromosome in the individual
    for chromosome in individual:
        job = chromosome['job']
        machine = chromosome['machine']
        processing_time = chromosome['processingTime']

        # Calculate the start time for the current operation
        start_time = max(job_completion_times.get(job, 0), machine_completion_times.get(machine, 0))

        # Update the completion time for the current operation
        completion_time = start_time + processing_time

        # Update the completion times for the job and machine
        job_completion_times[job] = completion_time
        machine_completion_times[machine] = completion_time

        # Update the total completion time
        total_completion_time = max(total_completion_time, completion_time)

    # Return the fitness value (inverse of the total completion time)
    fitness = 1 / total_completion_time
    return fitness

def order_crossover(parent1, parent2):
    # Select two random crossover points
    point1 = random.randint(0, len(parent1) - 2)
    point2 = random.randint(point1 + 1, len(parent1))
    
    # Create an empty child with the same length as the parents
    child = [None] * len(parent1)
    
    # Copy the selected segment from parent1 to the child
    child[point1:point2] = parent1[point1:point2]
    
    # Fill the remaining positions in the child with the values from parent2
    index = point2
    for value in parent2[point2:] + parent2[:point2]:
        if value not in child:
            child[index] = value
            index = (index + 1) % len(parent1)
    
    return child

def check_constraints(child):
    job_operations = {}  # Track the last operation number for each job
    for operation in child:
        job = operation['job']
        op_nb = operation['opNb']
        if job not in job_operations:
            job_operations[job] = 0  # Initialize last operation number for the job
        if op_nb <= job_operations[job]:
            return False  # Precedence constraint violated
        job_operations[job] = op_nb  # Update the last operation number for the job
    return True  # All precedence constraints satisfied

def keyFit():
    return 'fitScore'

def tournament_selection(population, tournament_size):
    fitnessScore = []

    # Randomly select individuals for the tournament
    tournament = random.sample(population, tournament_size)

    # Calculate fitness for each individual
    for individual in tournament:
        fitnessScore.append({'fitScore': fitnes_function(individual), 'individual': individual})
    fitnessSorted = sorted(fitnessScore, key=lambda x: x['fitScore'], reverse=True)

    # Select the top two individuals as parents
    parent1 = fitnessSorted[0].get('individual')
    parent2 = fitnessSorted[1].get('individual')

    return parent1, parent2

def swap_mutation(individual):
    # Randomly select two positions in the chromosome
    pos1 = random.randint(0, len(individual) - 1)
    pos2 = random.randint(0, len(individual) - 1)
    
    # Swap the values at the selected positions
    individual[pos1], individual[pos2] = individual[pos2], individual[pos1]
    
    return individual

def replace():

    #crossover até faltarem 2 na população
    #guarda os 2 melhores da antiga gen e troca os antigos pelos novos
    #mutation em todos
    return 

pop  = generate_population(10, opTotal, opMachines, jobs)
parents = tournament_selection(pop, 5)
child = order_crossover(parents[0], parents[1])
if check_constraints(child) == True:
    swap_mutation(child)



