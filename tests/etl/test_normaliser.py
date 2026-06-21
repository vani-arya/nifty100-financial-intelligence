import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.normaliser import normalize_ticker, normalize_year

# ==========================================

# TICKER TESTS (20)

# ==========================================

def test_normalize_ticker_01():
    assert normalize_ticker("abb") == "ABB"

def test_normalize_ticker_02():
    assert normalize_ticker("tcs") == "TCS"

def test_normalize_ticker_03():
    assert normalize_ticker("infy") == "INFY"

def test_normalize_ticker_04():
    assert normalize_ticker("wipro") == "WIPRO"

def test_normalize_ticker_05():
    assert normalize_ticker("reliance") == "RELIANCE"

def test_normalize_ticker_06():
    assert normalize_ticker("  tcs  ") == "TCS"

def test_normalize_ticker_07():
    assert normalize_ticker(" infy") == "INFY"

def test_normalize_ticker_08():
    assert normalize_ticker("wipro ") == "WIPRO"

def test_normalize_ticker_09():
    assert normalize_ticker("INFY") == "INFY"

def test_normalize_ticker_10():
    assert normalize_ticker("TCS") == "TCS"

def test_normalize_ticker_11():
    assert normalize_ticker("BAJAJ-AUTO") == "BAJAJ-AUTO"

def test_normalize_ticker_12():
    assert normalize_ticker("bajaj-auto") == "BAJAJ-AUTO"

def test_normalize_ticker_13():
    assert normalize_ticker("M&M") == "M&M"

def test_normalize_ticker_14():
    assert normalize_ticker("m&m") == "M&M"

def test_normalize_ticker_15():
    assert normalize_ticker("ULTRACEMCO") == "ULTRACEMCO"

def test_normalize_ticker_16():
    assert normalize_ticker("ultracemco") == "ULTRACEMCO"

def test_normalize_ticker_17():
    assert normalize_ticker("HDFCBANK") == "HDFCBANK"

def test_normalize_ticker_18():
    assert normalize_ticker("hdfcbank") == "HDFCBANK"

def test_normalize_ticker_19():
    assert normalize_ticker("") == ""

def test_normalize_ticker_20():
    assert normalize_ticker(None) is None

# ==========================================

# YEAR TESTS (20)

# ==========================================

def test_normalize_year_01():
    assert normalize_year("Dec 2012") == 2012

def test_normalize_year_02():
    assert normalize_year("Mar 2014") == 2014

def test_normalize_year_03():
    assert normalize_year("Jun 2018") == 2018

def test_normalize_year_04():
    assert normalize_year("Sep 2020") == 2020

def test_normalize_year_05():
    assert normalize_year("Dec 2023") == 2023

def test_normalize_year_06():
    assert normalize_year("Mar 2024") == 2024

def test_normalize_year_07():
    assert normalize_year("2024") == 2024

def test_normalize_year_08():
    assert normalize_year("2023") == 2023

def test_normalize_year_09():
    assert normalize_year("2022") == 2022

def test_normalize_year_10():
    assert normalize_year("Mar-13") == 2013

def test_normalize_year_11():
    assert normalize_year("Mar-14") == 2014

def test_normalize_year_12():
    assert normalize_year("Mar-15") == 2015

def test_normalize_year_13():
    assert normalize_year("Mar-20") == 2020

def test_normalize_year_14():
    assert normalize_year("Mar-22") == 2022

def test_normalize_year_15():
    assert normalize_year("Mar-24") == 2024

def test_normalize_year_16():
    assert normalize_year("Mar 2016 9m") == 2016

def test_normalize_year_17():
    assert normalize_year("2024.5") == 2024

def test_normalize_year_18():
    assert normalize_year("Mar 2023 15") == 2023

def test_normalize_year_19():
    assert normalize_year(None) is None

def test_normalize_year_20():
    assert normalize_year(" 2021 ") == 2021
