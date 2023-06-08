import random
import math


def swap_solution(solution):
    #Similar ao swap mutation do genetic
    pos1 = random.randint(0, len(solution) - 1)
    pos2 = random.randint(0, len(solution) - 1)

    solution[pos1], solution[pos2] = solution[pos2], solution[pos1]
    
    return solution

def check_constraints(solution):
    job_operations = {}  #Checa as restrições
    for operation in solution:
        job = operation['job']
        op_nb = operation['opNb']
        if job not in job_operations:
            job_operations[job] = 0
        if op_nb <= job_operations[job]:
            return False
        job_operations[job] = op_nb
    return True

#Similar ao replace mutation do genetic
def replace_solution(solution, jobs):
    for i in range(len(solution)):
        job = solution[i].get('job')
        opNb = solution[i].get('opNb')

        indexOp = random.randint(0, len(jobs[job - 1]) - 1)
        newOperation = jobs[job - 1][opNb - 1][indexOp]

        solution[i] = newOperation

    return solution
#diminui a temperatura pela fórmula
def decrease_temperature(initalTemp, alpha, iteration):
    temp = initalTemp * (alpha ** iteration)
    return temp

#Similar ao fitnesse function, porém sem inverter o makespan
def evaluate_makespan(solution):
    #Variáveis
    job_completion_times = {}
    machine_completion_times = {}
    total_completion_time = 0

    for operation in solution:
        job = operation['job']
        machine = operation['machine']
        processing_time = operation['processingTime']

        start_time = max(job_completion_times.get(job, 0), machine_completion_times.get(machine, 0))

        completion_time = start_time + processing_time

        job_completion_times[job] = completion_time
        machine_completion_times[machine] = completion_time

        total_completion_time = max(total_completion_time, completion_time)

    makespan = total_completion_time
    return makespan


def acceptance_probability(curr_cost, new_cost, temperature):
    if new_cost < curr_cost:
        return True  # Aceita solução melhor sem condições
    else:   # Passa pela probabilidade de aceitação
        delta_cost = new_cost - curr_cost
        prob = math.exp(-delta_cost / temperature)
        random_number = random.uniform(0, 1)
        return random_number < prob

#Função de execução do algoritmo
def simulated_annealing(initial_solution, jobs, initial_temp, alpha, max_iterations):
    current_solution = initial_solution.copy()
    current_cost = evaluate_makespan(current_solution)
    current_temp = initial_temp
    
    for iteration in range(max_iterations):
        new_solution = swap_solution(current_solution.copy())
        if check_constraints(new_solution) == False:
            new_solution = replace_solution(current_solution.copy(), jobs)
        else:
            new_solution = replace_solution(new_solution.copy(), jobs)
        new_cost = evaluate_makespan(new_solution)
        
        if acceptance_probability(current_cost, new_cost, current_temp):
            current_solution = new_solution
            current_cost = new_cost

        current_temp = decrease_temperature(initial_temp, alpha, iteration)
        if current_temp < 0.00:
            break
    print(current_cost)
    return current_solution, current_cost