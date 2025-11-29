import tkinter as tk
from logic import Calculator
from ui import UI

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator()
    app = UI(root, calculator)
    root.mainloop()