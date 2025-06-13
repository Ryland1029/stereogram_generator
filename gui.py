import tkinter as tk
from tkinter import Tk, Label, Button, Entry, Text, Frame, Checkbutton, Radiobutton, Scale, Listbox, Scrollbar, Canvas, StringVar, IntVar

from PIL import ImageTk

from stereogram import generate_sirds

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stereogram Generator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        #self.root.configure(bg="grey")

        #title of App
        title = tk.Label(
            self.root,
            text="Stereogram Generator",
            font=("Arial", 20),
            fg = "blue"
        )
        title.pack(padx=20, pady=10)

        #button to run the program to generate image
        run_button = tk.Button(
            self.root,
            text="generate stereorgram",
            command=self.generate_and_display
        )
        run_button.pack(pady=10)

        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

    def generate_and_display(self):
        image = generate_sirds()
        self.photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.photo)

    def run(self):
        self.root.mainloop()
