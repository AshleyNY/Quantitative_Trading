# data.py用于获取数据的模块，我打算把他们分开来写，提高代码的可读性和可维护性。
from datetime import datetime, timedelta

import akshare as ak
import pandas as pd


def get_single_stock_history_data(symbol):
    try:
        data = ak.stock_zh_a_hist(symbol=symbol, adjust="hfq")[['日期', '开盘', '收盘', '最高', '最低', '成交量']]
        data.columns = ['date', 'open', 'close', 'high', 'low', 'volume']
        data.index = pd.to_datetime(data['date'])
        numeric_columns = ['open', 'close', 'high', 'low', 'volume']
        for column in numeric_columns:
            data[column] = pd.to_numeric(data[column], errors='coerce')
        data[numeric_columns] = data[numeric_columns].ffill().bfill()
        return data

    except Exception as e:
        print(f"数据获取失败: {str(e)}")
        return pd.DataFrame()



def get_single_stock_ticks_data_advanced(stock_code,start,end):
    try:
        data = ak.stock_zh_a_hist_min_em(symbol =stock_code,start_date=start,end_date=end,period="1",adjust="hfq")[['时间','开盘','收盘','最高','最低','成交量']]
        data.columns = ['date', 'open', 'close', 'high', 'low', 'volume']
        data.index = pd.to_datetime(data['date'])
        numeric_columns = ['open', 'close', 'high', 'low', 'volume']
        for column in numeric_columns:
            data[column] = pd.to_numeric(data[column], errors='coerce')
        data[numeric_columns] = data[numeric_columns].ffill().bfill()
        return data

    except Exception as e:
        print(f"数据获取错误: {e}")
        return None

def get_single_stock_ticks_data_transfer(stock_code, start, end):
    try:
        data = ak.stock_zh_a_hist_min_em(symbol=stock_code, start_date=start, end_date=end, period="1", adjust="hfq")[['时间','开盘','收盘','最高','最低','成交量']]
        data.columns = ['date', 'open', 'close', 'high', 'low', 'volume']
        data.index = pd.to_datetime(data['date'])

        """一个非常阴间的算法，因为backtrader不支持分钟级别的回测，那我只能把时间的索引映射成从1970年开启的时间了。。。"""
        base_date = datetime(1970, 1, 1)
        new_dates = []
        for dt in data.index:
            minutes_passed = (dt.hour * 60 + dt.minute) - (9 * 60 + 30)  # 计算从9:30开始经过的分钟数
            new_date = base_date + timedelta(days=minutes_passed) #timedelta是一个时间计算函数，其余的都是老师上课教过的
            new_dates.append(new_date)

        data.index = pd.DatetimeIndex(new_dates)
        data['date'] = pd.DatetimeIndex(new_dates)

        numeric_columns = ['open', 'close', 'high', 'low', 'volume']
        for column in numeric_columns:
            data[column] = pd.to_numeric(data[column], errors='coerce')
        data[numeric_columns] = data[numeric_columns].ffill().bfill()
        data['open'] = data.apply(lambda row: row['close'] if row['open'] == 0 else row['open'], axis=1) #这个接口有毛病，返回的open数据全是0，需要改一下

        return data
    except Exception as e:
        print(f"数据获取错误: {e}")
        return None