import random
from utils import parser


dataset = parser.parse(r'Data\Kacem\Kacem1_4x5.fjs')
jobsNb = dataset.get('JobsNb')
machinesNb = dataset.get('machinesNb')
opTotal = dataset.get('opTotal')
op_machines = dataset.get('op_machines')
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

def generate_individual(opTotal, op_machines, jobs):
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
                currOperation = jobs[i][j][random.randint(0, op_machines - 1)]
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

generate_individual(opTotal, op_machines, jobs)


def generate_population(max_population, machinesNb, jobs):
    population = []

    for i in range(max_population):
        population.append(generate_individual(machinesNb, jobs))
    return population

def keyJob(e):
    return e['job']

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
    individual.append({'fitness': fitness})
    return fitness

def crossover(parent1, parent2):
    # Select a random crossover point
    crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 1)

    # Perform the crossover
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    return child1, child2

def tournament_selection(population, tournament_size):
    # Randomly select individuals for the tournament
    tournament = random.sample(population, tournament_size)

    # Calculate fitness for each individual
    for individual in tournament:
        fitnes_function(individual)
        
    # Sort the tournament individuals by their fitness values
    tournament.sort(key=lambda individual: individual[len(individual) - 1]['fitness'], reverse=True)

    # Select the top two individuals as parents
    parent1 = tournament[0]
    parent2 = tournament[1]

    return parent1, parent2


def swap_mutation(individual):
    # Randomly select two positions in the chromosome
    pos1 = random.randint(0, len(individual) - 1)
    pos2 = random.randint(0, len(individual) - 1)
    
    # Swap the values at the selected positions
    individual[pos1], individual[pos2] = individual[pos2], individual[pos1]
    
    return individual






