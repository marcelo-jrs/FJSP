import random
from utils import parser


dataset = parser.parse(r'Data\Kacem\Kacem1_4x5.fjs')
jobsNb = dataset.get('JobsNb')
machinesNb = dataset.get('machinesNb')
jobs = dataset.get('jobs')



def generate_chromossome(machinesNb, jobs):
    chromossome = []
    jobNb = 0
    proc_time = 0
    x = 0

    random.shuffle(jobs)

    for job in jobs:
        for operation in job:
            counter = len(operation)
            machine = operation[random.randint(0, counter - 1)].get('machine', random.randint(1, machinesNb))
            for i in operation:
                machine_proc = i.get('machine') 
                if machine_proc == machine:
                    proc_time = i.get('processingTime')
                    jobNb = i.get('job')
                    chromossome.append({'job': jobNb ,'machine': machine, 'processingTime': proc_time})            
        
    return chromossome

def generate_population(max_population, machinesNb, jobs):
    population = []

    for i in range(max_population):
        population.append(generate_chromossome(machinesNb, jobs))
    return population

def keyJob(e):
    return e['job']


def fitnes_function(chromossome):
    # Initialize variables
    job_completion_times = {}
    machine_completion_times = {}
    total_completion_time = 0

    # Iterate over each gene in the chromosome
    for gene in chromossome:
        job = gene['job']
        machine = gene['machine']
        processing_time = gene['processingTime']

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
        fitness = fitnes_function(individual)
        individual.append({'fitness': fitness})
        
    # Sort the tournament individuals by their fitness values
    tournament.sort(key=lambda individual: individual['fitness'], reverse=True)

    # Select the top two individuals as parents
    parent1 = tournament[0]
    parent2 = tournament[1]

    return parent1, parent2


pop = generate_population(10, machinesNb, jobs)

for chromossome in pop:
    fitnes_function(chromossome)

print(tournament_selection(pop,5))




