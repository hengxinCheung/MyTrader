"""All built-in functions must contain the argument 'env' (mytrader.mylang.env.Environment),
which must be at the first position and is automatically injected by the compiler.
So the user does not need to input the argument. And you can get any data you need from the 'env'.
Here are some special rule for coding builtin function:
- first argument must be 'env'
- arguments of this type '*args, **kwargs' can not be used
- arguments can not have default value"""
from mytrader.mylang.env import EnvironmentType, Environment


def INFO(env: Environment, condition, msg):
    if condition:
        print(msg)


def LOG(env: Environment, msg):
    print(msg)


def CLOSE(env: Environment):
    if env.type == EnvironmentType.BACKTEST:
        # 这里不能直接返回pd的一列，应该创建一个TimeSeries对象以返回
        return env.running_bars["close"]


def OPEN(env: Environment):
    if env.type == EnvironmentType.BACKTEST:
        return env.running_bars["open"]


def HIGH(env: Environment):
    if env.type == EnvironmentType.BACKTEST:
        return env.running_bars["high"]


def LOW(env: Environment):
    if env.type == EnvironmentType.BACKTEST:
        return env.running_bars["low"]


def VOLUME(env: Environment):
    if env.type == EnvironmentType.BACKTEST:
        return env.running_bars["volume"]


__all__ = (
    "INFO",
    "LOG",
    "CLOSE",
    "OPEN",
    "HIGH",
    "LOW",
    "VOLUME",
)
