from df_row import DfRow


def test_construct_with_single_value():
    df = DfRow(a={"a" : 1})
    assert df.get("a", 0) == 1


def test_construct_with_two_pairs():
    df = DfRow(a=[1, 2], b=[3, 4])
    assert df.get("a", 0) == 1
    assert df.get("a", 1) == 2
    assert df.get("b", 0) == 3
    assert df.get("b", 1) == 4


def test_nrow():
    assert DfRow(a=[1, 2], b=[3, 4]).nrow() == 2


def test_ncol():
    assert DfRow(a=[1, 2], b=[3, 4]).ncol() == 2


def test_equality():
    left = DfRow(a=[1, 2], b=[3, 4])
    right = DfRow(b=[3, 4], a=[1, 2])
    assert left.eq(right) and right.eq(left)


def test_inequality():
    left = DfRow(a=[1, 2], b=[3, 4])
    assert not left.eq(DfRow(a=[1, 2]))
    assert not left.eq(DfRow(a=[1, 2], b=[1, 2]))


def test_select():
    df = DfRow(a=[1, 2], b=[3, 4])
    selected = df.select("a")
    assert selected.eq(DfRow(a=[1, 2]))


def test_filter():
    def odd(a, b):
        return (a % 2) == 1
    df = DfRow(a=[1, 2], b=[3, 4])
    assert df.filter(odd).eq(DfRow(a=[1], b=[3]))
