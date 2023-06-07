# More explanations on this file format can be found in the dataset.
import pandas as pd


def parse(path):
    file = open(path, 'r')

    firstLine = file.readline()
    firstLineValues = list(map(int, firstLine.split()[0:3]))
    opTotal = 0
    jobsNb = firstLineValues[0]
    machinesNb = firstLineValues[1]
    opMachines = firstLineValues[2]

    jobs = []

    for i in range(jobsNb):
        currentLine = file.readline()
        currentLineValues = list(map(int, currentLine.split()))
        opTotal += currentLineValues[0]
        operations = []
        opNb = 0

        j = 1
        while j < len(currentLineValues):
            k = currentLineValues[j]
            j = j+1
            operation = []
            opNb += 1
            for ik in range(k):
                machine = currentLineValues[j]
                j = j+1
                processingTime = currentLineValues[j]
                j = j+1

                operation.append({'job': i + 1,'machine': machine, 'processingTime': processingTime, 'opNb': opNb})
            operations.append(operation)
        jobs.append(operations)

    file.close()

    return {'machinesNb': machinesNb, 'JobsNb': jobsNb, 'opTotal': opTotal, 'opMachines': opMachines, 'jobs': jobs }