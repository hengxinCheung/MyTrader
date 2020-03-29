from .engine import EventEngine
from .object import Event, EventType

"""定义的事件类型"""
E_TIMER = EventType("eTimer")  # 定时器事件，默认每秒产生一次
E_LOG = EventType(name="eLog", priority=10)  # 日志事件
