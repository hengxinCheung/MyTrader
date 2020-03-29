import numpy as np


def fit_series(*series_list):
    size = min(len(series) for series in series_list)
    if size == 0:
        raise TypeError("The size of series can not equal to 0")
    new_series_list = [series[-size:] for series in series_list]
    return new_series_list


def get_value(val):
    if isinstance(val, TimeSeries):
        return val.value
    else:
        return val


def get_series(val):
    if isinstance(val, TimeSeries):
        return val.series
    else:
        return DuplicateNumericSeries(val).series


def ensure_timeseries(series):
    if isinstance(series, TimeSeries):
        return series
    else:
        return DuplicateNumericSeries(series)


class TimeSeries(object):
    @property
    def series(self):
        raise NotImplementedError

    @property
    def value(self):
        try:
            return self.series[-1]
        except IndexError:
            raise TypeError("DATA UNAVAILABLE")

    def __len__(self):
        return len(self.series)

    def __lt__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 < s2
        return BoolSeries(series)

    def __gt__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 > s2
        return BoolSeries(series)

    def __eq__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 == s2
        return BoolSeries(series)

    def __ne__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 != s2
        return BoolSeries(series)

    def __ge__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 >= s2
        return BoolSeries(series)

    def __le__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 <= s2
        return BoolSeries(series)

    def __sub__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 - s2
        return NumericSeries(series)

    def __rsub__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s2 - s1
        return NumericSeries(series)

    def __add__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 + s2
        return NumericSeries(series)

    def __radd__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s2 + s1
        return NumericSeries(series)

    def __mul__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 * s2
        return NumericSeries(series)

    def __rmul__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s2 * s1
        return NumericSeries(series)

    def __truediv__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 / s2
        return NumericSeries(series)

    def __rtruediv__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s2 / s1
        return NumericSeries(series)

    __div__ = __truediv__

    def __bool__(self):
        return len(self) > 0 and bool(self.value)

    def __and__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        return BoolSeries(s1 & s2)

    def __or__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        return BoolSeries(s1 | s2)

    def __invert__(self):
        with np.errstate(invalid='ignore'):
            series = ~self.series
        return BoolSeries(series)

    # fix bug in python 2
    __nonzero__ = __bool__

    def __repr__(self):
        return str(self.value)


class NumericSeries(TimeSeries):
    def __init__(self, series=[]):
        super(NumericSeries, self).__init__()
        self._series = series
        self.extra_create_kwargs = {}

    @property
    def series(self):
        return self._series

    def __getitem__(self, index):
        assert isinstance(index, int) and index >= 0
        return self.__class__(series=self.series[:len(self.series) - index], **self.extra_create_kwargs)


class DuplicateNumericSeries(NumericSeries):
    # FIXME size should come from other series
    def __init__(self, series, size=640000):
        try:
            val = series[-1]
        except:
            val = series
        super(DuplicateNumericSeries, self).__init__(np.full(size, val, dtype=np.float64))


class BoolSeries(NumericSeries):
    pass