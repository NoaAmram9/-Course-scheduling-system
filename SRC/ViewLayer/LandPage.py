import os
import shutil
import customtkinter as ctk
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, messagebox
from SRC.ViewLayer.Layout.MainPage import MainPage

class LandPage:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.file_uploaded = False
        self.file_label = None  # Label to show uploaded file name
        self.root.title("Schedule System Creator")
        self.root.geometry("600x600")
        self.root.config(bg="#FAFAFA")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.build_ui()

    def build_ui(self):
        # === HEADER ===
        header = ctk.CTkLabel(
            self.root,
            text="WELCOME TO SCHEDUAL SYSTEM CREATOR",
            font=("Helvetica", 20, "bold"),
            text_color="#000",
            fg_color="#F1F1F1",
            corner_radius=10,
            height=50
        )
        header.pack(pady=(30, 20), padx=40, fill="x")

        # === UPLOAD AREA ===
        self.drop_area = ctk.CTkFrame(
            self.root,
            fg_color="#FFFFFF",
            border_color="#BBBBBB",
            border_width=1,
            corner_radius=12,
            width=400,
            height=200
        )
        self.drop_area.pack(pady=40)
        self.drop_area.pack_propagate(False)

        self.drop_label = ctk.CTkLabel(
            self.drop_area,
            text="You can drag a .txt file here\nor upload a file.",
            font=("Helvetica", 14),
            text_color="#777"
        )
        self.drop_label.pack(pady=10)

        # Enable drag-and-drop
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.handle_drop)

        # === UPLOAD BUTTON ===
        self.upload_button = ctk.CTkButton(
            self.drop_area,
            text="UPLOAD",
            font=("Helvetica", 14, "bold"),
            fg_color="#FFFDD0",
            text_color="black",
            hover_color="#FFFACD",
            corner_radius=20,
            command=self.upload_file
        )
        self.upload_button.pack(pady=10)
        # === FILE NAME LABEL (below drop area) ===
        self.file_label = ctk.CTkLabel(
            self.root,
            text="",
            font=("Helvetica", 12),
            text_color="#444"
        )
        self.file_label.pack(pady=(0, 10))
  
        # === SEND BUTTON ===
        self.send_button = ctk.CTkButton(
            self.root,
            text="SEND.",
            font=("Helvetica", 14, "bold"),
            fg_color="#FDECEC",
            text_color="black",
            hover_color="#FCDCDC",
            corner_radius=20,
            command=self.send_action,
            width=100
        )
        self.send_button.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

    def handle_drop(self, event):
     file_path = event.data.strip("{}")

     if not file_path.endswith(".txt"):
        messagebox.showerror("Invalid file", "Only .txt files are allowed.")
        return

     try:
        # Define the destination directory relative to project structure
        save_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'Data')
        os.makedirs(save_dir, exist_ok=True)

        # Set a fixed name for the saved file
        filename = "courses.txt"
        destination_path = os.path.join(save_dir, filename)

        # Copy the dragged file into your project
        shutil.copy(file_path, destination_path)
        self.file_label.configure(text=f"Uploaded: {os.path.basename(file_path)}")
        self.file_uploaded = True
        
        messagebox.showinfo("Success", f"File saved and loaded successfully:\n{destination_path}")

     except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

    def upload_file(self):
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
                self.file_label.configure(text=f"Uploaded: {os.path.basename(file_path)}")
                self.file_uploaded = True
                

                messagebox.showinfo("Success", f"File saved and loaded successfully:\n{destination_path}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def send_action(self):
     if not self.file_uploaded:
        messagebox.showwarning("Missing File", "Please upload a .txt file before proceeding.")
        return
     self.root.withdraw()  # Hide the window instead of destroying it
     main_page = MainPage(self.controller)
     main_page.run()



    def run(self):
        self.root.mainloop()
   
