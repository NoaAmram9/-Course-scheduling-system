
import sys
import os
from tkinterdnd2 import TkinterDnD
from SRC.ViewLayer.LandPage import LandPage
from SRC.Controller.Controller import Controller

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'SRC')))



def main():
    controller = Controller()
    root = TkinterDnD.Tk()
    app = LandPage(root, controller)
    app.run()

if __name__ == "__main__":
    main()
