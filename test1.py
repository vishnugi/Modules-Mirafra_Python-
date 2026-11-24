import pytest

def add(a,b):
    return a+b

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 2, 3),
        (2, 3, 5),
        (-1, 1, 0),
        (2, 3, 5),
    ]
)
def test_add(a, b, expected):
    assert add(a, b) == expected
# import sys 
# import subprocess
# arg=sys.argv[1:]
# print(subprocess.run(arg,capture_output=True,text=True))
# print(arg)