import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'SRC')))

import tkinter as tk
from SRC.ViewLayer.gui import CourseSchedulerGUI


def main():
    root = tk.Tk()
    app = CourseSchedulerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
