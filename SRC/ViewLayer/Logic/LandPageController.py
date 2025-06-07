from PyQt5.QtWidgets import QMessageBox
from SRC.ViewLayer.View.main_page_qt5 import MainPageQt5
from SRC.Models.ValidationError import ValidationError
import os
import shutil
from SRC.Controller.FileController import FileController
class LandPageController:
    def __init__(self, view):
        self.view = view
        self.file_controller = None  # יאותחל לפי סוג הקובץ
        
        self.file_uploaded = False
        self.uploaded_path = None
        self.Data = None
        # Connect buttons and signals
        self.view.upload_button.clicked.connect(self.upload_file)
        self.view.send_button.clicked.connect(self.send_action)
        self.view.file_uploaded.connect(self.handle_uploaded_file)

    def handle_uploaded_file(self, path):
        # בדיקת סיומת קובץ
        if not path.endswith((".txt", ".xlsx")):
            QMessageBox.critical(self.view, "Invalid file", "Only .txt or .xlsx files are allowed.")
            return

        try:
            save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Data')
            os.makedirs(save_dir, exist_ok=True)

            # קבלת הסיומת
            extension = os.path.splitext(path)[1]
            
            # יצירת קונטרולר לפי סוג הקובץ
            
            self.file_controller = FileController(extension)
            
            # יצירת נתיב יעד
            dest_path = os.path.join(save_dir, f"courses{extension}")
            
            # העתקת הקובץ
            shutil.copy(path, dest_path)
            
           
            
            # עדכון UI
            self.view.file_label.setText(f"Uploaded: {os.path.basename(path)}")
            self.uploaded_path = dest_path
            
            self.file_uploaded = True
            
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Failed to save file:\n{str(e)}")

    def upload_file(self):
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Select .txt or .xlsx File",
            "",
            "Supported Files (*.txt *.xlsx)"
        )
        if file_path:
            self.handle_uploaded_file(file_path)
    def send_action(self):
        if not self.file_uploaded:
            QMessageBox.warning(self.view, "Missing File", "Please upload a .txt or .xlsx file before proceeding.")
            return

        if not self.file_controller:
            QMessageBox.critical(self.view, "Error", "File controller not initialized.")
            return

        try:
            courses, errors = self.file_controller.read_courses_from_file(self.uploaded_path)
             # הוספת קוד לחילוץ שני החלקים האחרונים של הנתיב
            from pathlib import Path
            last_two_parts = Path(self.uploaded_path).parts[-2:]
            filePath = os.path.join(*last_two_parts)
            unix_style_path = filePath.replace("\\", "/")
            if errors:
                error_messages = "\n".join(str(error) for error in errors)
                QMessageBox.warning(self.view, "Invalid Course File", f"The following errors were found:\n\n{error_messages}")
                return

            self.view.close()
            self.Data = courses
           
            self.main_page = MainPageQt5(self.Data, self.file_controller,unix_style_path)
            self.main_page.show()
            self.main_page.setWindowTitle("Main Page")
            self.main_page.resize(800, 600)

        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Failed to process file:\n{str(e)}")

    # def send_action(self):
    #     if not self.file_uploaded:
    #         QMessageBox.warning(self.view, "Missing File", "Please upload a .txt or .xlsx file before proceeding.")
    #         return

    #     if not self.file_controller:
    #         QMessageBox.critical(self.view, "Error", "File controller not initialized.")
    #         return

    #     # קריאת הקורסים מהקובץ
    #     try:
    #         data = self.file_controller.read_courses_from_file(self.uploaded_path)
    #         print(f"Data read from file:11111111111111111")
    #         # בדיקת שגיאות validation
    #         if all(isinstance(x, ValidationError) for x in data):
    #             error_messages = "\n".join(str(error) for error in data)
    #             QMessageBox.warning(self.view, "Invalid Course File", f"The following errors were found:\n\n{error_messages}")
    #             return
    #         print(f"Data read from file: 2222222222222222")
    #         # סגירת החלון הנוכחי ופתיחת הדף הראשי
    #         self.view.close()

    #         self.main_page = MainPageQt5(self.file_controller)
    #         self.main_page.show()
    #         self.main_page.setWindowTitle("Main Page")
    #         self.main_page.resize(800, 600)
            
    #     except Exception as e:
    #         QMessageBox.critical(self.view, "Error", f"Failed to process file:\n{str(e)}")