import tkinter as tk
from GUI.GUI import StockBacktestGUI

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = StockBacktestGUI(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("程序已被手动终止。")