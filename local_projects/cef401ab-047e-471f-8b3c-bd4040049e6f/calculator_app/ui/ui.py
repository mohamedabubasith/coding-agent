import tkinter as tk

class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.calculator = Calculator()
        
        # Entry widgets
        self.entry1 = tk.Entry(root, width=15)
        self.entry1.grid(row=0, column=0, padx=10, pady=10)
        
        self.entry2 = tk.Entry(root, width=15)
        self.entry2.grid(row=0, column=1, padx=10, pady=10)
        
        # Button widgets
        self.add_button = tk.Button(root, text="Add", command=self.add_values)
        self.add_button.grid(row=1, column=0, padx=10, pady=10)
        
        self.subtract_button = tk.Button(root, text="Subtract", command=self.subtract_values)
        self.subtract_button.grid(row=1, column=1, padx=10, pady=10)
        
        # Result label
        self.result_label = tk.Label(root, text="Result: ", font=("Arial", 14))
        self.result_label.grid(row=2, column=0, columnspan=2, pady=10)
    
    def add_values(self):
        try:
            num1 = float(self.entry1.get())
            num2 = float(self.entry2.get())
            result = self.calculator.add(num1, num2)
            self.result_label.config(text=f"Result: {result}")
        except ValueError:
            self.result_label.config(text="Result: Invalid input")
    
    def subtract_values(self):
        try:
            num1 = float(self.entry1.get())
            num2 = float(self.entry2.get())
            result = self.calculator.subtract(num1, num2)
            self.result_label.config(text=f"Result: {result}")
        except ValueError:
            self.result_label.config(text="Result: Invalid input")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()