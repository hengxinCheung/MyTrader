from enum import Enum, auto


class EnvironmentType(Enum):
    REAL = auto
    BACKTEST = auto


class Environment(object):
    def __init__(self, type: EnvironmentType):
        """"""
        self.type = type  # 环境类型
        self.orders = []  # 委托列表
        self.trades = []  # 交易列表
        self.positions = []  # 持仓列表
        self.ticks = []  # tick数据列表
        self.bars = []  # bar数据列表

        self.model_type = "bar"  # 运行模型类型：收盘价(bar)、实时价(tick)

        self.contract = ""  # 允许交易的合约号，目前不支持多合约
        self.available_fund = 0  # 可用资金
        self.default_open_hands = 1  # 默认开仓手数
        self.commission = 0  # 手续费
        self.commission_type = "per"  # 手续费类型：绝对值(abs)或百分比(per)
        self.deposit = 0  # 保证金比例

    def on_tick(self, tick):
        pass

    def on_bar(self, bar):
        pass

    def get_data(self):
        if self.model_type == "bar":
            return self.bars
        elif self.model_type == "tick":
            return self.ticks


class RealEnvironment(Environment):
    def __init__(self):
        super(RealEnvironment, self).__init__(EnvironmentType.REAL)
        self.load_history = False  # 是否加载历史数据，如订单、交易、持仓等
        self.retry_count = 20  # 下单重试次数

        # 如果要加载历史信息，将会从数据库中读取
        if self.load_history:
            self.load_orders()
            self.load_trades()
            self.load_positions()

    def load_orders(self):
        """从数据库读取历史委托信息"""
        pass

    def load_trades(self):
        """从数据库读取历史交易信息"""
        pass

    def load_positions(self):
        """从数据库读取历史持仓信息"""
        pass


class BacktestEnvironment(Environment):
    def __init__(self):
        super(BacktestEnvironment, self).__init__(EnvironmentType.BACKTEST)
