import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='estagio',
)


def insert_instance(autor, dataset, max_population, max_generation, tournament_size, initial_temp, alpha, max_iterations):
  conexao.connect()
  cursor = conexao.cursor()
  cursor.execute(f'INSERT INTO instance (autor, dataset, max_population, max_generation, tournament_size, initial_temp, alpha, max_iterations) VALUES ("{autor}", {dataset}, {max_population}, {max_generation}, {tournament_size}, {initial_temp}, {alpha}, {max_iterations})')
  conexao.commit()
  id = cursor.getlastrowid()
  cursor.close()
  conexao.close()
  return id

def insert_result(id_instance, makespan):
  conexao.connect()
  cursor = conexao.cursor()
  cursor.execute(f'INSERT INTO result (id_instance, makespan) VALUES ({id_instance},{makespan})')
  conexao.commit()
  id = cursor.getlastrowid()
  cursor.close()
  conexao.close()
  return id

def insert_operation(id_result, solution):
  conexao.connect()
  cursor = conexao.cursor()
  for operation in solution:
    cursor.execute('INSERT INTO operation (id_result, job, machine, processing_time, operation_number) VALUES ({0}, {1}, {2}, {3}, {4})'.format(id_result, operation.get('job'), operation.get('machine'), operation.get('processingTime'), operation.get('opNb')))
  cursor.close()
  conexao.commit()
  conexao.close()

data = [{'job': 4, 'machine': 1, 'processingTime': 1, 'opNb': 1}, {'job': 4, 'machine': 2, 'processingTime': 1, 'opNb': 2}, {'job': 3, 'machine': 4, 'processingTime': 7, 'opNb': 1}, {'job': 1, 'machine': 3, 'processingTime': 4, 'opNb': 1}, {'job': 3, 'machine': 4, 'processingTime': 5, 'opNb': 2}, {'job': 2, 'machine': 1, 'processingTime': 2, 'opNb': 1}, {'job': 2, 'machine': 2, 'processingTime': 6, 'opNb': 2}, {'job': 3, 'machine': 1, 'processingTime': 2, 'opNb': 3}, {'job': 3, 'machine': 4, 'processingTime': 1, 'opNb': 4}, {'job': 1, 'machine': 3, 'processingTime': 5, 'opNb': 2}, {'job': 1, 'machine': 3, 'processingTime': 5, 'opNb': 3}, {'job': 2, 'machine': 2, 'processingTime': 5, 'opNb': 3}]
autor = 'autor'
id_instance = insert_instance(autor, 1, 1, 1, 1 ,1 , 1, 1)
id_result = insert_result(id_instance, 19)
insert_operation(id_result, data)
