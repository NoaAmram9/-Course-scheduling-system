# from PyQt5.QtWidgets import QMessageBox
# from SRC.ViewLayer.View.main_page_qt5 import MainPageQt5
# from SRC.Models.ValidationError import ValidationError
# import os
# import shutil
# from SRC.Controller.FileController import FileController
# from pathlib import Path
# class LandPageController:
#     def __init__(self, view):
#         self.view = view
#         self.file_controller = None     # FileController instance
        
#         self.file_uploaded = False
#         self.uploaded_path = None
#         self.Data = None
#         # Connect buttons and signals
#         self.view.upload_button.clicked.connect(self.upload_file)
#         self.view.send_button.clicked.connect(self.send_action)
#         self.view.file_uploaded.connect(self.handle_uploaded_file)

#     def handle_uploaded_file(self, path):
#         #check if the path is valid
#         if not path.endswith((".txt", ".xlsx")):
#             QMessageBox.critical(self.view, "Invalid file", "Only .txt or .xlsx files are allowed.")
#             return

#         try:
#             save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Data')
#             os.makedirs(save_dir, exist_ok=True)

#             # get the file extension
#             extension = os.path.splitext(path)[1]
            
#             # create the destination path
#             dest_path = os.path.join(save_dir, f"courses{extension}")
            
#             # copy the file to the destination
#             shutil.copy(path, dest_path)
#             self.uploaded_path = dest_path
#             last_two_parts = Path(self.uploaded_path).parts[-2:]
#             filePath = os.path.join(*last_two_parts)
#             unix_style_path = filePath.replace("\\", "/")
#             # create the file controller with the correct file type
#             self.file_controller = FileController(extension, unix_style_path)
            
#             # update the view to show the uploaded file
#             self.view.file_label.setText(f"Uploaded: {os.path.basename(path)}")
            
            
#             self.file_uploaded = True
            
#         except Exception as e:
#             QMessageBox.critical(self.view, "Error", f"Failed to save file:\n{str(e)}")

#     def upload_file(self):
#         from PyQt5.QtWidgets import QFileDialog
#         file_path, _ = QFileDialog.getOpenFileName(
#             self.view,
#             "Select .txt or .xlsx File",
#             "",
#             "Supported Files (*.txt *.xlsx)"
#         )
#         if file_path:
#             self.handle_uploaded_file(file_path)
#     def send_action(self):
#         if not self.file_uploaded:
#             QMessageBox.warning(self.view, "Missing File", "Please upload a .txt or .xlsx file before proceeding.")
#             return

#         if not self.file_controller:
#             QMessageBox.critical(self.view, "Error", "File controller not initialized.")
#             return

#         try:
#             courses, errors = self.file_controller.read_courses_from_file(self.uploaded_path)
#              # add the last two parts of the path to the filePath
           
#             last_two_parts = Path(self.uploaded_path).parts[-2:]
#             filePath = os.path.join(*last_two_parts)
#             unix_style_path = filePath.replace("\\", "/")
#             if errors:
#                 error_messages = "\n".join(str(error) for error in errors)
#                 QMessageBox.warning(self.view, "Invalid Course File", f"The following errors were found:\n\n{error_messages}")
#                 return

#             self.view.close()
#             self.Data = courses
           
#             self.main_page = MainPageQt5(self.Data, self.file_controller,unix_style_path)
#             self.main_page.show()
#             self.main_page.setWindowTitle("Main Page")
#             self.main_page.resize(800, 600)

#         except Exception as e:
#             QMessageBox.critical(self.view, "Error", f"Failed to process file:\n{str(e)}")
######################################
















#######################################

# from PyQt5.QtWidgets import QMessageBox
# from SRC.ViewLayer.View.main_page_qt5 import MainPageQt5
# from SRC.Models.ValidationError import ValidationError
# import os
# import shutil
# from SRC.Controller.FileController import FileController
# from pathlib import Path

