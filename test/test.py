from datetime import datetime,time

from openpyxl.descriptors import DateTime

import src.core.data as data
from src.core.backtest import run_ticks_backtest, run_daily_backtest
from src.core.data import get_single_stock_ticks_data_advanced, get_single_stock_ticks_data_transfer
from src.core.utils import min2date

if __name__ == "__main__":
    start_time = datetime(2025, 5, 21, 9, 30, 0)
    end_time = datetime(2025, 5, 21, 15, 0, 0)
    result = get_single_stock_ticks_data_transfer(
        stock_code="601069",
        start=start_time,
        end=end_time,
    )
    result.to_csv("test/test.csv")



    """  
         run_ticks_backtest(
        stock_code="601069",
        date=datetime(2025, 5, 21),
        start_cash=100000,
        profit_rate=1.02,
        profit_size=1000,
        stop_by_profit=True,
        loss_rate=0.98,
        loss_size=1000,
        stop_by_loss=True,
        buy_size=1000,  # 这里假设均线买入笔数和止盈交易笔数相同
        sell_size=1000  # 这里假设均线卖出笔数和止损交易笔数相同
    )
    
    start_time = datetime(2025,5,21,9,30,0)
    end_time = datetime(2025,5,21,15,0,0)
    result = get_single_stock_ticks_data_transfer(
        stock_code="601069",
        start=start_time,
        end=end_time,
    )

    print(result['date'])

    a,b = min2date(start_time,end_time)

    print(a,b)
    print(start_time,end_time)

    result.to_csv("test/test.csv")"""






    """    start_time = datetime(2025,5,1,9,30,0)
    end_time = datetime(2025,5,1,15,0,0)
    min2date(start_time, end_time)
    v_start_date, v_end_date = min2date(start_time, end_time)
    print(v_start_date, v_end_date)
    """

    """result = get_single_stock_ticks_data_advanced("601069", "2025-05-21 09:30:00", "2025-05-21 15:00:00")

    maxdate = result.index.max().date()
    time = time(hour=9, minute=30, second=0)
    maxdate = datetime.combine(maxdate, time)

    # 指定输出文件的路径
    result.to_csv("test/test.csv")"""



    """result = run_ticks_backtest(
        stock_code="601069",
        date=datetime(2025, 5, 21),
        start_cash=100000,
        profit_rate=1.02,
        profit_size=1000,
        stop_by_profit=True,
        loss_rate=0.98,
        loss_size=1000,
        stop_by_loss=True,
        buy_size=1000,  # 这里假设均线买入笔数和止盈交易笔数相同
        sell_size=1000  # 这里假设均线卖出笔数和止损交易笔数相同
    )

    print(result)"""
