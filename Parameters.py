import os

def WriteParamsToFile():
    
    if(os.path.exists("/home/alfredo/Documenti/makehuman/v1py3/scripts/params.txt")):
        os.remove("/home/alfredo/Documenti/makehuman/v1py3/scripts" + "/params.txt")
    
    f = open("/home/alfredo/Documenti/makehuman/v1py3/scripts" + "/params.txt", "x")
    params = G.app.mhapi.modifiers.getAvailableModifierNames()
    f.write("\n".join(str(i) for i in params))
    f.close()

WriteParamsToFile()

