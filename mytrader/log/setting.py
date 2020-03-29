import os
# 导入日志模块
import logging

LOGGER_SETTING = {
    "logger_name": "MyTrader",  # 日志记录的名称，默认使用项目名
    "logger_level": logging.DEBUG,  # 日志记录级别
    "console_level": logging.DEBUG,  # 输出在控制台的级别
    "file_level": logging.WARNING,  # 输出在文件的级别
    "logger_formatter": "[%(levelname)s] %(asctime)s: %(message)s",  # 日志记录格式
    "console_formatter": "[%(levelname)s] %(asctime)s: %(message)s",  # 控制台输出格式
    "file_formatter": "[%(levelname)s] %(asctime)s: %(message)s",  # 文件输出格式
    "dir": os.path.join(os.getcwd(), 'logs'),  # 日志文件存放文件夹
    "filename_prefix": 'MyTrader',    # 日志文件名前缀，默认使用项目名
    "filename_suffix": "log",   # 日志文件名后缀
}
