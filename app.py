import sys
from PyQt5.QtWidgets import QApplication
from SRC.ViewLayer.View.LandPageView import LandPageView
from SRC.Controller.Controller import Controller
from SRC.Controller.FileController import FileController
from SRC.ViewLayer.Logic.LandPageController import LandPageController

def main():
    app = QApplication(sys.argv)
    # controller = FileController("excel")  # Initialize the file controller with the desired file type
    view = LandPageView()
    logic = LandPageController(view)
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
