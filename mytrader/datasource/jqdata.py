import datetime
import functools
from mytrader.datasource.datasource import DataSource
from jqdatasdk import *


NAME = "JqData"


class JQData(DataSource):
    def __init__(self, username: str, password: str):
        super(JQData, self).__init__(name=NAME)
        # 账户信息
        self.username = username
        self.password = password
        # 自动登录
        self.login()

    def login(self):
        """登录远程服务器"""
        auth(self.username, self.password)

    def logout(self):
        """登出远程服务器"""
        if self.is_login:
            logout()

    @property
    def is_login(self):
        """查看登录状态"""
        return is_auth()

    @functools.lru_cache()
    def get_securities(self, types=['futures'], date=None):
        """获取所有标的信息"""
        return get_all_securities(types=types, date=date)

    @functools.lru_cache()
    def get_symbols(self):
        """获取所有的标的的代码列表"""
        securities = self.get_securities()
        return list(securities.index)

    @functools.lru_cache()
    def get_name_by_symbol(self, symbol):
        """获取对应代码的名字"""
        securities = self.get_securities()
        name = securities.loc[symbol]['display_name']
        return name

    @functools.lru_cache()
    def get_trading_dates(self, start, end):
        """获取指定范围内的交易日"""
        start = str(start)
        end = str(end)
        return [date for date in get_trade_days(start_date=start, end_date=end)]

    @functools.lru_cache()
    def normalize(self, symbol):
        symbols = self.get_symbols()
        for s in symbols:
            if s.startswith(symbol):
                return s
        return None

    @functools.lru_cache()
    def get_bars(self, symbol, start, end, freq):
        """按开始日期、结束日期、频率获取给定期货代码的价格信息"""
        symbol = self.normalize(symbol)
        if symbol:
            return get_price(security=symbol, start_date=str(start), end_date=str(end),
                             frequency=freq, skip_paused=True)
        return []


if __name__ == '__main__':
    jq = JQData(username="15626487308", password="487308")
    print(jq.get_securities())
    print(len(jq.get_securities()))
    print(jq.normalize("ZN2011"))
