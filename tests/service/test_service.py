from typing import Dict, List
from hospital_service.service import get_hospitals_as_dictionary, Hospital
from hospital_service.config import Settings
from pytest_mock import MockerFixture


def test_hospitals_have_general_info_and_measures(mocker: MockerFixture):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info.csv",
        hospital_treatment_csv_file_name="tests/service/test-measures.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)

    actual_hospitals: Dict = get_hospitals_as_dictionary()

    assert len(actual_hospitals) == 2

    assert actual_hospitals["10001"]["general_info"]
    assert len(actual_hospitals["10001"]["measures"]) == 2

    assert actual_hospitals["10005"]["general_info"]
    assert len(actual_hospitals["10005"]["measures"]) == 3
