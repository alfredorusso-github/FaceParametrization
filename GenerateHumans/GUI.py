import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from HumanGenerator import HumanGenerator
from ttkwidgets import CheckboxTreeview

h = HumanGenerator()

class TreeViewFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        self.grid(padx=10, pady=10)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Introduction label
        ttk.Label(self, text='Select parameters').grid(column=0, row=0, sticky='W', padx=10, pady=10)

        # Treeview
        self.tree = CheckboxTreeview(self, show="tree")

        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        id = len(h.paramsDict)
        for i, (key, values) in enumerate(h.paramsDict.items()):
            self.tree.insert('', tk.END, text=key, open=False, iid=i)

            for value in values:
                self.tree.insert('', tk.END, text=value, iid=id)
                self.tree.move(id, i, 0)
                id = id + 1

    def printChecked(self):
        for item in self.tree.get_checked():
            print(self.tree.item(item)['text'])
        
        print('-' * 50)

class ButtonsFrame(ttk.Frame):
    def __init__(self, container, treeviewframe):
        super().__init__(container)

        self.treeViewFrame = treeviewframe

        self.grid(padx=10, pady=10)
        
        self.columnconfigure(2, weight=4)

        # Slider stuff
        ttk.Label(self, text='Select step range:').grid(column=0, row=0, sticky='w', padx=10)

        self.current_value = tk.DoubleVar(value=0.25)
        ttk.Scale(self, from_=0, to=1, orient='horizontal', variable=self.current_value, command=self.changeValue, length=200).grid(column=1, row=0, sticky='w')

        self.valueLabel = ttk.Label(self, text=self.current_value.get())
        self.valueLabel.grid(column=2, row=0, sticky='w', padx=5)

        # Run button
        ttk.Button(self, text='Run', width=10, command=self.__start).grid(column=0, row=1, sticky='se', padx=10, pady=5, columnspan=3)

    def changeValue(self, event):
        self.valueLabel.configure(text=self.getValue(float(event)))

    def getValue(self, value):
        rounded = round(value, 2)
        return f"{rounded:.2f}"

    def __start(self):
        # setting choices made
        tree = self.treeViewFrame.tree

        h.choices = [tree.item(tree.parent(item))['text'] + "/" + tree.item(item)['text'] for item in self.treeViewFrame.tree.get_checked()]
        # print(h.choices)

        # setting step size
        h.step = round(self.current_value.get(), 2) * 100

        h.createHuman()

class App(tk.Tk):
    window_width = 800
    window_height = 600

    def __init__(self):
        super().__init__()

        # setting title
        self.title("Human Generator")

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width/2 - self.window_width / 2)
        center_y = int(screen_height/2 - self.window_height / 2)

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
        treeViewFrame = TreeViewFrame(self)
        treeViewFrame.grid(column=0, row=0, sticky="nsew")

        # Buttons frame
        buttonsFrame = ButtonsFrame(self, treeViewFrame)
        buttonsFrame.grid(column=0, row=1, sticky='nsew')

if __name__ == "__main__":
    app = App()
    app.mainloop()