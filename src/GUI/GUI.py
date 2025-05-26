import tkinter as tk
import tkinter.ttk as ttk

from src.GUI.daily_page import DailyPage
from src.GUI.ticks_page import TicksPage


class StockBacktestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("股票量化交易回测系统")
        self.root.geometry("1000x700")

        #选项卡
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 日K
        self.daily_page = DailyPage(self.notebook)
        self.notebook.add(self.daily_page.frame, text="日交易策略")

        # 分时
        self.ticks_page = TicksPage(self.notebook)
        self.notebook.add(self.ticks_page.frame, text="分时交易策略")







"""

import tkinter as tk
from tkinter import messagebox
from src.core.backtest import run_daily_backtest
from src.core.data import get_single_stock_history_data
from src.core.utils import validate_stock_code
import tkinter.ttk as ttk
from datetime import datetime


class StockBacktestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("股票回测系统")

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))


        self.create_input_widgets()


        self.start_button = ttk.Button(self.main_frame, text="开始回测", command=self.start_backtest)
        self.start_button.grid(row=15, column=0, columnspan=2, pady=10)


        self.result_text = tk.Text(self.main_frame, height=20, width=80)
        self.result_text.grid(row=16, column=0, columnspan=2, pady=10)

    def create_input_widgets(self):

        ttk.Label(self.main_frame, text="请输入股票代码（A股6位数字代码）：").grid(row=0, column=0, sticky=tk.W)
        self.stock_code_entry = ttk.Entry(self.main_frame)
        self.stock_code_entry.grid(row=0, column=1, pady=5)
        self.stock_code_entry.bind("<KeyRelease>", self.update_date_range)

        ttk.Label(self.main_frame, text="是否开启止盈功能（y/n）：").grid(row=1, column=0, sticky=tk.W)
        self.use_take_profit_var = tk.BooleanVar()
        self.use_take_profit_checkbox = ttk.Checkbutton(self.main_frame, variable=self.use_take_profit_var)
        self.use_take_profit_checkbox.grid(row=1, column=1, pady=5)


        ttk.Label(self.main_frame, text="止盈比例（例如1.1表示10%止盈）：").grid(row=2, column=0, sticky=tk.W)
        self.take_profit_entry = ttk.Entry(self.main_frame)
        self.take_profit_entry.insert(0, '1.1')
        self.take_profit_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.main_frame, text="止盈交易笔数（股数）：").grid(row=3, column=0, sticky=tk.W)
        self.take_profit_size_entry = ttk.Entry(self.main_frame)
        self.take_profit_size_entry.insert(0, '1000')
        self.take_profit_size_entry.grid(row=3, column=1, pady=5)


        ttk.Label(self.main_frame, text="是否开启止损功能（y/n）：").grid(row=4, column=0, sticky=tk.W)
        self.use_stop_loss_var = tk.BooleanVar()
        self.use_stop_loss_checkbox = ttk.Checkbutton(self.main_frame, variable=self.use_stop_loss_var)
        self.use_stop_loss_checkbox.grid(row=4, column=1, pady=5)


        ttk.Label(self.main_frame, text="止损比例（例如0.95表示5%止损）：").grid(row=5, column=0, sticky=tk.W)
        self.stop_loss_entry = ttk.Entry(self.main_frame)
        self.stop_loss_entry.insert(0, '0.95')
        self.stop_loss_entry.grid(row=5, column=1, pady=5)

        ttk.Label(self.main_frame, text="止损交易笔数（股数）：").grid(row=6, column=0, sticky=tk.W)
        self.stop_loss_size_entry = ttk.Entry(self.main_frame)
        self.stop_loss_size_entry.insert(0, '1000')
        self.stop_loss_size_entry.grid(row=6, column=1, pady=5)

        ttk.Label(self.main_frame, text="是否开启均线交易功能（y/n）：").grid(row=7, column=0, sticky=tk.W)
        self.use_sma_crossover_var = tk.BooleanVar()
        self.use_sma_crossover_checkbox = ttk.Checkbutton(self.main_frame, variable=self.use_sma_crossover_var)
        self.use_sma_crossover_checkbox.grid(row=7, column=1, pady=5)


        ttk.Label(self.main_frame, text="均线周期（如10表示10日均线，建议5 - 30）：").grid(row=8, column=0, sticky=tk.W)
        self.maperiod_entry = ttk.Entry(self.main_frame)
        self.maperiod_entry.insert(0, '10')
        self.maperiod_entry.grid(row=8, column=1, pady=5)

        ttk.Label(self.main_frame, text="初始资金（例如1000000）：").grid(row=9, column=0, sticky=tk.W)
        self.start_cash_entry = ttk.Entry(self.main_frame)
        self.start_cash_entry.insert(0, '1000000')
        self.start_cash_entry.grid(row=9, column=1, pady=5)


        ttk.Label(self.main_frame, text="起始时间 (YYYY-MM-DD)：").grid(row=10, column=0, sticky=tk.W)
        self.start_date_entry = ttk.Entry(self.main_frame)
        self.start_date_entry.grid(row=10, column=1, pady=5)

        ttk.Label(self.main_frame, text="结束时间 (YYYY-MM-DD)：").grid(row=11, column=0, sticky=tk.W)
        self.end_date_entry = ttk.Entry(self.main_frame)
        self.end_date_entry.grid(row=11, column=1, pady=5)

        self.date_range_label = ttk.Label(self.main_frame, text="数据时间范围：未获取")
        self.date_range_label.grid(row=12, column=0, columnspan=2, pady=5)

    def update_date_range(self, event=None):
        stock_code = self.stock_code_entry.get().strip()
        if validate_stock_code(stock_code):
            stock_df = get_single_stock_history_data(stock_code)
            if not stock_df.empty:
                data_start = stock_df.index.min().date()
                data_end = stock_df.index.max().date()
                self.date_range_label.config(text=f"数据时间范围：{data_start} 至 {data_end}")
            else:
                self.date_range_label.config(text="数据时间范围：未获取")
        else:
            self.date_range_label.config(text="数据时间范围：未获取")

    def start_backtest(self):

        stock_code = self.stock_code_entry.get().strip()
        if not validate_stock_code(stock_code):
            messagebox.showerror("错误", "股票代码格式不正确，请输入6位纯数字代码。")
            return

        use_take_profit = self.use_take_profit_var.get()
        try:
            take_profit = float(self.take_profit_entry.get().strip())
            take_profit_size = int(self.take_profit_size_entry.get().strip())
        except ValueError:
            messagebox.showerror("错误", "止盈比例或交易笔数输入无效，请输入有效的数字。")
            return

        use_stop_loss = self.use_stop_loss_var.get()
        try:
            stop_loss = float(self.stop_loss_entry.get().strip())
            stop_loss_size = int(self.stop_loss_size_entry.get().strip())
        except ValueError:
            messagebox.showerror("错误", "止损比例或交易笔数输入无效，请输入有效的数字。")
            return

        use_sma_crossover = self.use_sma_crossover_var.get()
        try:
            maperiod = int(self.maperiod_entry.get().strip())
            start_cash = float(self.start_cash_entry.get().strip())
        except ValueError:
            messagebox.showerror("错误", "均线周期或初始资金输入无效，请输入有效的数字。")
            return


        if use_sma_crossover and not (5 <= maperiod <= 30):
            messagebox.showerror("错误", "均线周期应在5 - 30之间。")
            return


        if use_take_profit and take_profit <= 1:
            messagebox.showerror("错误", "止盈比例必须大于1。")
            return


        if use_stop_loss and not (0 < stop_loss < 1):
            messagebox.showerror("错误", "止损比例应在0 - 1之间。")
            return


        start_date_str = self.start_date_entry.get().strip()
        end_date_str = self.end_date_entry.get().strip()

        try:
            if start_date_str:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            else:
                start_date = None

            if end_date_str:
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            else:
                end_date = None

        except ValueError:
            messagebox.showerror("错误", "日期格式错误，请输入 YYYY-MM-DD 格式。")
            return

        # 检查日期顺序
        if start_date and end_date and start_date > end_date:
            messagebox.showerror("错误", "开始日期不能晚于结束日期。")
            return


        try:
            report, cerebro = run_daily_backtest(stock_code, use_take_profit, take_profit, take_profit_size,
                                                 use_stop_loss, stop_loss, stop_loss_size,
                                                 use_sma_crossover, maperiod, start_cash, start_date, end_date)
            if report and cerebro:
                # 在文本框中显示回测结果
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, report)
                # 绘制图表
                cerebro.plot(
                    style='candlestick',
                    barup='red',
                    bardown='green',
                    title=f'{stock_code} 回测结果\n{start_date.strftime("%Y-%m-%d")} 至 {end_date.strftime("%Y-%m-%d")}',
                    grid=True,
                    figsize=(14, 7)
                )
                messagebox.showinfo("回测完成", "回测已成功完成，请查看输出结果。")
        except Exception as e:
            messagebox.showerror("错误", f"回测过程中出现错误：{str(e)}")
"""