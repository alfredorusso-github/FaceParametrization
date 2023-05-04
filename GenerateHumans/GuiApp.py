import tkinter as tk

from HumanGenerator import HumanGenerator
from ttkwidgets import CheckboxTreeview
import customtkinter as ctk

import utils

h = HumanGenerator(utils.get_file_path())


class TreeViewFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)

        self.grid(padx=10, pady=10)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Introduction label
        ctk.CTkLabel(self, text='Select parameters').grid(column=0, row=0, sticky='W', padx=10, pady=10)

        # Treeview
        self.tree = CheckboxTreeview(self, show="tree")

        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        child_id = len(h.paramsDict)
        for i, (key, values) in enumerate(h.paramsDict.items()):
            self.tree.insert('', tk.END, text=key, open=False, iid=str(i))

            for value in values:
                self.tree.insert('', tk.END, text=value, iid=child_id)
                self.tree.move(child_id, str(i), 0)
                child_id = child_id + 1

        scrollbar = ctk.CTkScrollbar(self, orientation='vertical', command=self.tree.yview())
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.tree['yscrollcommand'] = scrollbar.set

    def __print_checked(self):
        for item in self.tree.get_checked():
            print(self.tree.item(item)['text'])

        print('-' * 50)


class ButtonsFrame(ctk.CTkFrame):
    choices = []

    def __init__(self, container, treeviewframe):
        super().__init__(container)

        self.treeViewFrame = treeviewframe

        self.grid(padx=10, pady=10)

        self.columnconfigure(2, weight=4)

        # Slider stuff
        ctk.CTkLabel(self, text='Select step range:').grid(column=0, row=0, sticky='w', padx=10)

        self.current_value = tk.DoubleVar(value=0.25)
        ctk.CTkSlider(self, from_=0, to=1, orientation='horizontal', variable=self.current_value,
                      command=self.change_value).grid(column=1, row=0, sticky='w')

        self.valueLabel = ctk.CTkLabel(self, text=str(self.current_value.get()))
        self.valueLabel.grid(column=2, row=0, sticky='w', padx=5)

        # Run button
        ctk.CTkButton(self, text='Run', width=100, command=self.__start, hover=True, corner_radius=50).grid(column=0,
                                                                                                            row=1,
                                                                                                            sticky='se',
                                                                                                            padx=10,
                                                                                                            pady=5,
                                                                                                            columnspan=3)

    def change_value(self, event):
        self.valueLabel.configure(text=self.get_value(float(event)))

    @staticmethod
    def get_value(value):
        rounded = round(value, 2)
        return f"{rounded:.2f}"

    def __start(self):
        # setting choices made
        tree = self.treeViewFrame.tree

        self.choices = [tree.item(tree.parent(item))['text'] + "/" + tree.item(item)['text'] for item in
                        self.treeViewFrame.tree.get_checked()]

        if len(self.choices) == 0:
            return None

        # setting step size
        step = round(self.current_value.get(), 2)
        num_values = (1 / step) + 1

        size_string = utils.compute_size(self.choices, num_values)

        size_dialog = SizeDialog(size_string)

        h.create_human(self.choices, step) if size_dialog.get_user_input() else None


class SizeDialog(ctk.CTkToplevel):

    message = ''
    choice = False

    def __init__(self, msg):
        super().__init__()
        self.geometry("350x200")
        self.resizable(False, False)

        self.message = msg
        self._create_widgets()

    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.size_label = ctk.CTkLabel(self, text=self.message, width=300, wraplength=300)
        self.size_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky='ew')

        self.ok_button = ctk.CTkButton(self, text='OK', width=100, corner_radius=100, command=self._ok_event)
        self.ok_button.grid(row=1, column=0, columnspan=1, padx=(20, 10), pady=(0, 20), sticky='ew')

        self.cancel_button = ctk.CTkButton(self, text='Cancel', width=100, corner_radius=100, command=self._cancel_event)
        self.cancel_button.grid(row=1, column=1, columnspan=1, padx=(20, 10), pady=(0, 20), sticky='ew')

    def _ok_event(self):
        self.choice = True
        self.destroy()

    def _cancel_event(self):
        self.choice = False
        self.destroy()

    def get_user_input(self):
        self.master.wait_window(self)
        return self.choice


class App(ctk.CTk):
    window_width = 800
    window_height = 600

    def __init__(self):
        super().__init__()
        self._set_appearance_mode("system")

        # setting title
        self.title("Human Generator")

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - self.window_width / 2)
        center_y = int(screen_height / 2 - self.window_height / 2)

        # setting window position to the center of the screen
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        # set the minimum size of the window
        self.minsize(800, 600)

        self.columnconfigure(0, weight=1)

        # self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        # Tree view frame
        tree_view_frame = TreeViewFrame(self)
        tree_view_frame.grid(column=0, row=0, sticky="nsew")

        # Buttons frame
        buttons_frame = ButtonsFrame(self, tree_view_frame)
        buttons_frame.grid(column=0, row=1, sticky='nsew')


if __name__ == "__main__":
    app = App()
    app.mainloop()
