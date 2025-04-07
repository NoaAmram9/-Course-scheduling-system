import sys
import os
import tkinter as tk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'SRC')))


from SRC.ViewLayer.gui import GUI
from SRC.Controller.Controller import Controller
def main():
    # יצירת אובייקט של ה-Controller
    controller = Controller()

    # יצירת אובייקט GUI ומחובר ל-Controller
    app = GUI(controller)
    
    # הפעלת ה-GUI
    app.run()
    

if __name__ == "__main__":
    main()