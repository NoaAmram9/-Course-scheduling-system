from PyQt5.QtWidgets import QMessageBox
from SRC.ViewLayer.View.main_page_qt5 import MainPageQt5
from SRC.Models.ValidationError import ValidationError
import os
import shutil

class LandPageController:
    def __init__(self, view, controller):
        self.view = view
        self.controller = controller
        self.file_uploaded = False

        # Connect buttons and signals
        self.view.upload_button.clicked.connect(self.upload_file)
        self.view.send_button.clicked.connect(self.send_action)
        self.view.file_uploaded.connect(self.handle_uploaded_file)

    def handle_uploaded_file(self, path):
        if not path.endswith(".txt"):
            QMessageBox.critical(self.view, "Invalid file", "Only .txt files are allowed.")
            return

        try:
            save_dir = os.path.join(os.path.dirname(__file__),'..' ,'..', '..', 'Data')
            os.makedirs(save_dir, exist_ok=True)
            dest_path = os.path.join(save_dir, "courses.txt")
            shutil.copy(path, dest_path)
            self.view.file_label.setText(f"Uploaded: {os.path.basename(path)}")
            self.file_uploaded = True
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Failed to save file:\n{str(e)}")

    def upload_file(self):
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Select .txt File", "", "Text Files (*.txt)")
        if file_path:
            self.handle_uploaded_file(file_path)

    def send_action(self):
        if not self.file_uploaded:
            QMessageBox.warning(self.view, "Missing File", "Please upload a .txt file before proceeding.")
            return

        data = self.controller.process_repository_file("Data/courses.txt")
        if all(isinstance(x, ValidationError) for x in data):
            error_messages = "\n".join(str(error) for error in data)
            QMessageBox.warning(self.view, "Invalid Course File", f"The following errors were found:\n\n{error_messages}")
            return

        
        # Close current view
        self.view.close()
        
        # Create and show the main page
        self.main_page = MainPageQt5(self.controller)
        self.main_page.show()  # Use show() instead of run() for Qt5 widgets
        
        # Optional: Set window properties
        self.main_page.setWindowTitle("Main Page")
        self.main_page.resize(800, 600)  # Set appropriate size
