from datetime import datetime


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

