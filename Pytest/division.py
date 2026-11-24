import pytest

def divide(a, b):
    return a/b

def test_divide_positive():
    assert divide(6, 2) == 3
    assert divide(10, 5) == 2

def test_divide_negative():
    assert divide(-6, 2) == -3
    assert divide(10, -5) == -2

def test_divide_zero():
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)

def test_invalid_type():
    with pytest.raises(TypeError):
        divide('6', 2)
    with pytest.raises(TypeError):
        divide(6, '2')