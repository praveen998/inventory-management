import pytest
from .utils import addnum

def test_add_num():
    result1=addnum(5,6)
    assert result1==12
    result2=addnum(6,8)
    assert result2==14

  