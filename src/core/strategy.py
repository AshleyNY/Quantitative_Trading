import backtrader as bt


class MyStrategy(bt.Strategy):
    params = (
        ("maperiod", 10),
        ("start_date", None),
        ("end_date", None),
        ("stop_loss", 0.95),
        ("take_profit", 1.1),
        ("use_take_profit", False),
        ("use_stop_loss", False),
        ("use_sma_crossover", False),
        ("take_profit_size", 1000),
        ("stop_loss_size", 1000),
        ("sma_buy_size", 1000),
        ("sma_sell_size", 1000)
    )

    def __init__(self):
        self.data_close = self.datas[0].close
        self.order = None
        self.buy_price = None
        self.sma = None #这里指的是平均移动线，是一种用于分析股票价格趋势的技术指标。它通过计算一定时间窗口内的价格平均值，来平滑价格数据，从而帮助我们识别趋势方向和价格变化。
        self.crossover = None

        if self.p.use_sma_crossover:
            self.sma = bt.indicators.SimpleMovingAverage(
                self.datas[0].close, period=self.p.maperiod
            )
            self.crossover = bt.indicators.CrossOver(self.datas[0].close, self.sma)

    def log(self, txt):
        dt = self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()} - {txt}")


    def next(self):
        if self.order:
            return

        current_date = self.datas[0].datetime.date(0)
        if (self.p.start_date and current_date < self.p.start_date.date()) or \
                (self.p.end_date and current_date > self.p.end_date.date()):
            return

        if not self.position:
            if self.p.use_sma_crossover and self.crossover > 0:
                self.order = self.buy(size=self.p.sma_buy_size)
        else:
            if self.p.use_take_profit and self.buy_price and self.data_close[0] >= self.buy_price * self.p.take_profit:
                self.order = self.sell(size=self.p.take_profit_size)
            elif self.p.use_stop_loss and self.buy_price and self.data_close[0] < self.buy_price * self.p.stop_loss:
                self.order = self.sell(size=self.p.stop_loss_size)
            elif self.p.use_sma_crossover and self.crossover < 0:
                self.order = self.sell(size=self.p.sma_sell_size)