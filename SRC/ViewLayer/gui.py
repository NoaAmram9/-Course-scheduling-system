import tkinter as tk
from tkinter import filedialog, messagebox
from SRC.Controller.Controller import ScheduleController

class CourseSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Scheduling System")
        self.controller = ScheduleController()

        # כפתור לבחירת קובץ קורסים
        self.label = tk.Label(root, text="בחר קובץ קורסים:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="בחר קובץ", command=self.load_file)
        self.select_button.pack()

        # כפתור ליצירת מערכות שעות
        self.run_button = tk.Button(root, text="הפק מערכות שעות", command=self.generate_schedule)
        self.run_button.pack(pady=10)

        # כפתור לשמירת קובץ פלט
        self.save_button = tk.Button(root, text="שמור תוצאה", command=self.save_file, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.selected_file = None
        self.generated_schedules = None

    def load_file(self):
        """ פונקציה לטעינת קובץ קורסים """
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.selected_file = file_path
            messagebox.showinfo("טעינת קובץ", f"קובץ נטען בהצלחה: {file_path}")

    def generate_schedule(self):
        """ פונקציה שמפעילה את יצירת מערכות השעות """
        if not self.selected_file:
            messagebox.showwarning("שגיאה", "אנא בחר קובץ קורסים תחילה!")
            return

        # יצירת מערכות שעות דרך הקונטרולר
        self.generated_schedules = self.controller.generate_schedules(self.selected_file)

        if self.generated_schedules:
            messagebox.showinfo("הצלחה", "מערכות השעות נוצרו בהצלחה!")
            self.save_button.config(state=tk.NORMAL)  # מפעיל את כפתור השמירה
        else:
            messagebox.showerror("שגיאה", "נכשלה יצירת מערכות שעות.")

    def save_file(self):
        """ פונקציה לשמירת הקובץ עם מערכות השעות """
        if not self.generated_schedules:
            messagebox.showwarning("שגיאה", "אין מערכות שעות לשמור!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.writelines(self.generated_schedules)
            messagebox.showinfo("שמירה", f"הקובץ נשמר בהצלחה: {file_path}")

