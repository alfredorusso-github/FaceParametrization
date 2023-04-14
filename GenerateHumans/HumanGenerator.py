import os
import itertools
import re
import sizeComputation
from pathlib import Path

def getFilePath(fn):
    upperPath = Path().absolute()
    currentPath = os.path.dirname(os.path.realpath(__file__))

    for filename in os.listdir(currentPath):
        if(filename == fn): return currentPath + "/" + fn
    
    for filename in os.listdir(upperPath):
        if(filename == fn) : return upperPath + "/" + fn

def createFolder(path):

    numbers = [int(name) for name in os.listdir(path) if re.search(r"^\d+\.?\d*$", name)]
    
    folderPath = path + "/" + str(max(numbers) + 1) if len(numbers) > 0 else path + "/1"

    if not os.path.exists(folderPath):
        print("Creating folder ...")
        os.mkdir(folderPath)

    return folderPath

class HumanGenerator():
    paramsFileName = "FaceParams.txt"
    paramsDict = {}
    choices = []
    step = 25

    VERSION = "version v1.2.0"
    CAMERA = "camera 0.0 0.0 0.0 0.0 0.0 1.225"
    STANDARD_PARAMETERS = """modifier macrodetails/Gender 1.000000
    modifier macrodetails/Age 0.500000
    modifier macrodetails/African 0.000000
    modifier macrodetails/Asian 0.000000
    modifier macrodetails/Caucasian 1.000000
    modifier macrodetails-universal/Muscle 0.500000
    modifier macrodetails-universal/Weight 0.500000
    modifier macrodetails-height/Height 0.500000
    modifier macrodetails-proportions/BodyProportions 0.500000"""
    SUFFIX = """eyes HighPolyEyes 2c12f43b-1303-432c-b7ce-d78346baf2e6
    clothesHideFaces True
    skinMaterial skins/default.mhmat
    material HighPolyEyes 2c12f43b-1303-432c-b7ce-d78346baf2e6 eyes/materials/brown.mhmat
    subdivide False"""

    PATH = os.path.expanduser("~") + "/Documenti/makehuman/v1py3/models"

    def __init__(self, d = {}) -> None:
       self.paramsDict = d

       if(len(self.paramsDict) == 0):
           self.createDict()
    
    def __len__(self):
        return len(self.paramsDict)

    def __str__(self) -> str:
        return str(self.paramsDict)
    
    def start(self):
        self.selectParameters()
    
    def createDict(self):
        filePth = getFilePath(self.paramsFileName)

        f = open(filePth)

        params = [param.split("\n")[0] for param in f.readlines()]

        for modifier in params:
            splittedLine = modifier.split("/")
            self.paramsDict.setdefault(splittedLine[0], []).append(splittedLine[1])
    
    def selectParameters(self):
        print("CHOOSE PARAMTERS FOR CREATING HUMAN")
        
        all = input("Do you wanto to choice all parameters? (Y/n): ")
        
        if(all.lower == "y" or all == ""):
            for key, values in self.paramsDict.items():
                for value in values:
                    self.choices.append(key + "/" + value)
        else:
            choiceSingleParameter = input("Do you want to choice single parameter? (Y/n): ")

            for key, values in self.paramsDict.items():
                choice = input("Do you want include parameters for {0}? (Y/n): ".format(key)) 
                if(choice.lower() == "y" or choice == ""):
                    for value in values:
                        if(choiceSingleParameter.lower() == "y" or choiceSingleParameter == ""):
                            choice = input("Do you want include parameters for {0} (Y/n): ".format(value))
                            if(choice.lower == "y" or choice == ""): self.choices.append(key + "/" + value)
                        else:
                            self.choices.append(key + "/" + value)

        # (max_range - min_range) / (num_elements - 1)
        self.step = ( (1.0 - (-1.0)) / (sizeComputation.computeSize(self.choices) - 1) ) * 100

        choice = input("Do you want to ocntinue? (Y/n): ")
        self.createHuman() if choice.lower() == "y" or choice == "" else None        
    
    def debugChoice(self):
        self.choices = [key + "/" + value for key, values in self.paramsDict.items() for value in values if key == "eyebrows"]

        self.step = (1.0 - (-1.0)) / (sizeComputation.computeSize(self.choices) - 1) * 100
        print(self.step)

        choice = input("Do you want to ocntinue? (Y/n): ")
        self.createHuman() if choice.lower() == "y" or choice == "" else None

    def createHuman(self):

        # create range of values for parameters
        values = [[i/100 for i in range(-100, 101, int(self.step))] for _ in range(len(self.choices))]

        # create folder for storing models and getting its path
        path = createFolder(self.PATH)

        print("Creating humans ...")

        humanNumber = 1
        for combination in itertools.product(*[value for value in values]):
            self.writeHuman(list(zip([choice for choice in self.choices], combination)), humanNumber, path)
            humanNumber += 1

    def writeHuman(self, human, humanNumber, path):
        fileName = "human " + str(humanNumber) + ".mhm"

        pattern = r"\n\s+"

        f = open(path + "/" + fileName, "x")

        name = "name human" + str(humanNumber)
        tmpStr = self.VERSION + "\n" + name + "\n" + self.CAMERA + "\n" + re.sub(pattern, "\n", self.STANDARD_PARAMETERS) + "\n"

        for param in human:
            tmpStr += "modifier " + param[0] + " " + str(param[1]) + "\n"

        tmpStr += re.sub(pattern, "\n", self.SUFFIX)

        f.write(tmpStr)

        f.close()

if __name__ == "__main__":
    h = HumanGenerator()
    h.start()
    # h.debugChoice()
