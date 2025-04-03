import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class GUI:
    def __init__(self, controller):
        self.controller = controller
        
        # יצירת חלון Tkinter
        self.window = tk.Tk()
        self.window.title("System Scheduler")
        self.window.geometry("400x300")  # גודל החלון
        self.window.config(bg="#B6B6B4")  # צבע 
        # יצירת כפתור לטעינת קובץ
        self.load_button = tk.Button(self.window, text="Load file", command=self.load_file)
        self.load_button.pack(pady=10)
        self.load_chosen_courses_button = tk.Button(self.window, text="Load chosen courses file", command=self.load_chosen_courses_file)
        self.load_chosen_courses_button.pack(pady=10)
        
        # יצירת ComboBox להציג את הקורסים
        self.course_combobox = ttk.Combobox(self.window, state="readonly")
        self.course_combobox.pack(pady=10)
        
        # יצירת כפתור לאישור בחירת קורסים
        self.select_button = tk.Button(self.window, text="Select Courses", command=self.select_courses)
        self.select_button.pack(pady=10)
        
    # def load_file(self):
    #     """ פותח חלון קובץ וטעינת הקובץ למערכת """
    #     file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        
    #     if file_path:
    #         try:
    #             # שלח את הקובץ ל-Controller למיפוי לאובייקטים
    #             self.controller.process_file(file_path)
    #             messagebox.showinfo("Success", "File loaded successfully.")
                
    #             # לאחר שהקובץ נטען, הצג את הקורסים ב-ComboBox
    #             courses = self.controller.get_courses()
    #             self.course_combobox['values'] = courses
    #         except Exception as e:
    #             messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def load_file(self):
        """ פותח חלון קובץ וטעינת הקובץ למערכת """   
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
        """ פותח חלון קובץ וטעינת הקובץ למערכת """   
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
        """ שולח את הקורסים שנבחרו ל-Controller """
        # selected_courses = self.course_combobox.get()
        # if not selected_courses:
        #     messagebox.showwarning("Warning", "Please select courses.")
        #     return
        
        # שלח את הקורסים שנבחרו ל-Controller להמשך עיבוד
        self.controller.run("Data/courses.txt", "Data/chosen_courses.txt")
 
    def run(self):
        """ הפעלת חלון Tkinter """
        self.window.mainloop()