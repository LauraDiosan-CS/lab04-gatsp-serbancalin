import ga

def read(fileName):
    d = {}
    f = open(fileName, "r")
    line = f.readline().strip()
    d["n"] = int(line)
    matrix = []
    for i in range(d["n"]):
        line = f.readline().strip()
        nrs = []
        for nr in line.split(" "):
            nrs.append(int(nr))
        matrix.append(nrs)
    d["matrix"] = matrix
    line = f.readline().strip()
    d["startNode"] = int(line)
    return d


def printSolution(drumMinim, traseu):
    print("Drumul minim: ", drumMinim)
    string = "\nTraseu: "
    for x in traseu:
        string += str(x) + " "
    string += str(traseu[0])
    print(string)


def run():
    fileName = input("Numele fisierului intrare: ")
    d = read(fileName)

    d["dimensiunePopulatie"] = 15
    d["nrGeneratii"] = 500
    drum, distanta = ga.mainGA(d)
    printSolution(distanta, drum)

while True:
    run()
