import pytest

def is_palindrome(s):
    return s == s[::-1]

def test_palindrome():
    assert is_palindrome("madam")==True
    assert is_palindrome("level")==True

def test_non_palindrome():
    assert is_palindrome("python")==False
    assert is_palindrome("hello")==False

def test_case_sensitive():
    assert is_palindrome("Madam")==False
    assert is_palindrome("Level")==False

def test_empty_string():
    assert is_palindrome("")==True

