import tkinter as tk
from tkinter import ttk
import sv_ttk

from PIL import ImageTk, Image
import time

import stereogram
import maps
import noise
import coloring

class App:
    def __init__(self):
        self.root = tk.Tk()
        sv_ttk.set_theme("dark")
        self.root.title("Stereogram Generator")
        self.root.geometry("1050x700")
        self.root.resizable(True, True)

        # init pattern width
        self.pattern_width = 60

        #title of App
        title = ttk.Label(
            self.root,
            text="Stereogram Generator",
            font=("Arial", 25),
            #fg = "maroon"
        )
        title.pack()

        # frame for generation option buttons/dropdowns/etc
        self.options_frame = ttk.Frame(self.root)
        self.options_frame.pack( anchor="nw", pady=50)

        # dropdown to pick which depth map to generate from
        self.map_functions = maps.available_maps
        self.map_options = ["--Choose map--"] + list(self.map_functions.keys())
        self.selected_map_name = tk.StringVar(self.root)
        self.selected_map_name.set(self.map_options[0])

        self.map_menu = ttk.OptionMenu(self.options_frame, self.selected_map_name, *self.map_options)
        self.map_menu.pack(anchor="w", padx=10, pady=10)

        #dropdown to pick which noise algorithm to use
        self.noise_pattern = noise.available_patterns
        self.noise_options = ["--Choose pattern--"] + list(self.noise_pattern.keys())
        self.selected_pattern_name = tk.StringVar(self.root)
        self.selected_pattern_name.set(self.noise_options[0])

        self.noise_menu = ttk.OptionMenu(self.options_frame, self.selected_pattern_name, *self.noise_options)
        self.noise_menu.pack(anchor="w", padx=10)

        #nested frame for slider/label placement
        self.slider_frame = ttk.Frame(self.options_frame)
        self.slider_frame.pack(anchor = "w", padx=20, pady=10)

        # slider scale to change pattern width
        self.pattern_width_slider = ttk.Scale(
            self.slider_frame,
            from_=20,
            to=200,
            orient=tk.HORIZONTAL,
            command=self.on_slider_change
        )
        self.pattern_width_slider.set(self.pattern_width)
        self.pattern_width_slider.pack()

        self.slider_label = ttk.Label(self.slider_frame, text="Pattern Width")
        self.slider_label.pack()

        # color options dropdown menu
        self.coloring_type = coloring.available_color_options
        self.color_options = ["--Choose color--"] + list(self.coloring_type.keys())
        self.selected_color_option = tk.StringVar(self.root)
        self.selected_color_option.set(self.color_options[0])
        self.selected_color_option.trace("w", self.update_hue_slider_visibility)

        self.color_menu = ttk.OptionMenu(self.options_frame, self.selected_color_option, *self.color_options)
        self.color_menu.pack(anchor="w", padx=10, pady=10)

        # slider to change hue in-app if sat option picked

        # nested frame for hue slider/label placement
        self.hue_slider_frame = ttk.Frame(self.options_frame)
        self.hue_slider_frame.pack(anchor = "w", padx=20)

        self.hue_var = tk.DoubleVar(value = 0.6)
        self.hue_slider = ttk.Scale(
            self.hue_slider_frame,
            from_ = 0,
            to = 1.0,
            #resolution = 0.01,
            orient = tk.HORIZONTAL,
            variable=self.hue_var,
        )
        self.hue_slider.pack()

        self.hue_label = ttk.Label(self.hue_slider_frame, text="Hue")
        self.hue_label.pack()
        self.update_hue_slider_visibility()

        # frma for gen button and benchmark (bottom left of app)
        self.gen_frame = ttk.Frame(self.root)
        self.gen_frame.pack(side=tk.LEFT, anchor="sw", padx=10, pady=10)

        #button to run the program to generate the image
        run_button = ttk.Button(
            self.gen_frame,
            text="Generate (Enter)",
            #bg="white",
            command=self.generate_and_display
        )
        run_button.pack(anchor="sw", padx=10, pady=10)
        # bind ENTER key to also run the button
        self.root.bind("<Return>", lambda event: self.generate_and_display())

        # time it took to generate image
        self.gen_time_label = ttk.Label(self.gen_frame, text="", font=("Arial", 10))
        self.gen_time_label.pack(anchor="sw", padx=10)

        # toggle light vs dark theme
        self.theme_button = ttk.Button(self.root, text="Theme", command=sv_ttk.toggle_theme)
        self.theme_button.place(x=80,y=10)

        # button to reset the app
        reset_button = ttk.Button(self.root, text="Reset", command=self.reset_app)
        reset_button.place(x=10,y=10)

        # draw the image onto gui
        self.image_label = tk.Label(self.root)
        self.image_label.place(x=225, y=80)



    def generate_and_display(self):
        start_time = time.perf_counter()

        # define which map to use
        selected_map = self.selected_map_name.get()
        if selected_map == "--Choose map--":
            return
        depth_map_function = self.map_functions[selected_map]

        #define which noise type to use
        selected_pattern_name = self.selected_pattern_name.get()
        if selected_pattern_name == "--Choose pattern--":
            return
        noise_pattern = noise.available_patterns[selected_pattern_name]

        #define which color option to use, if any
        selected_color_option = self.selected_color_option.get()
        if selected_color_option == "--Choose color--":
            return
        color_option = coloring.available_color_options[selected_color_option]

        width = 800
        height = 600

        depth_map = depth_map_function(width=width, height=height)

        #linking all the args for the stereogram function
        image = stereogram.generate_sirds(
            depth_map=depth_map,
            pattern_width=self.pattern_width,
            noise_pattern=noise_pattern,
            color_option=color_option,
            hue=self.hue_var.get(),
        )
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        self.gen_time_label.config(text=f" generated in: \n {elapsed_time:.3f} sec")

        # put the image in the gui
        self.photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.photo)


    def on_slider_change(self, value):
        if self.selected_map_name.get() == "--Choose map--":
            return
        self.pattern_width = int(float(value))
        # this auto-updates the image during sliding
        ### self.generate_and_display()

    def update_hue_slider_visibility(self, *args):
        if not hasattr(self, 'hue_slider'):
            return
        if self.selected_color_option.get() == "single hue":
            self.hue_slider.configure(state="normal")
            #self.hue_label.configure(fg="black")
        else:
            self.hue_slider.configure(state="disabled")
            #self.hue_label.configure(fg="gray")

    def reset_app(self):
        self.selected_map_name.set(self.map_options[0])
        self.selected_pattern_name.set(self.noise_options[0])
        self.pattern_width_slider.set(self.pattern_width)
        self.selected_color_option.set(self.color_options[0])
        self.hue_slider.set(0.6)
        self.image_label.config(image="")
        self.gen_time_label.config(text="")


    def run(self):
        self.root.mainloop()
