import cv2
import numpy as np
from tkinter import filedialog, Tk, messagebox
import tkinter as tk
from highpass import *
from lowpass import *

def option_selected(option):
    if option == "highpass":
        hpmain()
    elif option == "lowpass":
        lpmain()
    else:
        messagebox.showinfo("Option Selected", "No image chosen")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Highpass and Lowpass Filter Tool")

    # Function to handle option selection
    def choose_option(option):
        option_selected(option)

    # Create and configure buttons for options
    option1_btn = tk.Button(root, text="Highpass Filter", command=lambda: choose_option("highpass"))
    option1_btn.pack(pady=50)

    option2_btn = tk.Button(root, text="Lowpass Filter", command=lambda: choose_option("lowpass"))
    option2_btn.pack(pady=50)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
