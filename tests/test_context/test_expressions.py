import ast
from copy import deepcopy

import pytest

from app_model.expressions import Constant, Expr, Name, parse_expression, safe_eval
from app_model.expressions._expressions import _OPS, _iter_names


def test_names():
    assert Name("n").eval({"n": 5}) == 5

    # currently, evaludating with a missing name is an error.
    with pytest.raises(NameError):
        Name("n").eval()

    assert repr(Name("n")) == "Expr.parse('n')"


def test_constants():
    assert Constant(1).eval() == 1
    assert Constant(3.14).eval() == 3.14

    assert Constant("asdf").eval() == "asdf"
    assert str(Constant("asdf")) == "'asdf'"
    assert str(Constant(r"asdf")) == "'asdf'"

    assert Constant(b"byte").eval() == b"byte"
    assert str(Constant(b"byte")) == "b'byte'"

    assert Constant(True).eval() is True
    assert Constant(False).eval() is False
    assert Constant(None).eval() is None

    assert repr(Constant(1)) == "Expr.parse('1')"

    # only {None, str, bytes, bool, int, float} allowed
    with pytest.raises(TypeError):
        Constant((1, 2))  # type: ignore


def test_bool_ops():
    n1 = Name[bool]("n1")
    true = Constant(True)
    false = Constant(False)

    assert (n1 & true).eval({"n1": True}) is True
    assert (n1 & false).eval({"n1": True}) is False
    assert (n1 & false).eval({"n1": False}) is False
    assert (n1 | true).eval({"n1": True}) is True
    assert (n1 | false).eval({"n1": True}) is True
    assert (n1 | false).eval({"n1": False}) is False

    # real constants
    assert (n1 & True).eval({"n1": True}) is True
    assert (n1 & False).eval({"n1": True}) is False
    assert (n1 & False).eval({"n1": False}) is False
    assert (n1 | True).eval({"n1": True}) is True
    assert (n1 | False).eval({"n1": True}) is True
    assert (n1 | False).eval({"n1": False}) is False

    # when working with Expr objects:
    # the binary "op" & refers to the boolean op "and"
    assert str(Constant(1) & 1) == "1 and 1"
    # note: using "and" does NOT work to combine expressions
    # (in this case, it would just return the second value "1")
    assert not isinstance(Constant(1) and 1, Expr)