# class LandPageController:
#     def __init__(self, view):
#         self.view = view
#         self.file_controller = None
        
#         self.file_uploaded = False
#         self.uploaded_path = None
#         self.Data = None
        
#         # Connect buttons and signals
#         self.view.upload_button.clicked.connect(self.upload_file)
#         self.view.send_button.clicked.connect(self.send_action)
#         self.view.file_uploaded.connect(self.handle_uploaded_file)

#     def handle_uploaded_file(self, path):
#         self.clear_database_on_new_upload()
#         # Check if the path is valid
#         if not path.endswith((".txt", ".xlsx")):
#             QMessageBox.critical(self.view, "Invalid file", "Only .txt or .xlsx files are allowed.")
#             return

#         try:
#             save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Data')
#             os.makedirs(save_dir, exist_ok=True)

#             # Get the file extension
#             extension = os.path.splitext(path)[1]
            
#             # Create the destination path
#             dest_path = os.path.join(save_dir, f"courses{extension}")
            
#             # Copy the file to the destination
#             shutil.copy(path, dest_path)
#             self.uploaded_path = dest_path
            
#             last_two_parts = Path(self.uploaded_path).parts[-2:]
#             filePath = os.path.join(*last_two_parts)
#             unix_style_path = filePath.replace("\\", "/")
            
#             # Create the file controller with database enabled
#             self.file_controller = FileController(extension, unix_style_path, use_database=True)
            
#             # Update the view to show the uploaded file
#             self.view.file_label.setText(f"Uploaded: {os.path.basename(path)}")
            
#             self.file_uploaded = True
            
#         except Exception as e:
#             QMessageBox.critical(self.view, "Error", f"Failed to save file:\n{str(e)}")

#     def upload_file(self):
#         from PyQt5.QtWidgets import QFileDialog
#         file_path, _ = QFileDialog.getOpenFileName(
#             self.view,
#             "Select .txt or .xlsx File",
#             "",
#             "Supported Files (*.txt *.xlsx)"
#         )
#         if file_path:
#             self.handle_uploaded_file(file_path)
    
#     def send_action(self):
#         self.clear_database_on_new_upload()
#         if not self.file_uploaded:
#             QMessageBox.warning(self.view, "Missing File", "Please upload a .txt or .xlsx file before proceeding.")
#             return

#         if not self.file_controller:
#             QMessageBox.critical(self.view, "Error", "File controller not initialized.")
#             return

#         try:
#             # Read courses from file and import to database
#             courses, errors = self.file_controller.read_courses_from_file(self.uploaded_path)
            
#             last_two_parts = Path(self.uploaded_path).parts[-2:]
#             filePath = os.path.join(*last_two_parts)
#             unix_style_path = filePath.replace("\\", "/")
            
#             if errors:
#                 error_messages = "\n".join(str(error) for error in errors)
#                 QMessageBox.warning(self.view, "Invalid Course File", f"The following errors were found:\n\n{error_messages}")
#                 return

           

#             self.view.close()
#             self.Data = courses
           
#             self.main_page = MainPageQt5(self.Data, self.file_controller, unix_style_path)
#             self.main_page.show()
#             self.main_page.setWindowTitle("Main Page")
#             self.main_page.resize(800, 600)

#         except Exception as e:
#             QMessageBox.critical(self.view, "Error", f"Failed to process file:\n{str(e)}")
    
#     def clear_database_on_new_upload(self):
       
#         if self.file_controller and self.file_controller.use_database:
#             try:
#                 self.file_controller.clear_database()
#                 print("Database cleared for new import")
#             except Exception as e:
#                 print(f"Error clearing database: {e}")
    
   
   
   
   
   
   
   
from PyQt5.QtWidgets import QMessageBox
# from SRC.ViewLayer.View.main_page_qt5 import MainPageQt5
from SRC.ViewLayer.View.MainPage import MainPageView as MainPageQt5
from SRC.Models.ValidationError import ValidationError
import os
import shutil
from SRC.Controller.FileController import FileController
from pathlib import Path

