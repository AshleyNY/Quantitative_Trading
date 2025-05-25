# src/backtest.py

from datetime import datetime
import backtrader as bt
from src.core.data import get_stock_data
from src.core.strategy import MyStrategy
from src.core.utils import get_date_input

def run_backtest(stock_code, use_take_profit, take_profit, take_profit_size,
                 use_stop_loss, stop_loss, stop_loss_size,
                 use_sma_crossover, maperiod, start_cash, start_date=None, end_date=None):
    while True:
        stock_df = get_stock_data(stock_code)
        if not stock_df.empty:
            break
        print("未找到对应股票数据，请检查代码格式（A股6位数字代码）")
        return None, None

    # 如果没有输入起始时间和结束时间，使用数据的最早和最晚日期
    if not start_date:
        start_date = datetime.combine(stock_df.index.min().date(), datetime.min.time())
    if not end_date:
        end_date = datetime.combine(stock_df.index.max().date(), datetime.min.time())

    # 修正开始日期
    data_start = stock_df.index.min().date()
    data_end = stock_df.index.max().date()
    if start_date.date() < data_start:
        print(f"警告：开始日期早于数据最早日期 ({data_start})，已自动修正")
        start_date = datetime.combine(data_start, datetime.min.time())
    elif start_date.date() > data_end:
        print(f"警告：开始日期晚于数据最新日期 ({data_end})，已自动修正")
        start_date = datetime.combine(data_end, datetime.min.time())

    # 修正结束日期
    if end_date.date() > data_end:
        print(f"警告：结束日期晚于数据最新日期 ({data_end})，已自动修正")
        end_date = datetime.combine(data_end, datetime.min.time())
    elif end_date.date() < data_start:
        print(f"警告：结束日期早于数据最早日期 ({data_start})，已自动修正")
        end_date = datetime.combine(data_start, datetime.min.time())

    # 检查日期顺序
    if start_date > end_date:
        print(f"错误：开始日期 {start_date.date()} 晚于结束日期 {end_date.date()}，已自动交换")
        start_date, end_date = end_date, start_date

    # 初始化回测引擎
    cerebro = bt.Cerebro()
    data = bt.feeds.PandasData(dataname=stock_df, fromdate=start_date, todate=end_date)
    cerebro.adddata(data)

    cerebro.addstrategy(
        MyStrategy,
        start_date=start_date,
        end_date=end_date,
        maperiod=maperiod,
        stop_loss=stop_loss,
        take_profit=take_profit,
        use_take_profit=use_take_profit,
        use_stop_loss=use_stop_loss,
        use_sma_crossover=use_sma_crossover,
        take_profit_size=take_profit_size,
        stop_loss_size=stop_loss_size,
        sma_buy_size=take_profit_size,  # 这里假设均线买入笔数和止盈交易笔数相同
        sma_sell_size=stop_loss_size    # 这里假设均线卖出笔数和止损交易笔数相同
    )

    cerebro.broker.setcash(start_cash)
    cerebro.broker.setcommission(commission=0.002)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade')

    # 运行回测
    results = cerebro.run()
    strat = results[0]

    # 分析结果
    drawdown_analysis = strat.analyzers.drawdown.get_analysis() if hasattr(strat.analyzers, 'drawdown') else {}
    drawdown_value = drawdown_analysis.get('max', {}).get('drawdown', 0.0) if isinstance(drawdown_analysis,
                                                                                         dict) else 0.0
    port_value = cerebro.broker.getvalue()
    pnl = port_value - start_cash

    trade_count = 0
    if hasattr(strat.analyzers, 'trade'):
        trade_analysis = strat.analyzers.trade.get_analysis()
        try:
            trade_count = trade_analysis['total']['closed']
        except KeyError:
            trade_count = 0

    # 生成报告
    report = f"\n{'=' * 30} 回测报告 {'=' * 30}\n"
    report += f"股票代码: {stock_code}\n"
    report += f"回测时间: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}\n"
    report += f"初始资金: {start_cash:,.2f} 元\n"
    report += f"总资金: {port_value:,.2f} 元\n"
    report += f"净收益: {pnl:,.2f} 元\n"
    report += f"收益率: {pnl / start_cash * 100:.2f}%\n"
    report += f"止盈功能: {'开启' if use_take_profit else '关闭'}\n"
    report += f"止盈比例: {take_profit * 100:.2f}% | 止盈交易笔数: {take_profit_size} 股" if use_take_profit else "止盈功能已关闭\n"
    report += f"止损功能: {'开启' if use_stop_loss else '关闭'}\n"
    report += f"止损比例: {stop_loss * 100:.2f}% | 止损交易笔数: {stop_loss_size} 股" if use_stop_loss else "止损功能已关闭\n"
    report += f"均线交易: {'开启' if use_sma_crossover else '关闭'}\n"
    report += f"均线周期: {maperiod} 日 | 均线买入笔数: {take_profit_size} 股 | 均线卖出笔数: {stop_loss_size} 股" if use_sma_crossover else "均线功能已关闭\n"
    report += f"最大回撤: {float(drawdown_value):.2f}%" if drawdown_value and float(drawdown_value) > 0 else "最大回撤: N/A (未触发持仓变动)\n"
    report += f"交易次数: {trade_count} 次\n"
    report += '=' * 70

    return report, cerebro