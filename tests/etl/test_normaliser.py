import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from src.etl.normaliser import normalize_ticker, normalize_year


def test_normalize_ticker_uppercase():
    assert normalize_ticker("abb") == "ABB"


def test_normalize_ticker_strip_spaces():
    assert normalize_ticker("  tcs  ") == "TCS"


def test_normalize_ticker_already_clean():
    assert normalize_ticker("INFY") == "INFY"


def test_normalize_year_dec_format():
    assert normalize_year("Dec 2012") == 2012


def test_normalize_year_mar_format():
    assert normalize_year("Mar 2014") == 2014


def test_normalize_year_short_format():
    assert normalize_year("Mar-15") == 2015


def test_normalize_year_short_format_2():
    assert normalize_year("Mar-13") == 2013