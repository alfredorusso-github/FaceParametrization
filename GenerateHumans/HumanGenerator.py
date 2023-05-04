import os
import itertools
import re


def create_folder(path):
    numbers = [int(name) for name in os.listdir(path) if re.search(r"^\d+\.?\d*$", name)]

    folder_path = path + "/" + str(max(numbers) + 1) if len(numbers) > 0 else path + "/1"

    if not os.path.exists(folder_path):
        print("Creating folder ...")
        os.mkdir(folder_path)

    return folder_path


class HumanGenerator:
    paramsDict = {}

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

    def __init__(self, file_pth) -> None:

        self.__create_dict(file_pth)

    def __create_dict(self, file_pth):

        f = open(file_pth)

        params = [param.split("\n")[0] for param in f.readlines()]

        for modifier in params:
            split_line = modifier.split("/")
            self.paramsDict.setdefault(split_line[0], []).append(split_line[1])

    def create_human(self, choices, step):

        # create range of values for parameters
        values = [[i / 100 for i in range(-100, 101, int(step * 100))] for _ in range(len(choices))]

        # create folder for storing models and getting its path
        path = create_folder(self.PATH)

        print("Creating humans ...")

        human_number = 1
        for combination in itertools.product(*[value for value in values]):
            self.__write_human(list(zip([choice for choice in choices], combination)), human_number, path)
            human_number += 1

        print("Finish creation")

    def __write_human(self, human, human_number, path):
        file_name = "human " + str(human_number) + ".mhm"

        pattern = r"\n\s+"

        f = open(path + "/" + file_name, "x")

        name = "name human" + str(human_number)
        tmp_str = self.VERSION + "\n" + name + "\n" + self.CAMERA + "\n" + re.sub(pattern, "\n",
                                                                                  self.STANDARD_PARAMETERS) + "\n"

        for param in human:
            tmp_str += "modifier " + param[0] + " " + str(param[1]) + "\n"

        tmp_str += re.sub(pattern, "\n", self.SUFFIX)

        f.write(tmp_str)

        f.close()
