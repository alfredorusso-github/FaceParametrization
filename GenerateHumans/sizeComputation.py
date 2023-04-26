# from HumanGenerator import getFilePath
import os
from pathlib import Path

# This utils is used in order to compute an estimated size for each face macroarea related to the parameters. 
# The size is realted to 11 values that each parameter can assume and assuming that each file has a weight of 1KB
# The value considered are [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

PARAMS = {}
SUFFIXES = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

numberOfValues = 5

def getFilePath(fn):
    upperPath = Path().absolute()
    currentPath = os.path.dirname(os.path.realpath(__file__))

    for filename in os.listdir(currentPath):
        if(filename == fn): return currentPath + "/" + fn
    
    for filename in os.listdir(upperPath):
        if(filename == fn) : return upperPath + "/" + fn

def getParams():
    paramsPath = getFilePath("FaceParams.txt")

    f = open(paramsPath)

    for line in f.readlines():
        param = line.split("\n")[0].split("/")
        PARAMS.setdefault(param[0], []).append(param[1])
    
    # print(PARAMS)

def computeSize():
    numberOfValues = int(input("How many values each parameter can assume: "))

    for key, values in PARAMS.items():
        numberCombinations = numberOfValues ** len(values)

        estimatedSize = numberCombinations * 1024

        for suffix in SUFFIXES:
            estimatedSize /= 1024
            if estimatedSize < 1024:
                print("For {0} there are {1} combinations with an estimated size of {2:.2f} {3}\n".format(key, numberCombinations, estimatedSize, suffix))
                break

def computeSize(Params):
    numberOfValues = int(input("Choose how many value each paramter can assume [3, 5, 11]: "))

    numberCombinations = numberOfValues ** len(Params)

    estimatedSize = numberCombinations * 1024

    for suffix in SUFFIXES:
        estimatedSize /= 1024

        if(suffix == 'YB' and estimatedSize > 1024):
            print("For the choices you made there are {0} combinations with an estimated size of {1:.2f} {2}".format(numberCombinations, estimatedSize, suffix))
            return numberOfValues
        elif estimatedSize < 1024:
            print("For the choices you made there are {0} combinations with an estimated size of {1:.2f} {2}".format(numberCombinations, estimatedSize, suffix))
            return numberOfValues

if __name__ == "__main__":
    getParams()
    computeSize()

