import os
import datetime
import logging
from mytrader import BaseEngine
from mytrader.log.object import LogData
from mytrader.log.setting import LOGGER_SETTING


ENGINE_NAME = "LogEngine"


class LogEngine(BaseEngine):
    """日志引擎，负责系统的日志记录功能"""
    def __init__(self):
        super(LogEngine, self).__init__(engine_name=ENGINE_NAME)
        # 获取日志记录名
        self.logger_name = LOGGER_SETTING["logger_name"]
        # 获取日志实例
        self.logger = logging.getLogger(self.logger_name)
        # 获取日志级别
        self.logger_level = LOGGER_SETTING["logger_level"]
        self.console_level = LOGGER_SETTING["console_level"]
        self.file_level = LOGGER_SETTING["file_level"]
        # 设置日志级别
        self.logger.setLevel(LOGGER_SETTING["logger_level"])
        # 获取日志格式
        self.logger_formatter = logging.Formatter(LOGGER_SETTING["logger_formatter"])
        self.console_formatter = logging.Formatter(LOGGER_SETTING["console_formatter"])
        self.file_formatter = logging.Formatter(LOGGER_SETTING["file_formatter"])
        # 获取日志文件信息
        self.dir = LOGGER_SETTING["dir"]
        self.filename_prefix = LOGGER_SETTING["filename_prefix"]
        self.filename_suffix = LOGGER_SETTING["filename_suffix"]
        # 添加处理器
        self.add_null_handler()
        self.add_console_handler()
        self.add_file_handler()

    def add_null_handler(self):
        """"""
        self.logger.addHandler(logging.NullHandler())

    def add_console_handler(self):
        """"""
        # 创建一个控制台处理器
        console_handler = logging.StreamHandler()
        # 设置输出级别
        console_handler.setLevel(self.console_level)
        # 设置输出样式
        console_handler.setFormatter(self.console_formatter)
        # 为日志记录器添加控制台处理器
        self.logger.addHandler(console_handler)

    def add_file_handler(self):
        """"""
        today = datetime.datetime.now().strftime("%Y%m%d")
        filename = "{}_{}.{}".format(self.filename_prefix, today, self.filename_suffix)
        file_path = os.path.join(self.dir, filename)

        print('Log file \'{}\' will be stored in {}'.format(filename, self.dir))

        # 处理文件夹不存在的情况
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

        # 创建文件处理器
        file_handler = logging.FileHandler(file_path, mode='a', encoding='utf-8')
        # 设置输出级别
        file_handler.setLevel(self.file_level)
        # 设置输出样式
        file_handler.setFormatter(self.file_formatter)
        # 为日志记录器添加文件处理器
        self.logger.addHandler(file_handler)

    def write_log(self, data: LogData):
        """"""
        self.logger.log(data.level, data.msg)

    def debug(self, msg: str):
        """"""
        self.logger.log(logging.DEBUG, msg)

    def info(self, msg: str):
        """"""
        self.logger.log(logging.INFO, msg)

    def warning(self, msg: str):
        """"""
        self.logger.log(logging.WARNING, msg)

    def critical(self, msg: str):
        """"""
        self.logger.log(logging.CRITICAL, msg)
