# import calculator
import pytest
from calculator import add,sub,mul,div


@pytest.mark.parametrize(
    "a, b, expected",
     [
         (1, 1, 3),
         (2, 3, 5),
         (-1, 0, 0),
         (2, 3, 5),
    ]
)
def test_add(a,b,expected):
    assert add(a,b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
     [
         (1, 1, 0),
         (3, 2, 1),
         (-1, 1, -2),
         (-1, -1, 0),
    ]
)
def test_sub(a,b,expected):
    assert sub(a,b) == expected

@pytest.mark.parametrize(
    "a, b, expected",
     [
         (1, 1, 1),
         (3, 0, 0),
         (-2, 1, -2),
         (-1, -3, 3),
    ]
)
def test_mul(a,b,expected):
    assert mul(a,b) == expected

@pytest.mark.parametrize(
    "a, b, expected",
     [
         (1, 1, 1),
         (4, 2, 2),
         (0, 1, 0),
        #  (2, 0, 0),
    ]
)

def test_div(a,b,expected):
    assert div(a,b) == expected

