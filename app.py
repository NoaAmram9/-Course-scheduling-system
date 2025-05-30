import sys
from PyQt5.QtWidgets import QApplication
from SRC.ViewLayer.View.LandPageView import LandPageView
from SRC.Controller.Controller import Controller
from SRC.ViewLayer.Logic.LandPageController import LandPageController

def main():
    app = QApplication(sys.argv)
    controller = Controller()
    view = LandPageView()
    logic = LandPageController(view, controller)
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
