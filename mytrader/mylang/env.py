from enum import Enum, auto


class EnvironmentType(Enum):
    REAL = auto
    BACKTEST = auto


class Environment(object):
    def __init__(self, type: EnvironmentType, orders, trades):
        """
        :param type
        """
        self.type = type
        self.orders = orders
        self.trades = trades


class RealEnvironment(Environment):
    def __init__(self):
        super(RealEnvironment, self).__init__(EnvironmentType.REAL)


class BacktestEnvironment(Environment):
    def __init__(self,
                 bars,  # K线数据
                 securities,  # 合约列表
                 available_money=100000,  # 可用资金数
                 default_open_hands=1,  # 默认开仓数
                 commission=0,  # 手续费
                 deposit=0,  # 保证金比例
                 ):
        super(BacktestEnvironment, self).__init__(EnvironmentType.BACKTEST, [], [])

        self.bars = bars
        self.running_bars = None
        self.securities = securities
        self.available_money = available_money
        self.default_open_hands = default_open_hands
        self.commission = commission
        self.deposit = deposit