class LandPageController:
    def __init__(self, view, parent_controller=None):
        self.view = view
        self.file_controller = None
        self.parent_controller = parent_controller  
        
        self.file_uploaded = False
        self.uploaded_path = None
        self.Data = None
        self.view.back_button.clicked.connect(self.go_back_to_start)
        # Connect buttons and signals
        self.view.upload_button.clicked.connect(self.upload_file)
        self.view.send_button.clicked.connect(self.send_action)
        self.view.file_uploaded.connect(self.handle_uploaded_file)

    def handle_uploaded_file(self, path):
        self.clear_database_on_new_upload()
        # Check if the path is valid
        if not path.endswith((".txt", ".xlsx")):
            QMessageBox.critical(self.view, "Invalid file", "Only .txt or .xlsx files are allowed.")
            return

        try:
            save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Data')
            os.makedirs(save_dir, exist_ok=True)

            # Get the file extension
            extension = os.path.splitext(path)[1]
            
            # Create the destination path
            dest_path = os.path.join(save_dir, f"courses{extension}")
            
            # Copy the file to the destination
            shutil.copy(path, dest_path)
            self.uploaded_path = dest_path
            
            last_two_parts = Path(self.uploaded_path).parts[-2:]
            filePath = os.path.join(*last_two_parts)
            unix_style_path = filePath.replace("\\", "/")
            
            # Create the file controller with database enabled
            self.file_controller = FileController(extension, unix_style_path, use_database=True)
            
            # Update the view to show the uploaded file
            self.view.file_label.setText(f"Uploaded: {os.path.basename(path)}")
            
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
        self.clear_database_on_new_upload()
        if not self.file_uploaded:
            QMessageBox.warning(self.view, "Missing File", "Please upload a .txt or .xlsx file before proceeding.")
            return

        if not self.file_controller:
            QMessageBox.critical(self.view, "Error", "File controller not initialized.")
            return

        try:
            # Read courses from file and import to database
            courses, errors = self.file_controller.read_courses_from_file(self.uploaded_path)
            
            last_two_parts = Path(self.uploaded_path).parts[-2:]
            filePath = os.path.join(*last_two_parts)
            unix_style_path = filePath.replace("\\", "/")
            
            if errors:
                error_messages = "\n".join(str(error) for error in errors)
                QMessageBox.warning(self.view, "Invalid Course File", f"The following errors were found:\n\n{error_messages}")
                return

           

            self.view.close()
            self.Data = courses
           
            self.main_page = MainPageQt5(self.Data, self.file_controller, unix_style_path)
            self.main_page.show()
            self.main_page.setWindowTitle("Main Page")
            self.main_page.resize(800, 600)

        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Failed to process file:\n{str(e)}")
    
    def clear_database_on_new_upload(self):
       
        if self.file_controller and self.file_controller.use_database:
            try:
                self.file_controller.clear_database()
                print("Database cleared for new import")
            except Exception as e:
                print(f"Error clearing database: {e}")
    def add_back_button(self):
        """Add a back button to return to start page"""
        from PyQt5.QtWidgets import QPushButton
        back_button = QPushButton("Back to Start")
        back_button.clicked.connect(self.go_back_to_start)
        # Add this button to your view layout
        
    def go_back_to_start(self):
        """Go back to the start page"""
        try:
            if self.parent_controller:
                # If we have a parent controller, use it to show the start page
                self.view.hide()
                self.parent_controller.show_start_page()
            else:
                # Fallback: create new start page
                self.view.close()
                from SRC.ViewLayer.View.StartPage import StartPageView
                from SRC.ViewLayer.Logic.StartPageController import StartPageController
                
                start_view = StartPageView()
                start_controller = StartPageController(start_view)
                start_view.show()
                
        except Exception as e:
            print(f"Error going back to start: {e}")