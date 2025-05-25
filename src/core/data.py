# data.py用于获取数据的模块，我打算把他们分开来写，提高代码的可读性和可维护性。

import akshare as ak
import pandas as pd
# 这是akshare的wiki文档，大家需要前去了解一下其中部分方法的调用：https://akshare.akfamily.xyz/introduction.html
# 这是关于pandas的教程，大家也许需要简单了解一下：https://www.runoob.com/pandas/pandas-tutorial.html

#下面的get_single_stock_history_data是一个简单的使用示例

"""
       qfq前复权：保持当前价格不变，将历史价格进行增减，从而使股价连续。 前复权用来看盘非常方便，能一眼看出股价的历史走势，叠加各种技术指标也比较顺畅，是各种行情软件默认的复权方式。 这种方法虽然很常见，但也有两个缺陷需要注意。

           2.1 为了保证当前价格不变，每次股票除权除息，均需要重新调整历史价格，因此其历史价格是时变的。 这会导致在不同时点看到的历史前复权价可能出现差异。

           2.2 对于有持续分红的公司来说，前复权价可能出现负值。

       hfq后复权：保证历史价格不变，在每次股票权益事件发生后，调整当前的股票价格。 后复权价格和真实股票价格可能差别较大，不适合用来看盘。 其优点在于，可以被看作投资者的长期财富增长曲线，反映投资者的真实收益率情况。
       """


def get_stock_data(symbol):
    try:
        data = ak.stock_zh_a_hist(symbol=symbol, adjust="hfq")[['日期', '开盘', '收盘', '最高', '最低', '成交量']]
        data.columns = ['date', 'open', 'close', 'high', 'low', 'volume'] #我们只要前六个
        data.index = pd.to_datetime(data['date'])

        numeric_columns = ['open', 'close', 'high', 'low', 'volume']
        for column in numeric_columns:
            data[column] = pd.to_numeric(data[column], errors='coerce')

        data[numeric_columns] = data[numeric_columns].ffill().bfill()

        return data

    except Exception as e:
        print(f"数据获取失败: {str(e)}")
        return pd.DataFrame()

#这个方法需要加一个sh或者sz来代表股票上市区域
def get_single_stock_ticks_data(market,stock_code,time):
    try:

        data = ak.stock_intraday_sina(symbol=market + stock_code,date=time)
        data.set_index('ticktime', inplace=True)
        data.index = pd.to_datetime(data.index)
        return data

    except Exception as e:
        print(f"数据获取错误: {e}")
        return None
