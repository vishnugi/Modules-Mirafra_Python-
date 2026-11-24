import pytest

def add(a,b):
    return a+b


def test_positive_num():
    assert add(2,3)==5
def test_neg_num():
    assert add(-2,-2)==-4
    assert add(3,-2)==1
    assert add(-4,3)==-1
def test_zero():
    assert add(0,0)==0
    assert add(3,0)==3
    assert add (0,-4)==-4
def test_invalid():
    with pytest.raises(TypeError):
        add('1',6)
