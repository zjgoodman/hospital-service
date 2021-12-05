from fastapi.testclient import TestClient
from hospital_service.main import app
from pytest_mock import MockerFixture
from hospital_service.config import Settings

client = TestClient(app)


def test_hello_world():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_get_hospitals(mocker: MockerFixture):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info.csv",
        hospital_treatment_csv_file_name="tests/service/test-measures.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)

    response = client.get("/hospitals")
    assert response.status_code == 200


def test_get_hospitals_without_score_compare_operator():
    response = client.get("/hospitals?score=50")
    assert response.status_code == 400


def test_get_hospitals_with_invalid_score_compare_operator():
    response = client.get("/hospitals?score=50&score_compare_operator=tasty")
    assert response.status_code == 400


def test_get_hospitals_with_score_compare_operator_without_score(mocker: MockerFixture):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info.csv",
        hospital_treatment_csv_file_name="tests/service/test-measures.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)

    response = client.get("/hospitals?score_compare_operator=eq")
    assert response.status_code == 200
