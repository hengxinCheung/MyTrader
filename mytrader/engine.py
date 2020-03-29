import threading


class BaseEngine(object):
    """基础引擎，所有的功能模块必须继承该引擎，可保证所有的引擎都是单例的"""
    _instance_lock = threading.Lock()   # 实例锁，以实现单例模式

    def __init__(self, engine_name: str):
        self.engine_name = engine_name

    def __new__(cls, *args, **kwargs):
        """当实例化一个对象时，会先执行类的__new__方法，再执行类的__init__方法"""
        # 判断此类有没有_instance属性(这个判断其实可以去掉，只是为了优化实例化速度，避免不必要的锁操作)
        if not hasattr(cls, '__instance'):
            # 为了防止多线程运行导致重复初始化，必须加锁
            with cls._instance_lock:
                # 再次判断是否具有_instance属性(有可能在加锁时有别的线程创建了实例),如果没有则创建一个
                if not hasattr(cls, '_instance'):
                    cls._instance = object.__new__(cls)
        # 返回实例对象
        return cls._instance
