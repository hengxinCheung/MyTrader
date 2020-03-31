from dataclasses import dataclass
from typing import Any
import datetime


@dataclass()
class Indicator(object):
    name: str  # 指标名
    value: Any  # 指标值
    time: (datetime, str)  # 生成时间
