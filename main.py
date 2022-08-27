import json
import numpy as np
import random as rand

from client2 import *

id = 'BhMZwn8YBiNiEqJ1mI0BY8EoNIVBExPjW1L898o7ptKIVXnIXi'

overfit = []
popsz = 10
iter = 3
mut_num = 5
max = 10e22
w = [1, 3]

answer = np.zeros((10, 11))
anserr = np.array([[max, max]] * 10)

def dumping(population, file):

    for i in range(0, popsz):
        file.write('\n')
        json.dump(np.array(population[i]).tolist(), file)

def fileChange(index):
    for indi in range(10, index + 1, -1):
        old = "generations_{}.txt".format(indi - 1)
        new = "generations_{}.txt".format(indi)

        with open(old, "r") as fro, open(new, "w") as to:
            to.write(fro.read())

def ansupdate(vec, error):
    global answer, anserr

    if(error[1] > anserr[9][1]):
        return 

    for i in range(0, 10):
        if(error[1] < anserr[i][1]):
            answer = np.delete(answer, 9, 0)
            answer = np.insert(answer, i, vec, 0)

            anserr = np.delete(anserr, 9, 0)
            anserr = np.insert(anserr, i, error, 0)

            fileChange(i)
            old = "tempor.txt"
            new = "generations_{}.txt".format(i + 1)
            with open(old, "r") as fro, open(new, "w") as to:
                to.write(fro.read())

            break

def mutation(population):

    for i in range(0, len(population)):

        j = rand.randint(0, 10)
        population[i][j] *= rand.uniform(-100, 100) 
        if(abs(population[i][j]) > 10):
            population[i][j] /= 100

    return population[:]

def fitness(pop):

    err = []
    totErr = 0
    prob = []
    prob2 = []

    for i in range(0, popsz):
        temp = np.array(get_errors(id, pop[i]))
        # err.append(w[0] * temp[0] + w[1] * temp[1])
        ansupdate(pop[i][:], temp)

    # pop = [x for y, x in sorted(zip(err, pop))]
    # err.sort()
    pop = answer[:]
    # err = anserr[:]
    for i in range(0, len(anserr)):
        err.append(w[0] * anserr[i][0] + w[1] * anserr[i][1])

    totErr = np.sum(np.array(err[:(int)(popsz / 2)]))
    for i in range(0, (int)(popsz / 2)):
        prob.append(err[i] / totErr)

    return prob
    
def crossover(selected):
    population = []

    for i in range(0, popsz, 2):
        num = rand.randint(2, 9)

        c1 = selected[i][:]
        c2 = selected[i + 1][:]

        temp = c1[:]
        c1[num:] = c2[num:]
        c2[num:] = temp[num:]

        population.append(c1)
        population.append(c2)

    return population

def selection(pop, prob):

    selected = []
    temp = prob[:]
    prev = 0
    pind = -1
    
    for i in range(0, popsz):
        num = rand.uniform(0, 1)
        upper = 0
        lower = 0

        for j in range(0, popsz):
            upper += temp[j]

            if(num < upper and num >= lower):
                selected.append(pop[j])

                for k in range(0, len(prob)):
                    if(k == pind):
                        temp[k] = prev
                    else:
                        temp[k] -= prev / (len(prob)- 1)

                for k in range(0, len(prob)):
                    if(k != j):
                        temp[k] += temp[j] / (len(prob)- 1)

                prev = temp[j]
                pind = j
                temp[j] = 0
                break

            lower = upper

    return selected[:]

def genalg(pop):

    global answer, anserr

    for i in range(0, iter):
        with open('tempor.txt', 'a') as file:
            file.write('\n\n\n')
            json.dump("Iteration ", file)
            json.dump(i, file)

            file.write('\n\n')
            json.dump("Initial Population", file)
            dumping(pop, file)

            prob = fitness(pop)
            # pop = generate(answer[0])

            selected = selection(pop, prob)
            file.write('\n\n')
            json.dump("After Selection", file)
            dumping(selected, file)
 
            pop = crossover(selected)
            file.write('\n\n')
            json.dump("After Crossover", file)
            dumping(pop, file)
        
            # for l in range(0, mut_num):
                # pop = mutation(pop)
            tempo = []
            for l in range(0, 5):
                ret = generate(pop[l], 2)[:]
                for z in range(0, len(ret)):
                    tempo.append(ret[z])
            pop = tempo[:]
        
            file.write('\n\n')
            json.dump("After mutation", file)
            dumping(pop, file)

    fitness(pop)
    with open('output.json', 'a') as op:
        json.dump(answer, op)
        
    with open('temp.txt', 'a') as temp:
        for i in range(0, 10):
            json.dump(np.array(answer[i]).tolist(), temp)
            json.dump(np.array(anserr[i]).tolist(), temp)
            temp.write('\n')

def generate(best, num):
    population = np.array([best][:] * num).tolist()

    for i in range(0, mut_num):
        population = mutation(population)

    return population

def main():

    with open('overfit.txt', 'r') as file:
        overfit = json.load(file)

    for i in range(1, 11):
        fname = "generations_{}.txt".format(i)
        with open(fname, 'w') as file:
            dumping(overfit, file)

    pop = generate(overfit, popsz)
    genalg(pop)

if __name__ == "__main__":
    main()
