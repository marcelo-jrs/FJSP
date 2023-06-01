import random
import math


def swap_solution(solution):
    # Randomly select two positions in the operation
    pos1 = random.randint(0, len(solution) - 1)
    pos2 = random.randint(0, len(solution) - 1)
    
    # Swap the values at the selected positions
    solution[pos1], solution[pos2] = solution[pos2], solution[pos1]
    
    return solution

def replace_solution(solution, jobs):
    for i in range(len(solution)):
        job = solution[i].get('job')
        opNb = solution[i].get('opNb')

        indexOp = random.randint(0, len(jobs[job - 1]) - 1)
        newOperation = jobs[job - 1][opNb - 1][indexOp]

        solution[i] = newOperation

    return solution

def decrease_temperature(initalTemp, alpha, iteration):
    temp = initalTemp * (alpha ** iteration)
    return temp

def evaluate(solution):
    # Initialize variables
    job_completion_times = {}
    machine_completion_times = {}
    total_completion_time = 0

    # Iterate over each chromosome in the solution
    for operation in solution:
        job = operation['job']
        machine = operation['machine']
        processing_time = operation['processingTime']

        # Calculate the start time for the current operation
        start_time = max(job_completion_times.get(job, 0), machine_completion_times.get(machine, 0))

        # Update the completion time for the current operation
        completion_time = start_time + processing_time

        # Update the completion times for the job and machine
        job_completion_times[job] = completion_time
        machine_completion_times[machine] = completion_time

        # Update the total completion time
        total_completion_time = max(total_completion_time, completion_time)

    cost = total_completion_time
    return cost

def accept_solution(currCost, newCost, temperature):
    acceptance_probability = math.exp((currCost - newCost) / temperature)
    random_number = random.uniform(0, 1)
    
    if random_number < acceptance_probability:
        return True  # New solution is accepted
    else:
        return False  # New solution is rejected


solution = [{'job': 4, 'machine': 2, 'processingTime': 5, 'opNb': 1}, {'job': 4, 'machine': 4, 'processingTime': 1, 'opNb': 2}, {'job': 2, 'machine': 5, 'processingTime': 8, 'opNb': 1}, {'job': 3, 'machine': 2, 'processingTime': 8, 'opNb': 1}, {'job': 3, 'machine': 4, 'processingTime': 5, 'opNb': 2}, {'job': 3, 'machine': 1, 'processingTime': 2, 'opNb': 3}, {'job': 1, 'machine': 2, 'processingTime': 5, 'opNb': 1}, {'job': 3, 'machine': 1, 'processingTime': 4, 'opNb': 4}, {'job': 2, 'machine': 4, 'processingTime': 8, 'opNb': 2}, {'job': 2, 'machine': 5, 'processingTime': 5, 'opNb': 3}, {'job': 1, 'machine': 4, 'processingTime': 7, 'opNb': 2}, {'job': 1, 'machine': 2, 'processingTime': 5, 'opNb': 3}]
initalTemp = 100.0
currTemp = initalTemp
alpha = 0.95
iteration = 0

