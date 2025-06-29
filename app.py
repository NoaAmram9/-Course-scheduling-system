

# import sys
# from PyQt5.QtWidgets import QApplication
# from SRC.ViewLayer.View.StartPage import StartPageView
# from SRC.ViewLayer.Logic.StartPageController import StartPageController

# def main():
#     """Main function to start the application"""
#     app = QApplication(sys.argv)
    
#     # Create the start page view
#     view = StartPageView()
    
#     # Create the controller and pass the view
#     logic = StartPageController(view)
    
#     # IMPORTANT: Keep references to prevent garbage collection
#     app.view = view
#     app.logic = logic
    
#     # Show the start page
#     view.show()
    
#     # Start the application event loop
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from SRC.ViewLayer.View.Login import LoginView
from SRC.ViewLayer.Logic.Login import LoginController
from SRC.ViewLayer.View.Register import RegisterView
from SRC.ViewLayer.Logic.Register import RegisterController


class ModernUI:
    """Main UI Manager for the application"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')  # Modern style
        self.current_view = None
        self.current_controller = None
        
        # Load global styles
        self.load_global_styles()
        
    def load_global_styles(self):
        """Load global application styles"""
        global_style = """
        QApplication {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
        }
        
        * {
            outline: none;
        }
        
        /* Scrollbar Styles */
        QScrollBar:vertical {
            background: #2b2b2b;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background: #555;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #666;
        }
        """
        self.app.setStyleSheet(global_style)
    
    def show_login(self):
        """Show login screen"""
        if self.current_view:
            self.current_view.close()
            
        view = LoginView()
        controller = LoginController(view, self)
        
        # Keep references
        self.current_view = view
        self.current_controller = controller
        
        view.show()
    
    def show_register(self):
        """Show register screen"""
        if self.current_view:
            self.current_view.close()
            
        view = RegisterView()
        controller = RegisterController(view, self)
        
        # Keep references
        self.current_view = view
        self.current_controller = controller
        
        view.show()
    
    def show_start_page(self, user_data=None):
        """Show start page after successful login"""
        if self.current_view:
            self.current_view.close()
            
        # Import here to avoid circular imports
        from SRC.ViewLayer.View.StartPage import StartPageView
        from SRC.ViewLayer.Logic.StartPageController import StartPageController
        
        # Create the start page view
        view = StartPageView()
        
        # Create the controller and pass the view
        logic = StartPageController(view)
        
        # IMPORTANT: Keep references to prevent garbage collection
        self.current_view = view
        self.current_controller = logic
        
        # Show the start page
        view.show()
    
    def run(self):
        """Start the application"""
        # Show login screen by default
        self.show_login()
        
        # Start the application event loop
        return self.app.exec_()


def main():
    ui_manager = ModernUI()
    sys.exit(ui_manager.run())


if __name__ == "__main__":
    main()