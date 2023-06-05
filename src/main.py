import pandas as pd
from utils import gantt
from algorithm import genetic as gn
from algorithm import simulated_annealing as sa

dataset = [{'job': 4, 'machine': 1, 'processingTime': 1, 'opNb': 1}, {'job': 3, 'machine': 4, 'processingTime': 7, 'opNb': 1}, {'job': 4, 'machine': 2, 'processingTime': 1, 'opNb': 2}, {'job': 2, 'machine': 1, 'processingTime': 2, 'opNb': 1}, {'job': 3, 'machine': 4, 'processingTime': 5, 'opNb': 2}, {'job': 3, 'machine': 4, 'processingTime': 2, 'opNb': 3}, {'job': 3, 'machine': 4, 'processingTime': 1, 'opNb': 4}, {'job': 2, 'machine': 2, 'processingTime': 6, 'opNb': 2}, {'job': 1, 'machine': 3, 'processingTime': 4, 'opNb': 1}, {'job': 2, 'machine': 2, 'processingTime': 5, 'opNb': 3}, {'job': 1, 'machine': 1, 'processingTime': 5, 'opNb': 2}, {'job': 1, 'machine': 3, 'processingTime': 5, 'opNb': 3}]
gantt.plot_gantt_chart(dataset)