def test_bin_ops():
    one = Constant(1)
    assert (one + 1).eval() == 2
    assert (one - 1).eval() == 0
    assert (one * 4).eval() == 4
    assert (one / 4).eval() == 0.25
    assert (one // 4).eval() == 0
    assert (one % 2).eval() == 1
    assert (one % 1).eval() == 0
    assert (Constant(2) ** 2).eval() == 4
    assert (one ^ 2).eval() == 3
    assert (Constant(4) & Constant(16)).eval() == 16
    assert (Constant(4) | Constant(16)).eval() == 4

    assert (Constant(16).bitand(16)).eval() == 16
    assert (Constant(16).bitor(4)).eval() == 20


def test_unary_ops():
    assert Constant(1).eval() == 1
    assert (+Constant(1)).eval() == 1
    assert (-Constant(1)).eval() == -1
    assert Constant(True).eval() is True
    assert (~Constant(True)).eval() is False


def test_comparison():
    n = Name[int]("n")
    n2 = Name[int]("n2")
    one = Constant(1)

    assert (n == n2).eval({"n": 2, "n2": 2})
    assert not (n == n2).eval({"n": 2, "n2": 1})
    assert (n != n2).eval({"n": 2, "n2": 1})
    assert not (n != n2).eval({"n": 2, "n2": 2})
    # real constant
    assert (n != 1).eval({"n": 2})
    assert not (n != 2).eval({"n": 2})

    assert (n < one).eval({"n": -1})
    assert not (n < one).eval({"n": 2})
    assert (n <= one).eval({"n": 0})
    assert (n <= one).eval({"n": 1})
    assert not (n <= one).eval({"n": 2})
    # with real constant
    assert (n < 1).eval({"n": -1})
    assert not (n < 1).eval({"n": 2})
    assert (n <= 1).eval({"n": 0})
    assert (n <= 1).eval({"n": 1})
    assert not (n <= 1).eval({"n": 2})

    assert (n > one).eval({"n": 2})
    assert not (n > one).eval({"n": 1})
    assert (n >= one).eval({"n": 2})
    assert (n >= one).eval({"n": 1})
    assert not (n >= one).eval({"n": 0})
    # real constant
    assert (n > 1).eval({"n": 2})
    assert not (n > 1).eval({"n": 1})
    assert (n >= 1).eval({"n": 2})
    assert (n >= 1).eval({"n": 1})
    assert not (n >= 1).eval({"n": 0})

    assert Expr.in_(Constant("a"), Constant("abcd")).eval() is True
    assert Constant("a").in_(Constant("abcd")).eval() is True

    assert Expr.not_in(Constant("a"), Constant("abcd")).eval() is False
    assert Constant("a").not_in(Constant("abcd")).eval() is False

    assert repr(n > n2) == "Expr.parse('n > n2')"


def test_iter_names():
    expr = "a if b in c else d > e"
    a = parse_expression(expr)
    assert a is parse_expression(a)
    b = Expr.parse(expr)  # alias
    assert sorted(_iter_names(a)) == ["a", "b", "c", "d", "e"]
    assert sorted(_iter_names(b)) == ["a", "b", "c", "d", "e"]

    with pytest.raises(RuntimeError):
        # don't directly instantiate
        Expr()


GOOD_EXPRESSIONS = [
    "a and b",
    "a == 1",
    "a @ 1",
    "2 & 4",
    "a if b == 7 else False",
    # valid constants:
    "1",
    "3.14",
    "True",
    "1 in {1, 2, 3}",
    "1 in [1, 2, 3]",
    "1 in (1, 2, 3)",
    "False",
    "None",
    "hieee",
    "b'bytes'",
    "1 < x < 2",
]

for k, v in _OPS.items():
    if issubclass(k, ast.unaryop):
        GOOD_EXPRESSIONS.append(f"{v} 1" if v == "not" else f"{v}1")
    elif v not in {"is", "is not"}:
        GOOD_EXPRESSIONS.append(f"1 {v} 2")

# these are not supported
BAD_EXPRESSIONS = [
    "a orr b",  # typo
    "a b",  # invalid syntax
    "a = b",  # Assign
    "my.attribute",  # Attribute
    "__import__(something)",  # Call
    'print("hi")',
    '{"key": "val"}',  # dicts not yet supported
    "mylist[0]",  # Index
    "mylist[0:1]",  # Slice
    'f"a"',  # JoinedStr
    "a := 1",  # NamedExpr
    r'f"{a}"',  # FormattedValue
    "[v for v in val]",  # ListComp
    "{v for v in val}",  # SetComp
    r"{k:v for k, v in val}",  # DictComp
    "(v for v in val)",  # GeneratorExp
]


@pytest.mark.parametrize("expr", GOOD_EXPRESSIONS)
def test_serdes(expr):
    assert str(parse_expression(expr)) == expr
    assert repr(parse_expression(expr))  # smoke test


@pytest.mark.parametrize("expr", BAD_EXPRESSIONS)
def test_bad_serdes(expr):
    with pytest.raises(SyntaxError):
        parse_expression(expr)


def test_deepcopy_expression():
    deepcopy(parse_expression("1"))
    deepcopy(parse_expression("1 > 2"))
    deepcopy(parse_expression("1 & 2"))
    deepcopy(parse_expression("1 or 2"))
    deepcopy(parse_expression("not 1"))
    deepcopy(parse_expression("~x"))
    deepcopy(parse_expression("2 if x else 3"))


def test_safe_eval():
    expr = "7 > x if x > 2 else 3"
    assert safe_eval(expr, {"x": 3}) is True
    assert safe_eval(expr, {"x": 10}) is False
    assert safe_eval(expr, {"x": 1}) == 3
    assert safe_eval(True) is True
    assert safe_eval(False) is False
    assert safe_eval("[1,2,3]") == [1, 2, 3]
    assert safe_eval("(1,2,3)") == (1, 2, 3)
    assert safe_eval("{1,2,3}") == {1, 2, 3}

    with pytest.raises(SyntaxError, match="Type 'Call' not supported"):
        safe_eval("func(x)")


def test_eval_kwargs():
    expr = parse_expression("a + b")
    assert expr.eval(a=1, b=2) == 3
    assert expr.eval({"a": 2}, b=2) == 4


@pytest.mark.parametrize("expr", GOOD_EXPRESSIONS)
def test_hash(expr):
    assert isinstance(hash(parse_expression(expr)), int)
