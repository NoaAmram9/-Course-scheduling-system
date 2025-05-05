# import sys
# import os
# import tkinter as tk

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'SRC')))

# from SRC.ViewLayer.LandPage import LandPage
# from SRC.Controller.Controller import Controller

# def main():
#     # יצירת אובייקט של ה-Controller
#     controller = Controller()
#     # יצירת אובייקט GUI ומחובר ל-Controller
#     app = LandPage(controller)
#     # הפעלת ה-GUI
#     app.run()
    
# if __name__ == "__main__":
#     main()



import sys
import os
from tkinterdnd2 import TkinterDnD

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'SRC')))

from SRC.ViewLayer.LandPage import LandPage
from SRC.Controller.Controller import Controller

def main():
    controller = Controller()
    root = TkinterDnD.Tk()
    app = LandPage(root, controller)
    app.run()

if __name__ == "__main__":
    main()
