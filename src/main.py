import tkinter as tk
from GUI.GUI import StockBacktestGUI
# 这是akshare的wiki文档，大家需要前去了解一下其中部分方法的调用：https://akshare.akfamily.xyz/introduction.html
# 这是关于pandas的教程，大家也许需要简单了解一下：https://www.runoob.com/pandas/pandas-tutorial.html
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = StockBacktestGUI(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("程序被手动终止")