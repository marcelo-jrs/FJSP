import random
from utils import parser


dataset = parser.parse(r'Data\Kacem\Kacem1_4x5.fjs')
jobsNb = dataset.get('JobsNb')
machinesNb = dataset.get('machinesNb')
jobs = dataset.get('jobs')



def generate_chromossome(machinesNb, jobs):
    chromossome = []
    jobNb = 0

    for job in jobs:
        jobNb += 1
        for operation in job:
            counter = len(operation)
            machine = operation[random.randint(0, counter - 1)].get('machine', random.randint(1, machinesNb))
            for i in operation:
                machine_proc = i.get('machine') 
                if machine_proc == machine:
                    proc_time = i.get('processingTime')
                    chromossome.append({'job': jobNb ,'machine': machine, 'processingTime': proc_time})
    return chromossome

def generate_population(max_population, machinesNb, jobs):
    population = []

    for i in range(max_population):
        population.append(generate_chromossome(machinesNb, jobs))
    return population

def keyJob(e):
    return e['job']


def calculate_makespan(chromossome):
    start_time = 0
    chromossome.sort(key=keyJob)

    for job, machine, processingTime in chromossome:
        machine




chromossome = generate_chromossome(machinesNb, jobs)

calculate_makespan(chromossome)




