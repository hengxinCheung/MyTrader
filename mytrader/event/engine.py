from queue import PriorityQueue, Empty, Full
from threading import Thread, Timer
from mytrader.event.object import Event, EventType
from typing import Callable


# 定时器事件类型
E_TIMER = EventType("eTimer")


class EventEngine(object):
    """
    事件引擎
    所有的变量都设置为私用，以防不小心修改导致bug

    事件监听函数必须定义为输入参数仅为一个Event对象，即
    def listen_method(event: Event):
        pass
    """
    def __init__(self, timer_interval: int = 1):
        """初始化事件引擎"""
        # 设置定时器时间间隔
        self.__timer_interval = timer_interval
        # 事件队列，采用优先级队列（PriorityQueue）
        self.__event_queue = PriorityQueue()
        # 事件引擎开关
        self.__active = False
        # 事件处理线程
        self.__event_thread = None
        # 计时器，用于产生一个定时事件，默认时间间隔是1秒
        self.__event_timer = None
        # 处理器字典，key是事件名，value是一个列表：保存对该事件监听的回调函数
        self.__handlers = {}
        # 前处理器列表，用来保存通用回调函数（对所有事件均调用）
        self.__pre_handlers = []

    def __run(self):
        """引擎运行"""
        while self.__active:
            try:
                # 取出事件
                event = self.__event_queue.get(timeout=1)
                self.__process_event(event)
            except Empty:
                continue

    def __process_event(self, event: Event):
        """处理事件"""
        # 先通过前处理器列表
        for pre_handler in self.__pre_handlers:
            pre_handler(event)

        # 再调用特定的处理器
        # 得到该事件类型的处理器列表
        if event.event_type.name in self.__handlers.keys():
            # 遍历处理器列表
            for handler in self.__handlers[event.event_type.name]:
                handler(event)  # 调用处理器

    def __on_timer(self):
        """向事件队列中存入计时器事件"""
        # 创建计时器事件
        event = Event(E_TIMER)
        # 向队列存入事件
        self.put(event)
        # 重新设定一个定时器，这样才可以一直产生定时事件
        self.__event_timer = Timer(self.__timer_interval, self.__on_timer)
        # 开启定时器
        self.__event_timer.start()

    def start(self):
        """引擎启动方法"""
        # 将引擎开关设为启动
        self.__active = True
        # 事件处理线程
        self.__event_thread = Thread(target=self.__run)
        # 计时器，用于产生一个定时事件，默认时间间隔是1秒
        self.__event_timer = Timer(self.__timer_interval, self.__on_timer)
        # 启动事件处理线程
        self.__event_thread.start()
        # 启动定时器
        self.__event_timer.start()

    def stop(self):
        """引擎关闭方法"""
        # 将引擎开关设为关闭
        self.__active = False
        # 关闭定时器
        self.__event_timer.cancel()
        # 关闭事件处理线程
        self.__event_thread.join()

    def register(self, event_type: EventType, handler: Callable):
        """注册特定事件处理函数监听"""
        # 如果事件名不在列表中，表示是该类型事件第一次注册
        if event_type.name not in self.__handlers.keys():
            # 初始化列表
            self.__handlers[event_type.name] = []
        # 将处理器添加进列表中
        self.__handlers[event_type.name].append(handler)

    def unregister(self, event_type: EventType, handler: Callable):
        """注销特定事件处理函数监听"""
        # 如果没有该类型事件，忽略
        if event_type.name not in self.__handlers.keys():
            return
        # 如果该函数存在于列表中，则移除该处理器
        if handler in self.__handlers[event_type.name]:
            self.__handlers[event_type.name].remove(handler)

    def register_pre_handler(self, handler: Callable):
        """注册前处理器"""
        if handler not in self.__pre_handlers:
            self.__pre_handlers.append(handler)

    def unregister_pre_handler(self, handler: Callable):
        """注销前处理器"""
        if handler in self.__pre_handlers:
            self.__pre_handlers.remove(handler)

    def put(self, event: Event):
        """向事件队列中存入事件"""
        try:
            self.__event_queue.put(event, timeout=1)
        except Full:    # 如果超时仍未得到queue使用权，会导致Full异常
            pass    # 抛弃数据
