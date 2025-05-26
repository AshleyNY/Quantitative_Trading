from datetime import datetime, timedelta
import backtrader as bt
from src.core.data import get_single_stock_history_data


def update_date_range(stock_code, date_range_label):
    stock_code = stock_code.strip()
    if validate_stock_code(stock_code):
        stock_df = get_single_stock_history_data(stock_code)
        if not stock_df.empty:
            data_start = stock_df.index.min().date()
            data_end = stock_df.index.max().date()
            date_range_label.config(text=f"数据时间范围：{data_start} 至 {data_end}")
        else:
            date_range_label.config(text="数据时间范围：未获取")
    else:
        date_range_label.config(text="数据时间范围：未获取")

def validate_stock_code(code: str) -> bool:
    """验证股票代码格式是否符合A股规则"""
    valid_prefix = ['60', '000', '300', '688', '002']
    if not code.isdigit():
        print("错误：股票代码必须为纯数字")
        return False
    if len(code) != 6:
        print("错误：股票代码必须为6位数字")
        return False
    if not any(code.startswith(prefix) for prefix in valid_prefix):
        print("警告：非主流市场代码（沪市60/688，深市000/002/300）")
    return True


def get_date_input(prompt: str, default_date: datetime = None) -> datetime:
    """安全获取日期输入"""
    while True:
        date_str = input(prompt).strip()
        if not date_str and default_date:
            return default_date
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            return parsed_date
        except ValueError:
            print("日期格式错误，请输入 YYYY-MM-DD 格式")


"""愚蠢的方法，把分钟转换为日期，用于回测，因为backtrader的时间单位最小只支持到day，只能把分钟转化为一个虚拟的日期来用了"""
def min2date(start_time,end_time):
    #传入的类型应当是2025-05-26 09:30:00 和 2025-05-26 15:00:00

    #计算一波有end_time到start_time之间多少秒
    minutes = end_time - start_time

    days = int(minutes.total_seconds()/60)

    virtual_start_time = datetime(1970,1,1)
    virtual_end_time = virtual_start_time + timedelta(days=days)

    return virtual_start_time,virtual_end_time

def data_min2date_rename(df):
    #传入的类型应当是一个dataframe，里面的index是datetime类型
    minutes = df.index().max() - df.index().min()
    days = int(minutes.total_seconds()/60)

    for dt in df['date']:
        df