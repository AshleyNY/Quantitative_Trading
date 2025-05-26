import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from src.core.backtest import run_ticks_backtest
from src.core.utils import update_date_range

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

class TicksPage:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.init_ticks_page()

    def init_ticks_page(self):

        title_label = ttk.Label(self.frame, text="分时交易策略回测", font=("SimHei", 16, "bold"))
        title_label.pack(pady=20)


        self.create_ticks_form(self.frame)
        self.create_result_frame(self.frame)


    """注意一下，row是列项排版，column是行项排版,具体可以参考知乎上的tk教程！！
         声明一下规范！！：同志们写控件“widgets”，一定要注释这个控件名字，然后
         注意留白分区，不然难看的一批
     """

    def create_ticks_form(self, parent):

        # 创建分时交易策略的表单控件
        form_frame = ttk.LabelFrame(parent, text="策略参数设置")
        form_frame.pack(fill=tk.X, padx=20, pady=10)

        # 股票代码
        ttk.Label(form_frame, text="股票代码:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ticks_stock_code = ttk.Entry(form_frame, width=15)
        self.ticks_stock_code.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.ticks_stock_code.insert(0, "0")
        self.ticks_stock_code.bind("<KeyRelease>", self.update_date_range)

        """每一个控件的横竖间隔都是2个单位，row和column"""

        # 日期
        ttk.Label(form_frame, text="日期:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.ticks_date = ttk.Entry(form_frame, width=12)
        self.ticks_date.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        self.ticks_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        #这个是价格均线周期
        ttk.Label(form_frame, text="价格均线周期:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.ticks_price_period = ttk.Entry(form_frame, width=12)
        self.ticks_price_period.grid(row=0, column=5, sticky=tk.W, padx=5, pady=5)
        self.ticks_price_period.insert(0, "10")

        # 止盈止损设置
        ttk.Label(form_frame, text="止盈比例:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.ticks_take_profit = ttk.Entry(form_frame, width=5)
        self.ticks_take_profit.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.ticks_take_profit.insert(0, "1.20")

        ttk.Label(form_frame, text="止损比例:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.ticks_stop_loss = ttk.Entry(form_frame, width=5)
        self.ticks_stop_loss.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        self.ticks_stop_loss.insert(0, "0.90")

        #这个是数量均线周期
        ttk.Label(form_frame, text="交易量均线周期:").grid(row=1, column=4, sticky=tk.W, padx=5, pady=5)
        self.ticks_volume_period = ttk.Entry(form_frame, width=12)
        self.ticks_volume_period.grid(row=1, column=5, sticky=tk.W, padx=5, pady=5)
        self.ticks_volume_period.insert(0, "10")


        # 复选框 - 策略开关
        self.ticks_use_tp_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, text="启用止盈", variable=self.ticks_use_tp_var).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        self.ticks_use_sl_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, text="启用止损", variable=self.ticks_use_sl_var).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # 初始资金
        ttk.Label(form_frame, text="初始资金:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.ticks_start_cash = ttk.Entry(form_frame, width=15)
        self.ticks_start_cash.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        self.ticks_start_cash.insert(0, "100000000")

        # 交易笔数
        ttk.Label(form_frame, text="交易笔数:").grid(row=3, column=2, sticky=tk.W, padx=5, pady=5)
        self.ticks_trade_size = ttk.Entry(form_frame, width=10)
        self.ticks_trade_size.grid(row=3, column=3, sticky=tk.W, padx=5, pady=5)
        self.ticks_trade_size.insert(0, "1000")

        # 运行回测按钮
        run_button = ttk.Button(form_frame, text="运行分时回测", command=self.run_ticks_backtest)
        run_button.grid(row=3, column=5, sticky=tk.E, padx=5, pady=5)

        self.date_range_label = ttk.Label(form_frame, text="数据时间范围：未获取")
        self.date_range_label.grid(row=4, column=0, columnspan=2, pady=5)

    def update_date_range(self, event=None):
        stock_code = self.ticks_stock_code.get()
        update_date_range(stock_code, self.date_range_label)

    def create_result_frame(self, parent):
        # 创建回测结果显示区域
        result_frame = ttk.LabelFrame(parent, text="回测结果")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 创建文本结果区域
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, height=10)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)

    def run_ticks_backtest(self):
        # 获取表单数据
        stock_code = self.ticks_stock_code.get()
        date_str = self.ticks_date.get()
        profit_rate = float(self.ticks_take_profit.get())
        loss_rate = float(self.ticks_stop_loss.get())
        stop_by_profit = self.ticks_use_tp_var.get()
        stop_by_loss = self.ticks_use_sl_var.get()
        start_cash = float(self.ticks_start_cash.get())
        trade_size = int(self.ticks_trade_size.get())
        price_period = int(self.ticks_price_period.get())
        volume_period = int(self.ticks_volume_period.get())

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("日期格式错误", "请使用YYYY-MM-DD格式输入日期")
            return


        self.result_text.delete(1.0, tk.END)

        try:
            report, back_test_ticks_engine = run_ticks_backtest(
                stock_code=stock_code,
                date=date,
                price_period=price_period,
                volume_period=volume_period,
                start_cash=start_cash,
                profit_rate=profit_rate,
                profit_size=trade_size,
                stop_by_profit=stop_by_profit,
                loss_rate=loss_rate,
                loss_size=trade_size,
                stop_by_loss=stop_by_loss,
                buy_size=trade_size,
                sell_size=trade_size
            )

            if report and back_test_ticks_engine:
                self.result_text.insert(tk.END, report)
                strategy_instance = back_test_ticks_engine.runstrats[0][0]
                back_test_ticks_engine.plot(
                    style='candlestick',
                    iplot= False,
                    barup='red',
                    bardown='green',
                    title=f'{stock_code} 回测结果\n{date.strftime("%Y-%m-%d")}',
                    grid=True,
                    figsize=(14, 7),
                )
                messagebox.showinfo("回测完成", "回测已成功完成，请查看输出结果。")

            else:
                self.result_text.insert(tk.END, "回测失败，请检查参数")

        except Exception as e:
            self.result_text.insert(tk.END, f"回测过程中发生错误: {str(e)}")