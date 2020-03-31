import random

def mainGA(input):
    nrIteratii = input["nrGeneratii"]
    # se creeaza o populatie
    populatie = Populatie()
    populatie.populeaza(input["n"], input["dimensiunePopulatie"], input["startNode"])

    while nrIteratii > 0:
        parinte1 = selectieReproducere(populatie, input["matrix"])
        parinte2 = selectieReproducere(populatie, input["matrix"])

        copil1, copil2 = incrucisare(parinte1, parinte2)

        copil1.mutatie()
        copil2.mutatie()

        while not copil1.eValid(input["startNode"]):
            copil1.mutatie()
        while not copil2.eValid(input["startNode"]):
            copil2.mutatie()

        if copil1.fitness(input["matrix"]) > copil2.fitness(input["matrix"]):
            copil1 = copil2

        populatie.selectieSupravietuire(copil1, input["matrix"])
        nrIteratii -= 1
    # se returneaza cromozomul cu fitnessul minim si valoarea acestuia
    return fitnessMinim(populatie, input["matrix"])

class Cromozom:
    """
    lista de noduri -> permutare de elemente de n
    """
    def __init__(self, n):
        self.__n = n
        self.__permutare = generarePermutareIdentica(n)

    def __eq__(self, other):
        for i in range(self.__n):
            if self.__permutare[i] != other.__permutare[i]:
                return False
        return True

    def getPermutare(self):
        return self.__permutare

    def setPermutare(self, permutare):
        self.__permutare = permutare

    def getN(self):
        return self.__n

    def mutatie(self):
        i = random.randrange(self.__n)
        j = random.randrange(self.__n)
        self.__permutare[i], self.__permutare[j] = self.__permutare[j], self.__permutare[i]

    def eValid(self, startNode):
        return self.__permutare[0] == startNode

    def fitness(self, matrix):
        f = 0
        node = self.__permutare[0]
        for i in range(self.__n - 1):
            f += matrix[node - 1][self.__permutare[i + 1] - 1]
            node = self.__permutare[i + 1]
        # se adauga la final si drumul de la ultimul nod la startNode
        # un cromozom e valid doar daca permutarea sa incepe cu startNode
        f += matrix[node - 1][self.__permutare[0] - 1]
        return f


class Populatie:
    """
    lista de cromozomi
    """
    def __init__(self):
        self.__cromozomi = []

    def addCromozom(self, cromozom):
        self.__cromozomi.append(cromozom)

    def getCromozomi(self):
        return self.__cromozomi

    def populeaza(self, n, dimesiunePopulatie, startNode):
        dim = 0
        while dim < dimesiunePopulatie:
            cromozom = Cromozom(n)
            while not cromozom.eValid(startNode):
                cromozom.mutatie()
            dim += 1
            self.__cromozomi.append(cromozom)

    def selectieSupravietuire(self, copil, matrix):
        fitnessMaxim = 0
        indexFitnessMaxim = -1
        index = -1
        for cromozom in self.__cromozomi:
            index += 1
            fitness = cromozom.fitness(matrix)
            if fitness > fitnessMaxim:
                fitnessMaxim = fitness
                indexFitnessMaxim = index
        if copil.fitness(matrix) < fitnessMaxim and indexFitnessMaxim > -1:
            self.__cromozomi[indexFitnessMaxim] = copil


def generarePermutareIdentica(n):
    permutare = []
    for i in range(n):
        permutare.append(i + 1)
    return permutare


def incrucisare(parinte1, parinte2):
    p1 = parinte1.getPermutare()
    p2 = parinte2.getPermutare()
    c1 = Cromozom(parinte1.getN())
    permutare = p1[:2]
    for i in range(2, parinte2.getN()):
        if p2[i] not in permutare:
            permutare.append(p2[i])
    for x in p2:
        if x not in permutare:
            permutare.append(x)
    c1.setPermutare(permutare)
    c2 = Cromozom(parinte2.getN())
    permutare = p2[:2]
    for i in range(2, parinte1.getN()):
        if p1[i] not in permutare:
            permutare.append(p1[i])
    for x in p1:
        if x not in permutare:
            permutare.append(x)
    c2.setPermutare(permutare)
    return c1, c2


def selectieReproducere(populatie, matrix):
    probabilitati = [0]
    sumaFitness = 0
    i = 1
    for cromozom in populatie.getCromozomi():
        fitness = 1 / cromozom.fitness(matrix)
        sumaFitness += fitness
        probabilitati.append(fitness)
        i += 1
    for j in range(1, i):
        prob = probabilitati[j] / sumaFitness
        probabilitati[j] = prob
    s = 0
    for j in range(i):
        s += probabilitati[j]
        probabilitati[j] = s
    nr = random.random()
    for j in range(1, i):
        if probabilitati[j - 1] <= nr < probabilitati[j]:
            return populatie.getCromozomi()[j - 1]
    return None


def fitnessMinim(populatie, matrix):
    copil = populatie.getCromozomi()[0]
    fitnessMin = copil.fitness(matrix)
    for c in populatie.getCromozomi():
        fitness = c.fitness(matrix)
        if fitness < fitnessMin:
            fitnessMin = fitness
            copil = c
    return copil.getPermutare(), fitnessMin