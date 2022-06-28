"""A row-oriented dataframe."""

import inspect
from df import DF


class DfRow(DF):
    """Row-wise dataframe."""

    def __init__(self, **kwargs):
        """Initialize from `name=[values]`."""
        assert len(kwargs) > 0
        assert _all_eq(len(kwargs[k]) for k in kwargs)
        assert _all_eq(kwargs[k].keys() for k in kwargs)
        for v in kwargs[0].keys():
            assert _all_eq(type(k[v]) for k in kwargs)
        self._data = kwargs
        self._columns = list(kwargs[0].keys())

    def ncol(self):
        """Report the number of columns."""
        n = set(self._data.keys()).pop()
        return len(self._data[n])

    def nrow(self):
        """Report the number of rows."""
        return len(self._data)

    def cols(self):
        """Return the set of column names."""
        return self._columns

    def eq(self, other):
        """Check equality of two dataframes."""
        assert isinstance(other, DF)
        for n in self._columns:
            if n not in other.cols():
                return False
            for i in range(len(self._data)):
                if self.get(n, i) != other.get(n, i):
                    return False
        return True

    def get(self, col, row):
        """Get a scalar value."""
        assert col in self._columns
        assert 0 <= row < len(self._data)
        return self._data[row][col]

    def set(self, col, row, value):
        """Set a scalar value."""
        assert col in self._columns
        assert 0 <= row < len(self._data)
        assert type(value) == type(self._data[row][col])
        self._data[row][col] = value

    def select(self, *names):
        """Select a subset of columns."""
        assert all(p in self._columns for p in names)
        result = []
        for i in range(self.nrow()):
            result.append({key: value for key, value in self._data[k].items() if key in names})
        return DfRow(**result)

    def filter(self, func):
        """Select a subset of rows."""
        params = list(inspect.signature(func).parameters.keys())
        assert all(p in self._columns for p in params)
        result = []
        for i in range(self.nrow()):
            args = {key: value for key, value in self._data[i].items() if key in params}
            if func(**args):
                result.append(self._data[i])
        return DfRow(**result)


def _all_eq(*values):
    """Assert that all values are equal."""
    return (not values) or all(v == values[0] for v in values)
