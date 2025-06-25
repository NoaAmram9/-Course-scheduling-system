# import sys
# from PyQt5.QtWidgets import QApplication
# from SRC.ViewLayer.View.LandPageView import LandPageView
# from SRC.Controller.FileController import FileController
# from SRC.ViewLayer.Logic.LandPageController import LandPageController

# def main():
#     app = QApplication(sys.argv)
#     # controller = FileController("excel")  # Initialize the file controller with the desired file type
#     view = LandPageView()
#     logic = LandPageController(view)
#     view.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()
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
    
#     # Show the start page
#     view.show()
    
#     # Start the application event loop
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()



import sys
from PyQt5.QtWidgets import QApplication
from SRC.ViewLayer.View.StartPage import StartPageView
from SRC.ViewLayer.Logic.StartPageController import StartPageController

def main():
    """Main function to start the application"""
    app = QApplication(sys.argv)
    
    # Create the start page view
    view = StartPageView()
    
    # Create the controller and pass the view
    logic = StartPageController(view)
    
    # IMPORTANT: Keep references to prevent garbage collection
    app.view = view
    app.logic = logic
    
    # Show the start page
    view.show()
    
    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()