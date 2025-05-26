from datetime import datetime
from tkinter import ttk, messagebox
import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.core.backtest import run_daily_backtest
from src.core.utils import update_date_range


plt.rcParams['font.family'] = 'SimHei'

plt.rcParams['axes.unicode_minus'] = False


class DailyPage:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.init_daily_page()

    def init_daily_page(self):

        title_label = ttk.Label(self.frame, text="日交易策略回测", font=("SimHei", 16, "bold"))
        title_label.pack(pady=20)

        """人机交互的表单，这样写比较有可读性"""
        self.create_daily_form(self.frame)

        """这个结果显示的图形还没开发完，暂时先显示文字反馈得了"""
        self.create_result_frame(self.frame)


    """注意一下，row是列项排版，column是行项排版,具体可以参考知乎上的tk教程！！
        声明一下规范！！：同志们写控件“widgets”，一定要注释这个控件名字，然后
        注意留白分区，不然难看的一批
    """

    def create_daily_form(self, parent):
        form_frame = ttk.LabelFrame(parent, text="策略参数设置")
        form_frame.pack(fill=tk.X, padx=20, pady=10)

        # 股票代码
        ttk.Label(form_frame, text="股票代码:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.daily_stock_code = ttk.Entry(form_frame, width=15)
        self.daily_stock_code.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.daily_stock_code.insert(0, "0")
        self.daily_stock_code.bind("<KeyRelease>", self.update_date_range)

        # 开始日期
        ttk.Label(form_frame, text="开始日期:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.daily_start_date = ttk.Entry(form_frame, width=12)
        self.daily_start_date.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        self.daily_start_date.insert(0, "2024-01-01")

        # 结束日期
        ttk.Label(form_frame, text="结束日期:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.daily_end_date = ttk.Entry(form_frame, width=12)
        self.daily_end_date.grid(row=0, column=5, sticky=tk.W, padx=5, pady=5)
        self.daily_end_date.insert(0, "2024-12-31")

        # 均线周期
        ttk.Label(form_frame, text="均线周期:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.daily_maperiod = ttk.Entry(form_frame, width=5)
        self.daily_maperiod.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.daily_maperiod.insert(0, "10")

        # 止盈止损设置
        ttk.Label(form_frame, text="止盈比例:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.daily_take_profit = ttk.Entry(form_frame, width=5)
        self.daily_take_profit.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        self.daily_take_profit.insert(0, "1.2")

        ttk.Label(form_frame, text="止损比例:").grid(row=1, column=4, sticky=tk.W, padx=5, pady=5)
        self.daily_stop_loss = ttk.Entry(form_frame, width=5)
        self.daily_stop_loss.grid(row=1, column=5, sticky=tk.W, padx=5, pady=5)
        self.daily_stop_loss.insert(0, "0.8")

        # 复选框 - 策略开关
        self.daily_use_sma_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, text="启用均线策略", variable=self.daily_use_sma_var).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        self.daily_use_tp_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, text="启用止盈", variable=self.daily_use_tp_var).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        self.daily_use_sl_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, text="启用止损", variable=self.daily_use_sl_var).grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)

        # 初始资金
        ttk.Label(form_frame, text="初始资金:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.daily_start_cash = ttk.Entry(form_frame, width=15)
        self.daily_start_cash.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        self.daily_start_cash.insert(0, "100000000")

        # 交易笔数
        ttk.Label(form_frame, text="交易笔数:").grid(row=3, column=2, sticky=tk.W, padx=5, pady=5)
        self.daily_trade_size = ttk.Entry(form_frame, width=10)
        self.daily_trade_size.grid(row=3, column=3, sticky=tk.W, padx=5, pady=5)
        self.daily_trade_size.insert(0, "1000")

        # 运行回测按钮
        run_button = ttk.Button(form_frame, text="运行日交易回测", command=self.run_daily_backtest)
        run_button.grid(row=3, column=5, sticky=tk.E, padx=5, pady=5)

        self.date_range_label = ttk.Label(form_frame, text="数据时间范围：未获取")
        self.date_range_label.grid(row=4, column=0, columnspan=2, pady=5)

    def update_date_range(self, event=None):
        stock_code = self.daily_stock_code.get()
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

    def run_daily_backtest(self):
        # 获取表单数据
        stock_code = self.daily_stock_code.get()
        start_date_str = self.daily_start_date.get()
        end_date_str = self.daily_end_date.get()
        maperiod = int(self.daily_maperiod.get())
        take_profit = float(self.daily_take_profit.get())
        stop_loss = float(self.daily_stop_loss.get())
        use_sma = self.daily_use_sma_var.get()
        use_tp = self.daily_use_tp_var.get()
        use_sl = self.daily_use_sl_var.get()
        start_cash = float(self.daily_start_cash.get())
        trade_size = int(self.daily_trade_size.get())

        # 转换日期格式
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("日期格式错误", "请使用YYYY-MM-DD格式输入日期")
            return

        # 清空结果区域
        self.result_text.delete(1.0, tk.END)

        # 运行日交易回测
        try:
            # 这里调用你的日交易回测函数
            report, back_test_engine = run_daily_backtest(
                stock_code=stock_code,
                maperiod=maperiod,
                stop_loss=stop_loss,
                take_profit=take_profit,
                use_take_profit=use_tp,
                use_stop_loss=use_sl,
                use_sma_crossover=use_sma,
                take_profit_size=trade_size,
                stop_loss_size=trade_size,
                start_cash=start_cash,
                start_date=start_date,
                end_date=end_date
            )

            # 在实际应用中，你需要从回测结果中提取数据并更新UI
            # 这里只是一个示例，你需要根据你的回测函数返回值进行调整
            if report and back_test_engine:
                # 在文本框中显示回测结果
                self.result_text.insert(tk.END, report)
                # 绘制图表
                back_test_engine.plot(
                    style='candlestick',
                    barup='red',
                    bardown='green',
                    title=f'{stock_code} 回测结果\n{start_date.strftime("%Y-%m-%d")} 至 {end_date.strftime("%Y-%m-%d")}',
                    grid=True,
                    figsize=(14, 7)
                )
                messagebox.showinfo("回测完成", "回测已成功完成，请查看输出结果。")
            else:
                self.result_text.insert(tk.END, "回测失败，请检查参数")

        except Exception as e:
            self.result_text.insert(tk.END, f"回测过程中发生错误: {str(e)}")