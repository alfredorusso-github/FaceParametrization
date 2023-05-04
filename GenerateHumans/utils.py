# This utils is used in order to compute an estimated size for each face macro area related to the parameters.
# The size is related to 11 values that each parameter can assume and assuming that each file has a weight of 1KB
# The value considered are [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

import os
from pathlib import Path

paramsFileName = "FaceParams.txt"
SUFFIXES = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']


def get_file_path():
    upper_path = Path().absolute()
    current_path = os.path.dirname(os.path.realpath(__file__))

    for FILENAME in os.listdir(current_path):
        if FILENAME == paramsFileName:
            return current_path + "/" + paramsFileName

    for FILENAME in os.listdir(upper_path):
        if FILENAME == paramsFileName:
            return upper_path + "/" + paramsFileName


def compute_size(params, number_of_values):
    number_combinations = number_of_values ** len(params)

    estimated_size = number_combinations * 1024

    for suffix in SUFFIXES:
        estimated_size /= 1024

        if suffix == 'YB' and estimated_size > 1024:
            return "For the choices you made there are {0} combinations with an estimated size of {1:.2f} {2}".format(
                number_combinations, estimated_size, suffix)
        elif estimated_size < 1024:
            return "For the choices you made there are {0} combinations with an estimated size of {1:.2f} {2}".format(
                number_combinations, estimated_size, suffix)
