import datetime
from mytrader.engine import BaseEngine
from mytrader.mylang.interpret import Interpreter
from mytrader.mylang.env import BacktestEnvironment
from mytrader.mylang.error import LexError, ParseError
from mytrader.backtest.object import Indicator

from mytrader.datasource.jqdata import JQData
import time


ENGINE_NAME = "BacktestEngine"


class BacktestEngine(BaseEngine):
    def __init__(self):
        super(BacktestEngine, self).__init__(engine_name=ENGINE_NAME)

        self.code = ""
        self.symbol = ""
        self.start_date = None
        self.end_date = None
        self.freq = ""

        self.env = None
        self.interpreter = None

        # 计算指标方法字典, key是指标名, value是一个Callable的方法体，默认只有一个参数就是env
        self.indicator_func = dict()
        # 计算指标的值列表，里面的元素是Indicator对象
        self.indicators = list()

    def backtest(self,
                 code: str,  # 策略代码
                 symbol: str,  # 合约代码
                 start_date: (str, datetime.datetime),  # 开始时间
                 end_date: (str, datetime.datetime),  # 结束时间
                 freq: str,  # K线周期
                 env: BacktestEnvironment  # 运行环境, 数据都存放在这里
                 ):
        """"""
        # 设置属性
        self.code = code
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.freq = freq
        self.env = env

        # 实例化编译器
        self.interpreter = Interpreter(env=self.env)

        # 清空指标
        self.indicators.clear()

        # 编译策略代码，可能会抛出LexerError或者ParseError
        try:
            self.interpreter.compile(code)
        except (LexError, ParseError) as e:
            print(e.error_msg)
            return

        for i in range(1, self.env.bars.shape[0]):
            # 重置当前所在bar
            self.env.running_bars = self.env.bars[:i]
            # 执行策略，可能会抛出EvalError或者其他
            try:
                self.interpreter.execute()
            except Exception as e:
                print(str(e))
                continue
            # 执行指标统计
            for name in self.indicator_func.keys():
                func = self.indicator_func.get(name)
                value = func(self.env)
                time = self.env.running_bars[-1].index
                indicator = Indicator(name=name, value=value, time=time)
                self.indicators.append(indicator)


if __name__ == '__main__':
    # 策略代码
    code = """
    LOG(\"123\");
    LOG(CLOSE());
    LOG(OPEN());
    LOG(LOW());
    LOG(HIGH());
    LOG(VOLUME());
    """
    # 创建回测引擎
    backtest_engine = BacktestEngine()
    # 创建数据源
    jq = JQData(username="15626487308", password="487308")
    # 获取bars数据
    bars = jq.get_bars(symbol="I2005.XDCE", start="2019-12-1 00:00:00", end="2020-01-01 23:59:59", freq="1d")
    securities = jq.get_securities()
    # 创建运行环境
    backtest_env = BacktestEnvironment(bars=bars, securities=securities, available_money=100000, default_open_hands=1,
                                       commission=0, deposit=0)
    # 开始回测
    backtest_engine.backtest(code=code, symbol="I2005", start_date='2019-12-1 00:00:00', end_date='2020-01-01 23:59:59',
                             freq='1d', env=backtest_env)