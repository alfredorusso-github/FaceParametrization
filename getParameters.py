# This a simple script run inside makehuman in order to extract the name of the parameters which
# is possible to modify in the editor

import os


def write_params_to_file():
    if os.path.exists('/home/alfredo/Documenti/makehuman/v1py3/scripts/params.txt'):
        os.remove("/home/alfredo/Documenti/makehuman/v1py3/scripts" + "/params.txt")

    f = open("/home/alfredo/Documenti/makehuman/v1py3/scripts" + "/params.txt", "x")
    params = G.app.mhapi.modifiers.getAvailableModifierNames()
    f.write("\n".join(str(i) for i in params))
    f.close()


write_params_to_file()
