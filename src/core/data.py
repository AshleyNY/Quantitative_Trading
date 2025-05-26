# data.py用于获取数据的模块，我打算把他们分开来写，提高代码的可读性和可维护性。
from datetime import datetime, timedelta

import akshare as ak
import pandas as pd
# 这是akshare的wiki文档，大家需要前去了解一下其中部分方法的调用：https://akshare.akfamily.xyz/introduction.html
# 这是关于pandas的教程，大家也许需要简单了解一下：https://www.runoob.com/pandas/pandas-tutorial.html

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

        # 转换日期
        base_date = datetime(1970, 1, 1)
        new_dates = []
        for dt in data.index:
            minutes_passed = (dt.hour * 60 + dt.minute) - (9 * 60 + 30)  # 计算从9:30开始经过的分钟数
            new_date = base_date + timedelta(days=minutes_passed)
            new_dates.append(new_date)

        data.index = pd.DatetimeIndex(new_dates)
        data['date'] = pd.DatetimeIndex(new_dates)

        numeric_columns = ['open', 'close', 'high', 'low', 'volume']
        for column in numeric_columns:
            data[column] = pd.to_numeric(data[column], errors='coerce')
        data[numeric_columns] = data[numeric_columns].ffill().bfill()
        data['open'] = data.apply(lambda row: row['close'] if row['open'] == 0 else row['open'], axis=1)

        if data.isnull().any().any():
            print("数据中存在缺失值，请检查！")
        return data
    except Exception as e:
        print(f"数据获取错误: {e}")
        return None