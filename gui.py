import tkinter as tk
from PIL import ImageTk

import stereogram
import maps

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stereogram Generator")
        self.root.geometry("1200x750")
        self.root.resizable(True, True)
        #self.root.configure(bg="grey")

        # init eye separation
        self.eye_sep = 60

        #for flagging if a map has been selected
        self.map_selected = False

        #title of App
        title = tk.Label(
            self.root,
            text="Stereogram Generator",
            font=("Arial", 20),
            fg = "blue"
        )
        title.pack(padx=20, pady=10)

        # dropdown to pick which depth map to generate from
        self.map_functions = maps.available_maps
        self.map_options = ["--Choose a map--"] + list(self.map_functions.keys())
        self.selected_map_name = tk.StringVar(self.root)
        self.selected_map_name.set(self.map_options[0])

        self.map_menu = tk.OptionMenu(self.root, self.selected_map_name, *self.map_options)
        self.map_menu.pack()

        #button to run the program to generate image
        run_button = tk.Button(
            self.root,
            text="generate stereogram",
            command=self.generate_and_display
        )
        run_button.pack(pady=10)

        # scale to change eye separation
        self.eye_sep_slider = tk.Scale(
            self.root,
            from_=20,
            to=200,
            orient=tk.HORIZONTAL,
            label="eye separation",
            command=self.on_slider_change
        )
        self.eye_sep_slider.set(self.eye_sep)
        self.eye_sep_slider.pack()

        # draw the image onto gui?
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)





    def generate_and_display(self):

        selected_name = self.selected_map_name.get()
        if selected_name == "--Choose a map--":
            return

        depth_map_function = self.map_functions[selected_name]

        width = 800
        height = 600

        depth_map = depth_map_function(width=width, height=height)

        image = stereogram.generate_sirds(depth_map=depth_map, eye_sep=self.eye_sep)
        self.photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.photo)

    def on_slider_change(self, value):
        if self.selected_map_name.get() == "--Choose a map--":
            return
        self.eye_sep = int(value)
        self.generate_and_display()

    def on_map_selected(self, *args):
        self.map_selected = True






    def run(self):
        self.root.mainloop()
