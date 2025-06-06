import backtrader as bt

"""这是一个策略类，用于存储策略，目前有两个，分别对应日K和分时交易"""


class DailyMA(bt.Strategy):  # 日均线大法，建议后期改为5日均线横穿30日均线
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
        self.sma = None  # 这里指的是平均移动线，是一种用于分析股票价格趋势的技术指标。但是不是特别好用，暂时用着
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
        """下面是一个简单策略，价格上穿均线买入，下穿均线卖出，测试一下后发现比较容易翻车"""
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


class SuperShortLineTrade(bt.Strategy):  # 超级短线交易
    params = (
        ("start_date", None),
        ("end_date", None),
        ('price_period', 5),  # 5分钟价格均线
        ('volume_period', 5),  # 5分钟成交量均线
        ("buy_size", 1000),
        ("sell_size", 1000),
        ("stop_by_profit", False),
        ("profit_size", 1000),
        ("profit_rate", 1.1),
        ("stop_by_loss", False),
        ("loss_size", 1000),
        ("loss_rate", 0.9),)

    def __init__(self):
        self.data_price = self.datas[0].close  # 把数据里的收盘价拿出来，暂时储存一下，分别复用和比较
        self.data_volume = self.datas[0].volume  # 量
        self.order = None
        self.buy_price = None
        self.volume_sma = None
        self.price_sma = None
        self.volume_crossover = None
        self.price_crossover = None

        self.price_sma = bt.indicators.SimpleMovingAverage(self.data_price, period=self.p.price_period, plotname="price_sma")
        self.price_crossover = bt.indicators.CrossOver(self.data_price, self.price_sma)  # 这玩意是交叉指标，但是实际用起来非常stupid

        #显然这是一个表数量的均线
        self.volume_sma = bt.indicators.SimpleMovingAverage(self.data_volume,period=self.p.volume_period,)
        self.volume_crossover = bt.indicators.CrossOver(self.data_volume, self.volume_sma)

    def log(self, txt):
        dt = self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()} - {txt}")

    """分析表(量价分析)
    放量上升：买入
    缩量上升：卖出
    缩量下降：买入
    放量下降：卖出
    无趋势：无操作
    """

    def notify_order(self, order):

        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.buy_price = order.executed.price
                self.log(f"买入: 价格={order.executed.price:.2f},数量={order.executed.size:.2f}")
            else:
                self.log( f"卖出: 价格={order.executed.price:.2f}，数量={order.executed.size:.2f}")
        self.order = None

    def next(self):

        if self.order:
            return

        current_date = self.datas[0].datetime.date(0)
        if (self.p.start_date and current_date < self.p.start_date.date()) or \
                (self.p.end_date and current_date > self.p.end_date.date()):
            return

        current_price = self.data_price[0]
        """我本来用的是量和价分析的 ，但是发现好像感觉更愚蠢了，盈利的概率小的可怜，暂时先用着单价分析得了——2025/5/25"""

        """既然这个策略输的那么惨，那我反过来试试。。。。"""

        if not self.position:
            if self.price_crossover < 0:
                self.order = self.buy(size=self.p.buy_size)
        else:
            if self.price_crossover > 0:
                self.order = self.sell(size=self.p.sell_size)

            if self.p.stop_by_profit and self.buy_price and current_price >= self.buy_price * self.p.profit_rate:
                self.order = self.sell(size=self.p.profit_size)
                self.log("卖出：止盈" + " 卖出股数：" + str(self.p.profit_size) + " 当前价格：" + str(current_price))
            if self.p.stop_by_loss and self.buy_price and current_price <= self.buy_price * self.p.loss_rate:
                self.order = self.sell(size=self.p.loss_size)
                self.log("卖出：止损" + " 卖出股数：" + str(self.p.loss_size) + " 当前价格：" + str(current_price))


"""            if self.volume_crossover > 0 and self.price_crossover > 0:
                self.order = self.buy(size=self.p.buy_size)
                self.log("买入：放量上涨" + " 买入股数：" + str(self.p.buy_size) + " 当前价格：" + str(current_price))
            if self.volume_crossover < 0 and self.price_crossover < 0:
                self.order = self.buy(size=self.p.buy_size)
                self.log("买入：缩量下跌" + " 买入股数：" + str(self.p.buy_size) + " 当前价格：" + str(current_price))

        else:
            if self.volume_crossover < 0 < self.price_crossover:
                self.order = self.sell(size=self.p.sell_size)
                self.log("卖出：放量下跌" + " 卖出股数：" + str(self.p.sell_size) + " 当前价格：" + str(current_price))
            if self.volume_crossover > 0 > self.price_crossover:
                self.order = self.sell(size=self.p.sell_size)
                self.log("卖出：放量下跌" + " 卖出股数：" + str(self.p.sell_size) + " 当前价格：" + str(current_price))
            if self.volume_crossover < 0 and self.price_crossover < 0:
                self.order = self.buy(size=self.p.buy_size)
                self.log("买入：放量上涨" + " 买入股数：" + str(self.p.buy_size) + " 当前价格：" + str(current_price))
            if self.volume_crossover > 0 and self.price_crossover > 0:
                self.order = self.buy(size=self.p.buy_size)
                self.log("买入：缩量下跌" + " 买入股数：" + str(self.p.buy_size) + " 当前价格：" + str(current_price))"""