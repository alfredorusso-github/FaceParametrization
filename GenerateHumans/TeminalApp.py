from HumanGenerator import HumanGenerator
import utils

h = HumanGenerator(utils.get_file_path())


# (max_range - min_range) / (num_elements - 1)
# self.step = ((1.0 - (-1.0)) / (sizeComputation.compute_size(self.choices) - 1)) * 100
#
# choice = input("Do you want to continue? (Y/n): ")
# self.createHuman() if choice.lower() == "y" or choice == "" else None


class App:
    choices = []

    def __init__(self):
        self.__start_wizard()

    def __start_wizard(self):
        self.__select_parameters()

        if len(self.choices) != 0:
            self.get_size_info()
        else:
            print("You didn't select any parameter! Try again...")

    def __select_parameters(self):
        print("CHOOSE PARAMETERS FOR CREATING HUMAN")

        all_params = input("Do you want to to choice all_params parameters? (Y/n): ")

        if all_params.lower == "y" or all_params == "":
            for key, values in h.paramsDict.items():
                for value in values:
                    self.choices.append(key + "/" + value)
        else:
            choice_single_parameter = input("Do you want to choice single parameter? (Y/n): ")

            for key, values in h.paramsDict.items():
                choice = input("Do you want include parameters for {0}? (Y/n): ".format(key))
                if choice.lower() == "y" or choice == "":
                    for value in values:
                        if choice_single_parameter.lower() == "y" or choice_single_parameter == "":
                            choice = input("Do you want include parameters for {0} (Y/n): ".format(value))
                            if choice.lower == "y" or choice == "":
                                self.choices.append(key + "/" + value)
                        else:
                            self.choices.append(key + "/" + value)

    # def debug_choice(self):
    #     self.choices = [key + "/" + value for key, values in h.paramsDict.items() for value in values if
    #                     key == "eyebrows"]
    #
    #     self.step = (1.0 - (-1.0)) / (utils.compute_size(self.choices) - 1) * 100
    #     print(self.step)
    #
    #     choice = input("Do you want to continue? (Y/n): ")
    #     h.createHuman() if choice.lower() == "y" or choice == "" else None

    def get_size_info(self):
        step = input("Select step size: ")
        num_values = (1 / float(step)) + 1

        print(utils.compute_size(self.choices, num_values))

        choice = input("Do you want to continue? (Y/n): ")
        h.create_human(self.choices, float(step)) if choice.lower() == "y" or choice == "" else None


if __name__ == '__main__':
    app = App()
