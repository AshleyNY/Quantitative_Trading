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
        self.sma = None
        self.crossover = None

        if self.p.use_sma_crossover:
            self.sma = bt.indicators.SimpleMovingAverage(
                self.datas[0].close, period=self.p.maperiod
            )
            self.crossover = bt.indicators.CrossOver(self.datas[0].close, self.sma)

    def log(self, txt):
        dt = self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()} - {txt}")

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"已买入，价格: {order.executed.price:.2f}, 数量: {order.executed.size}")
                self.buy_price = order.executed.price
            else:
                self.log(f"已卖出，价格: {order.executed.price:.2f}, 数量: {order.executed.size}")
            self.order = None

    def next(self):
        if self.order:
            return

        current_date = self.datas[0].datetime.date(0)
        if (self.p.start_date and current_date < self.p.start_date.date()) or \
                (self.p.end_date and current_date > self.p.end_date.date()):
            return

        if not self.position:
            if self.p.use_sma_crossover and self.crossover > 0:
                self.log(f"均线买入信号: {self.data_close[0]:.2f}")
                self.order = self.buy(size=self.p.sma_buy_size)
        else:
            if self.p.use_take_profit and self.buy_price and self.data_close[0] >= self.buy_price * self.p.take_profit:
                self.log(f"触发止盈卖出: {self.data_close[0]:.2f}")
                self.order = self.sell(size=self.p.take_profit_size)
            elif self.p.use_stop_loss and self.buy_price and self.data_close[0] < self.buy_price * self.p.stop_loss:
                self.log(f"触发止损卖出: {self.data_close[0]:.2f}")
                self.order = self.sell(size=self.p.stop_loss_size)
            elif self.p.use_sma_crossover and self.crossover < 0:
                self.log(f"均线卖出信号: {self.data_close[0]:.2f}")
                self.order = self.sell(size=self.p.sma_sell_size)