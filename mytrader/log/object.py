from dataclasses import dataclass
import datetime


@dataclass
class LogData(object):
    """日志数据"""
    msg: str  # 日志信息
    level: int = 20  # 日志级别: 默认是INFO
    time: datetime.datetime = datetime.datetime.now()  # 日志时间

    def __post_init__(self):
        self.msg = str(self.msg)
