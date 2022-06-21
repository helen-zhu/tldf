"""A row-oriented dataframe."""

import inspect
from df import DF


class DfRow(DF):
    """Row-wise dataframe."""

    def __init__(self, **kwargs):
        """Initialize from `name=[values]`."""
        assert len(kwargs) > 0
        assert _all_eq(len(kwargs[k]) for k in kwargs)
        for k in kwargs:
            assert _all_eq(type(v) for v in kwargs[k])
        self._data = kwargs

    def ncol(self):
        """Report the number of columns."""
        # Easy - swap
        n = set(self._data.keys()).pop()
        return len(self._data[n])

    def nrow(self):
        """Report the number of rows."""
        # Easy - swap
        return len(self._data)

    def cols(self):
        """Return the set of column names."""
        # How does one set column names in this case?
        # Does one just set this to rows?
        # This one is hard
        return set(self._data.keys())

    def rows(self):
        """Return the set of row names."""
        # Easy
        return set(self._data.keys())

    def eq(self, other):
        """Check equality of two dataframes."""
        # Easy
        assert isinstance(other, DF)
        for n in self._data:
            if n not in other.rows():
                return False
            for i in range(len(self._data[n])):
                if self.get(n, i) != other.get(n, i):
                    return False
        return True

    def get(self, col, row):
        """Get a scalar value."""
        # Easy
        assert row in self._data
        assert 0 <= col < len(self._data[row])
        return self._data[row][col]

    def set(self, col, row, value):
        """Set a scalar value."""
        # Easy
        assert row in self._data
        assert 0 <= col < len(self._data[row])
        assert type(value) == type(self._data[row][col])
        self._data[row][col] = value

    def select(self, *names):
        """Select a subset of columns."""
        # Difficult
        assert all(p in self.cols() for p in names)
        result = {n:[] for n in self._data}
        for i in range(self.nrow()):
            result[i] = self._data[i][names] # Figure out how to do this selection somehow
        return DfRow(**result)

    def filter(self, func):
        """Select a subset of rows."""
        # Medium: difficult because of the function, but not as logically challenging
        params = list(inspect.signature(func).parameters.keys())
        assert all(p in self.cols() for p in params)
        result = {}
        for i in range(self.nrow()):
            args = {n:self._data[i][n] for n in params}
            if func(**args):
                result.append(self._data[i])
        return DfRow(**result)


def _all_eq(*values):
    """Assert that all values are equal."""
    return (not values) or all(v == values[0] for v in values)
