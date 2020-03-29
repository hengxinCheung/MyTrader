from mytrader.datasource.datasource import DataSource


NAME = "CsvReader"


class CsvReader(DataSource):
    def __init__(self):
        super(CsvReader, self).__init__(name=NAME)

    def get_bars(self, filename):
        """"""
        return []
