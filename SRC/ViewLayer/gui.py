import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from SRC.ViewLayer.Layout.MainPage import MainPage

class GUI:
    def __init__(self, controller):
        self.controller = controller
        
        # Creat Tkinter
        self.window = tk.Tk()
        self.window.title("System Scheduler")
        self.window.geometry("400x300")  # window size
        self.window.config(bg="#B6B6B4")  # colore
        # buttoms to load files
        self.load_button = tk.Button(self.window, text="Load file", command=self.load_file)
        self.load_button.pack(pady=10)
        self.load_chosen_courses_button = tk.Button(self.window, text="Load chosen courses file", command=self.load_chosen_courses_file)
        self.load_chosen_courses_button.pack(pady=10)
        
        # create button too create schedule
        self.select_button = tk.Button(self.window, text="Generate Schedule", command=self.select_courses)
        self.select_button.pack(pady=10)

        # create button to go to main page
        self.open_main_button = tk.Button(self.window, text="Open Course Selector", command=self.open_main_page)
        self.open_main_button.pack(pady=10)
        
        
    def load_file(self):
        #load file to the system
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    
        if file_path:
            try:
                # Define the destination directory in your project
                save_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'Data')
                os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists

                # Get the filename and define the destination path
                filename = "courses.txt"
                destination_path = os.path.join(save_dir, filename)

                # Copy the file to the project folder
                shutil.copy(file_path, destination_path)

                messagebox.showinfo("Success", f"File saved and loaded successfully:\n{destination_path}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def load_chosen_courses_file(self):
       #load file to the system
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

        if file_path:
            try:
                # Define the destination directory in your project
                save_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'Data')
                os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists
                # Get the filename and define the destination path
                filename = "chosen_courses.txt"
                destination_path = os.path.join(save_dir, filename)
                # Copy the file to the project folder
                shutil.copy(file_path, destination_path)
                messagebox.showinfo("Success", f"File saved and loaded successfully:\n{destination_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def select_courses(self):
      # send to controller to select courses   
        # שלח את הקורסים שנבחרו ל-Controller להמשך עיבוד
        self.controller.run("Data/courses.txt", "Data/chosen_courses.txt")
 
    def open_main_page(self):
        self.window.destroy()  # סגור את מסך הנחיתה
        main_page = MainPage(self.controller)
        main_page.run()  # הפעל את מסך הקורסים
 
 
    def run(self):
      # start the GUI loop
        self.window.mainloop()