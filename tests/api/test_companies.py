import requests


def test_get_companies():

    response = requests.get(
        "http://127.0.0.1:8000/api/v1/companies"
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    assert len(data) > 0


def test_get_company_profile():

    response = requests.get(
        "http://127.0.0.1:8000/api/v1/companies/HDFCBANK"
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    assert (
        data["id"]
        == "HDFCBANK"
    )


def test_invalid_ticker_returns_404():

    response = requests.get(
        "http://127.0.0.1:8000/api/v1/companies/XYZ123"
    )

    assert (
        response.status_code
        == 404
    )


def test_pl_history():

    response = requests.get(
        "http://127.0.0.1:8000/api/v1/companies/HDFCBANK/pl"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0


def test_pl_year_filter():

    response = requests.get(
        "http://127.0.0.1:8000/api/v1/companies/HDFCBANK/pl?from_year=2020"
    )

    assert response.status_code == 200

    data = response.json()

    for row in data:

        year = int(
            row["year"][-4:]
        )

        assert year >= 2020


def test_bs_history():

    response = requests.get(
        "http://127.0.0.1:8000/api/v1/companies/HDFCBANK/bs"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0


def test_bs_year_filter():

    response = requests.get(
        "http://127.0.0.1:8000/api/v1/companies/HDFCBANK/bs?from_year=2020"
    )

    assert response.status_code == 200

    data = response.json()

    for row in data:

        year = int(
            row["year"][-4:]
        )

        assert year >= 2020


def test_cashflow_history():

    response = requests.get(
        "http://127.0.0.1:8000/api/v1/companies/HDFCBANK/cashflow"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0


def test_cashflow_year_filter():

    response = requests.get(
        "http://127.0.0.1:8000/api/v1/companies/HDFCBANK/cashflow?from_year=2020"
    )

    assert response.status_code == 200

    data = response.json()

    for row in data:

        year = int(
            row["year"][-4:]
        )

        assert year >= 2020


def test_ratios_history():

    response = requests.get(
        "http://127.0.0.1:8000/api/v1/companies/HDFCBANK/ratios"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0


def test_ratios_single_year():

    response = requests.get(
        "http://127.0.0.1:8000/api/v1/companies/HDFCBANK/ratios?year=2024"
    )

    assert response.status_code == 200

    data = response.json()

    for row in data:

        assert "2024" in row["year"]


def test_tearsheet_download():

    response = requests.get(
        "http://127.0.0.1:8000/api/v1/companies/HDFCBANK/tearsheet"
    )

    assert response.status_code == 200

    assert (
        response.headers[
            "content-type"
        ]
        ==
        "application/pdf"
    )