import tkinter as tk
from PIL import ImageTk

import stereogram
import maps
import noise


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stereogram Generator")
        self.root.geometry("1200x750")
        self.root.resizable(True, True)


        # init eye separation
        self.eye_sep = 60

        #for flagging if a map has been selected
        self.map_selected = False

        #title of App
        title = tk.Label(
            self.root,
            text="Stereogram Generator",
            font=("Arial", 25),
            fg = "black"
        )
        title.pack(padx=20, pady=10)

        # frame for generation option buttons/dropdowns/etc
        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack()

        # dropdown to pick which depth map to generate from
        self.map_functions = maps.available_maps
        self.map_options = ["--Choose a map--"] + list(self.map_functions.keys())
        self.selected_map_name = tk.StringVar(self.root)
        self.selected_map_name.set(self.map_options[0])

        self.map_menu = tk.OptionMenu(self.options_frame, self.selected_map_name, *self.map_options)
        self.map_menu.pack(side=tk.LEFT, padx=10)

        #dropdown to pick which noise algorithm to use
        self.noise_pattern = noise.available_patterns
        self.noise_options = ["--Choose a pattern--"] + list(self.noise_pattern.keys())
        self.selected_pattern_name = tk.StringVar(self.root)
        self.selected_pattern_name.set(self.noise_options[0])

        self.noise_menu = tk.OptionMenu(self.options_frame, self.selected_pattern_name, *self.noise_options)
        self.noise_menu.pack(side=tk.LEFT, padx=10)

        #nested frame for slider label placement
        self.slider_frame = tk.Frame(self.options_frame)
        self.slider_frame.pack(side=tk.LEFT, padx=10)

        # scale to change eye separation
        self.eye_sep_slider = tk.Scale(
            self.slider_frame,
            from_=20,
            to=200,
            orient=tk.HORIZONTAL,
            command=self.on_slider_change
        )
        self.eye_sep_slider.set(self.eye_sep)
        self.eye_sep_slider.pack()

        self.slider_label = tk.Label(self.slider_frame, text="Pattern Width")
        self.slider_label.pack()

        #button to run the program to generate the image
        run_button = tk.Button(
            self.root,
            text="Generate",
            command=self.generate_and_display
        )
        run_button.pack(pady=10)


        # draw the image onto gui
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)





    def generate_and_display(self):

        selected_map = self.selected_map_name.get()
        if selected_map == "--Choose a map--":
            return

        depth_map_function = self.map_functions[selected_map]

        selected_pattern_name = self.selected_pattern_name.get()
        if selected_pattern_name == "--Choose a pattern--":
            return
        noise_pattern = noise.available_patterns[selected_pattern_name]

        width = 800
        height = 600

        depth_map = depth_map_function(width=width, height=height)

        image = stereogram.generate_sirds(
            depth_map=depth_map,
            eye_sep=self.eye_sep,
            noise_pattern=noise_pattern,
        )


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
