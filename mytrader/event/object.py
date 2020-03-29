from typing import Any


class EventType(object):
    """
    事件类型
    由事件名称和事件优先级组成
    """
    def __init__(self, name: str, priority: int = 5):
        # 事件名称
        self.name = name
        # 事件优先级，数字越小优先级越高，建议取值范围为(1~10)
        self.priority = priority


class Event(object):
    """
    事件
    由事件类型和事件数据组成
    注意：因为设计了
    """
    def __init__(self, event_type: EventType, data: Any = None):
        self.event_type = event_type
        self.data = data

    def __lt__(self, other):
        return self.event_type.priority < other.event_type.priority

    def __gt__(self, other):
        return self.event_type.priority < other.event_type.priority

    def __eq__(self, other):
        return self.event_type.priority == other.event_type.priority

    def __ne__(self, other):
        return self.event_type.priority != other.event_type.priority

    def __le__(self, other):
        return self.event_type.priority <= other.event_type.priority

    def __ge__(self, other):
        return self.event_type.priority >= other.event_type.priority
