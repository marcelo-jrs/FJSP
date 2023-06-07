import matplotlib.pyplot as plt

def plot_gantt_chart(data):

    job_colors = {
        1: '#EF767A',
        2: '#456990',
        3: '#49BEAA',
        4: '#FF8C42',
        5: '#FFF275',
        6: '#C97B84',
        7: '#F9564F',
        8: '#7CA982',
        9: '#C44536',
        10: '#3C4F76'
    }
    # Initialize variables
    job_completion_times = {}
    machine_completion_times = {}
    total_completion_time = 0

    # Iterate over each operation in the solution 
    for operation in data:
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

        plt.barh(machine, processing_time, left=start_time, height=0.5, align='center', color=job_colors[job])

        plt.text(start_time + processing_time / 2, machine, f"Op {operation['opNb']}", ha='center', va='center')

    
    # Definir a escala do eixo X
    plt.xlim(0, total_completion_time)
    # Configurar o eixo Y
    machines = set(operation['machine'] for operation in data)
    plt.yticks(list(machines))
    plt.ylim(0.5, len(machines) + 0.5)
    plt.gca().invert_yaxis()

    # Definir rótulos dos eixos
    plt.xlabel('Tempo')
    plt.ylabel('Máquinas')

    plt.plot()

    # Exibir o gráfico de Gantt
    return plt.show()
