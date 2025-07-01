import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from SRC.ViewLayer.View.Login import LoginView
from SRC.ViewLayer.Logic.Login import LoginController
from SRC.ViewLayer.View.Register import RegisterView
from SRC.ViewLayer.Logic.Register import RegisterController
from SRC.ViewLayer.View.MainPage import MainPageView as MainPageQt5
from SRC.Controller.FileController import FileController

class MainApplication:
    """Main UI Manager for the application"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        self.current_view = None
        self.current_controller = None

    def show_login(self):
        if self.current_view:
            self.current_view.close()
        view = LoginView()
        controller = LoginController(view, self)
        self.current_view = view
        self.current_controller = controller
        view.show()
    
    def show_register(self):
        if self.current_view:
            self.current_view.close()
        view = RegisterView()
        controller = RegisterController(view, self)
        self.current_view = view
        self.current_controller = controller
        view.show()
    
    def show_start_page(self, user_data=None):
        if self.current_view:
            self.current_view.close()
        
      
        # # Default to Student if no user data provided
        # user_type = 'Student'
        if user_data:
            raw_type = user_data.get('type')
            user_type = str(raw_type).strip().lower().capitalize()
            
 
        # Route based on user type
        if user_type.lower() == 'student':
          
            # Students go to Main Page
            self._show_student_main_page(user_data)
        elif user_type.lower() == 'secretary':
        
            # Secretary goes to Start Page
            self._show_secretary_start_page(user_data)
        else:
            # Default fallback to student view
 
            self._show_student_main_page(user_data)
    
    def _show_secretary_start_page(self, user_data=None):
        """Show the Start Page for Secretary users"""
        try:
            from SRC.ViewLayer.View.StartPage import StartPageView
            from SRC.ViewLayer.Logic.StartPageController import StartPageController
            view = StartPageView()
            controller = StartPageController(view)
            self.current_view = view
            self.current_controller = controller
            view.show()
     
        except ImportError as e:
            
            self._show_student_main_page(user_data)
    
    def _show_student_main_page(self, user_data=None):
        """Show the Main Page for Student users"""
        db_path = "Data/courses.db"
        file_controller = FileController(
            file_type=".xlsx",
            filePath=db_path,
            use_database=True
        )
        
        courses = []
        try:
            courses = file_controller.get_courses_from_database()
        except Exception as e:
            print(f"Failed to load courses: {e}")
        
        def return_to_start():
            if self.current_view:
                self.current_view.close()
            self.show_start_page(user_data)
        
        main_page = MainPageQt5(
            Data=courses,
            controller=file_controller,
            filePath=db_path,
            go_back_callback=return_to_start
        )
        self.current_view = main_page
        self.current_controller = None
        main_page.show()
     
            
    def run(self):
        self.show_login()
        return self.app.exec_()

def main():
    ui_manager = MainApplication()
    sys.exit(ui_manager.run())

if __name__ == "__main__":
    main()