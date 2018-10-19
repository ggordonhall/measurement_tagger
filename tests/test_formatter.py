import pytest

from ..modules import formatter


formatter_obj = formatter.DistanceFormatter()


def test_split_numerals():
    assert formatter.split_numerals("a") == ["a"]
    assert formatter.split_numerals("1aa1") == ["1", "aa", "1"]
    assert formatter.split_numerals("12feetlong") == ["12", "feetlong"]
    assert formatter.split_numerals("12feet12") == ["12", "feet", "12"]


def test_replace_ft():
    assert formatter.replace_ft("ft") == "foot"
    assert formatter.replace_ft("feet") != "foot"
    assert formatter.replace_ft("ft ") != "foot"


def test_replace_feet_inches():
    assert formatter.replace_feet_inches("3'7\"") == "3 foot 7 inch"
    assert formatter.replace_feet_inches("3423'7\"") == "3423 foot 7 inch"
    assert formatter.replace_feet_inches("3'6") == "3 foot 6 inch"
    assert formatter.replace_feet_inches("3\"") != "3 inch"
    assert formatter.replace_feet_inches("3'7") == "3 foot 7 inch"


def test_remove_commas():
    assert formatter.remove_commas("5,000") == "5000"
    assert formatter.remove_commas("5,000,000") == "5000000"
    assert formatter.remove_commas("(5,000)") == "(5000)"
    assert formatter.remove_commas("5,0000 times") != "5000 times"


def test_format():
    format_result = formatter_obj.format("3 ft 7")
    assert format_result == "3 foot 7"
    format_result = formatter_obj.format(
        "I am 3'7\" and I live 5,000 miles from here.")
    assert format_result == "I am 3 foot 7 inch and I live 5000 miles from here."
    format_result = formatter_obj.format("55miles away 2times")
    assert format_result == "55 miles away 2 times"
    format_result = formatter_obj.format("(3'7)")
    assert format_result == "(3 foot 7)"
