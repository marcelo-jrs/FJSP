import random

#Checa se cabe na solução
def checkIfFits(index, individual, opJob, opNb):
    spotOpen = 0
    for i in range(index, len(individual)):
        if individual[i] == 0:
           spotOpen += 1
    if spotOpen > opJob - opNb:
        return True
    else:
        return False
#Gera individuo
def generate_individual(op_total, op_machines, jobs):
    individual = [0] * op_total
    lastIndex = 0
    occupiedIndex = []
    x = 1
    #Checa cada uma das restrições do problema e do dataset para formar um individuo válido
    for i in range(len(jobs)):
        opJob = len(jobs[i])
        x = 1
        for j in range(len(jobs[i])):
            x = 1
            while(x == 1):
                currIndex = random.randint(0, op_total - 1)
                if op_machines > 2:
                    currOperation = jobs[i][j][random.randint(0, op_machines - 1)]
                elif op_machines == 2:
                    currOperation = jobs[i][j][random.randint(0, op_machines)]
                if individual[currIndex] == 0:
                    if currOperation != individual[currIndex]:
                        if currIndex + opJob - currOperation.get('opNb') < op_total:
                            if lastIndex < currIndex | (lastIndex == 0 & currIndex == 0):
                                if checkIfFits(currIndex, individual, opJob, currOperation.get('opNb')) == True:
                                    individual[currIndex] = currOperation
                                    lastIndex = currIndex
                                    occupiedIndex.append(lastIndex)
                                    x = 0
        lastIndex = 0

    return individual
#Gera uma população de individuos
def generate_population(max_population, op_total, op_machines, jobs):
    population = []

    for i in range(max_population):
        population.append(generate_individual(op_total, op_machines, jobs))
    return population
#Retorna o fitness de um individuo, o "makespan"
def fitnes_function(individual):
    # Initialize variables
    job_completion_times = {}
    machine_completion_times = {}
    total_completion_time = 0

    #Passa por cada cromossomo ou gene do individuo
    for chromosome in individual:
        job = chromosome['job']
        machine = chromosome['machine']
        processing_time = chromosome['processingTime']

        #Calcula o start time para cada operação
        start_time = max(job_completion_times.get(job, 0), machine_completion_times.get(machine, 0))

        #Atualiza o completion time da operação
        completion_time = start_time + processing_time

        #Atualiza o completion time para o job e a máquina
        job_completion_times[job] = completion_time
        machine_completion_times[machine] = completion_time

        #Atualiza o tempo total
        total_completion_time = max(total_completion_time, completion_time)

    fitness = 1 / total_completion_time
    return fitness

#Crossover ou reprodução de 2 individuos
def order_crossover(parent1, parent2):
    #Seleciona 2 pontos aleatórios
    point1 = random.randint(0, len(parent1) - 2)
    point2 = random.randint(point1 + 1, len(parent1) - 1)
    
    child = [None] * len(parent1)
    
    #Copia os pontos selecionados de cada pai
    child[point1:point2] = parent1[point1:point2]
    
    #Preenche os pontos restantes
    index = point2
    for value in parent2[point2:] + parent2[:point2]:
        if value not in child:
            child[index] = value
            index = (index + 1) % len(parent1)
    
    return child
#Checa se a criança gerada esta de acordo com cada restrição
def check_constraints(child):
    job_operations = {} #Rastreia cad ajob
    for operation in child:
        job = operation['job']
        op_nb = operation['opNb']
        if job not in job_operations:
            job_operations[job] = 0  #Verifica se as operações estão em ordem
        if op_nb <= job_operations[job]:
            return False  #Falso
        job_operations[job] = op_nb
    return True  #True

def keyFit():
    return 'fitScore'
#Torneio para selecionar os 2 pais do crossover
def tournament_selection(population, tournament_size):
    fitness_score = []

    #Seleciona individuos aleatoriamente
    tournament = random.sample(population, tournament_size)

    #Calcula o fitness
    for individual in tournament:
        fitness_score.append({'fitScore': fitnes_function(individual), 'individual': individual})
    fitness_sorted = sorted(fitness_score, key=lambda x: x['fitScore'], reverse=True)
    
    #Seleciona os dois melhores do torneio
    parent1 = fitness_sorted[0].get('individual')
    parent2 = fitness_sorted[1].get('individual')

    return parent1, parent2
#Mutação de inversão
def swap_mutation(individual):
    #Seleciona 2 posições aleatorias
    pos1 = random.randint(0, len(individual) - 1)
    pos2 = random.randint(0, len(individual) - 1)
    
    #Troca as posiçoes, gerando um individuo diferente
    individual[pos1], individual[pos2] = individual[pos2], individual[pos1]
    
    return individual
#Mutação de troca, seleciona outras operações do dataset para mutar o individuo
def replace_mutation(individual, jobs):
    for i in range(len(individual)):
        job = individual[i].get('job')
        opNb = individual[i].get('opNb')

        indexOp = random.randint(0, len(jobs[job - 1]) - 1)
        newOperation = jobs[job - 1][opNb - 1][indexOp]

        individual[i] = newOperation

    return individual


def replace(population, child):

    #crossover até faltarem 2 na população
    #guarda os 2 melhores da antiga gen e troca os antigos pelos novos
    fitness_score = []

    #Ordena a população pelo fitness
    for individual in population:
        fitness_score.append({'fitScore': fitnes_function(individual), 'individual': individual})
    fitness_sorted = sorted(fitness_score, key=lambda x: x['fitScore'], reverse=True)
    
    index = len(fitness_sorted) - 1

    population.pop(index)
    population.insert(index, child)

    return population

def genetic_algorithm(max_generation, max_opulation, torunament_size, op_total, op_machines, jobs):
    population = generate_population(max_opulation, op_total, op_machines, jobs)
    currSolution = population[0]
    # Executar o algoritmo genético
    for generation in range(max_generation):
        # Avaliar a aptidão de cada indivíduo na população
        fitness_scores = []
        for individual in population:
            fitness = fitnes_function(individual)
            fitness_scores.append({'fitScore': fitness, 'individual': individual})

        # Selecionar os pais para reprodução
        parent1, parent2 = tournament_selection(population, torunament_size)

        if fitnes_function(currSolution) < fitnes_function(parent1):
            currSolution = parent1

        counter = 0
        while len(population) > counter:
            # Aplicar crossover
            child = order_crossover(parent1, parent2)

            # Verificar as restrições do filho gerado
            if check_constraints(child):
                # Substituir um indivíduo na população pelo filho gerado
                population = replace(population, child)
                counter += 1

        # Aplicar mutação

    # Obter a melhor solução da população final
    best_solution = max(population, key=lambda x: fitnes_function(x))
    best_score = fitnes_function(best_solution)
    return best_solution, best_score

