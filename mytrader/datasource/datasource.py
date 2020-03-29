from mytrader.engine import BaseEngine


ENGINE_NAME = "DataSource"


class DataSource(BaseEngine):
    def __init__(self, name):
        super(DataSource, self).__init__(engine_name=ENGINE_NAME)
        # 数据源名称
        self.name = name

    def get_bars(self, *args, **kwargs):
        """得到bar数据"""
        raise NotImplementedError
