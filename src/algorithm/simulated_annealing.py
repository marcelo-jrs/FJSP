import random
import math


def swap_solution(solution):
    # Randomly select two positions in the operation
    pos1 = random.randint(0, len(solution) - 1)
    pos2 = random.randint(0, len(solution) - 1)
    
    # Check if the positions violate any constraints
    while not check_constraints(solution, pos1, pos2):
        pos1 = random.randint(0, len(solution) - 1)
        pos2 = random.randint(0, len(solution) - 1)

    # Swap the values at the selected positions
    solution[pos1], solution[pos2] = solution[pos2], solution[pos1]
    
    return solution

def check_constraints(solution, pos1, pos2):
    # Retrieve the job and operation numbers at the selected positions
    job1 = solution[pos1]['job']
    job2 = solution[pos2]['job']
    opNb1 = solution[pos1]['opNb']
    opNb2 = solution[pos2]['opNb']

    # Check if swapping violates the constraints
    if job1 == job2 or opNb1 != opNb2:
        return False
    
    return True


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

def evaluate_makespan(solution):
    machine_completion_times = [0] * (max(operation['machine'] for operation in solution) + 1)

    for operation in solution:
        machine = operation['machine']
        processing_time = operation['processingTime']

        start_time = machine_completion_times[machine]
        completion_time = start_time + processing_time

        machine_completion_times[machine] = completion_time

    makespan = max(machine_completion_times)
    return makespan


def acceptance_probability(curr_cost, new_cost, temperature):
    if new_cost < curr_cost:
        return True  # Aceita solução melhor sem condições
    else:
        delta_cost = new_cost - curr_cost
        prob = math.exp(-delta_cost / temperature)
        random_number = random.uniform(0, 1)
        return random_number < prob

def simulated_annealing(initial_solution, jobs, initial_temp, alpha, max_iterations):
    current_solution = initial_solution.copy()
    current_cost = evaluate_makespan(current_solution)
    current_temp = initial_temp
    
    for iteration in range(max_iterations):
        new_solution = replace_solution(current_solution.copy(), jobs)
        new_solution = swap_solution(new_solution.copy())
        new_cost = evaluate_makespan(new_solution)
        
        if acceptance_probability(current_cost, new_cost, current_temp):
            current_solution = new_solution
            current_cost = new_cost

        current_temp = decrease_temperature(initial_temp, alpha, iteration)
        if current_temp < 0.00:
            break
    print(current_cost)
    return current_solution, current_cost