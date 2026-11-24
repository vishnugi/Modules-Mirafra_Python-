import pytest 

def filter_even(numbers):
    return [n for n in numbers if n % 2 == 0]

def test_mixed_numbers():
    assert filter_even([1, 2, 3, 4, 5]) == [2, 4]
    assert filter_even([10, 15, 20, 25]) == [10, 20]

def test_all_even():
    assert filter_even([2, 4, 6, 8]) == [2, 4, 6, 8]


def test_all_odd():
    assert filter_even([1, 3, 5, 7]) == []
    assert filter_even([9, 11, 13]) == []

def tetst_empty_list():
    assert filter_even([]) == []

def test_invalid_input():
    with pytest.raises(TypeError):
        filter_even('not a list')
    with pytest.raises(TypeError):
        filter_even(123)

def test_largest_list():
    assert filter_even(list(range(1, 1001))) == list(range(2, 1001, 2))
    