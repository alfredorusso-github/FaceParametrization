import os
import re

PARAMS_FILE = "/home/alfredo/Documenti/makehuman/v1py3/scripts/params.txt"
MODELS_DIR = "/home/alfredo/Documenti/makehuman/v1py3/models"

VERSION = "version v1.2.0"
SUFFIX = """eyes HighPolyEyes 2c12f43b-1303-432c-b7ce-d78346baf2e6
clothesHideFaces True
skinMaterial skins/default.mhmat
material HighPolyEyes 2c12f43b-1303-432c-b7ce-d78346baf2e6 eyes/materials/brown.mhmat
subdivide False"""

params = []
name = ""
camera = "camera 0.0 0.0 0.0 0.0 0.0 1.225"

standard_modifiers = """modifier breast/BreastSize 0.500000
modifier breast/BreastFirmness 0.500000
modifier macrodetails/Gender 1.000000
modifier macrodetails/Age 0.500000
modifier macrodetails/African 0.000000
modifier macrodetails/Asian 0.000000
modifier macrodetails/Caucasian 1.000000
modifier macrodetails-universal/Muscle 0.500000
modifier macrodetails-universal/Weight 0.500000
modifier macrodetails-height/Height 0.500000
modifier macrodetails-proportions/BodyProportions 0.500000"""

def createHuman():
    human = ""

    for i in range(-100, 101, 20):
        global name
        name = "name human" + str(i/10)

        human = "modifier nose/nose-scale-vert-decr|incr " + str(i/100)
        WriteHuman(human)


def createDefaultHuman():
    global name
    name = "name dafault"

    global camera
    camera = "camera 0.0 0.0 0.0 0.0 0.0 1.225"

    WriteHuman("")

def getFileName():
    return "/human" + str(getModelNumber()) + ".mhm"

def getModelNumber():
    numbers = []

    for filename in os.listdir(MODELS_DIR):
        if(re.search(r"\d+\.mhm$", filename)):
            numbers.append(int(list(filter(str.isdigit, filename))[0]))

    modelNumber = 0
    try:
        modelNumber = max(numbers) + 1
    except:
        modelNumber = 0
    
    return modelNumber

def WriteHuman(human):
    result = VERSION + "\n" + name + "\n" + camera + "\n" + standard_modifiers + "\n" + human + "\n" + SUFFIX

    f = open(MODELS_DIR + getFileName(), "x")
    f.write(result)
    f.close()

def getParams():
    
    try:

        f = open(PARAMS_FILE, "r")
        
        global params
        params = [param.split("\n")[0] for param in f.readlines()]

        f.close()

    except:
        print("Error while opening file")
    else:
        print("File opened")

def printParams():
    if(len(params) == 0):
        getParams()
    
    print(params)

if __name__ == "__main__":
    createHuman()