from cal import add, sub

def test_add():
    assert add(2,3)==5
    assert add(-1,-2)==-3

def test_sub():
    assert sub(1,1)==0
    assert sub(-1,-2)==1
    assert sub(5,6)==-1

