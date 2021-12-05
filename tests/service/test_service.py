from typing import Dict, List
from hospital_service.service import (
    get_hospitals,
    get_hospitals_as_dictionary,
    Hospital,
    get_hospitals_by_criteria,
)
import hospital_service.config as config
from hospital_service.config import Settings
from pytest_mock import MockerFixture
import pytest


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


def test_get_hospitals_without_filters(mocker: MockerFixture):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info-filters.csv",
        hospital_treatment_csv_file_name="tests/service/test-measures-filters.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)
    actual_hospitals: List[Hospital] = get_hospitals()

    assert len(actual_hospitals) == 276


def test_get_hospitals_by_measure_op_31(mocker: MockerFixture):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info-filters.csv",
        hospital_treatment_csv_file_name="tests/service/test-measures-filters.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)

    measureId: str = "OP_31"
    actual_hospitals: List[Hospital] = get_hospitals_by_criteria(measureId)

    assert len(actual_hospitals) == 176
    # to verify the count, grep the file
    # grep OP_31 tests/service/test-measures-filters.csv | wc -l
    # 176


def test_get_hospitals_by_measure_op_22(mocker: MockerFixture):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info-filters.csv",
        hospital_treatment_csv_file_name="tests/service/test-measures-filters.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)

    measureId: str = "OP_22"
    actual_hospitals: List[Hospital] = get_hospitals_by_criteria(measureId)

    assert len(actual_hospitals) == 177
    # to verify the count, grep the file
    # grep OP_22 tests/service/test-measures-filters.csv | wc -l
    # 177


score_operators_expectations = [
    ("eq", 1),
    ("ge", 2),
    ("le", 2),
    ("gt", 1),
    ("lt", 1),
    ("ne", 2),
]


@pytest.mark.parametrize(
    "score_compare_operator,expected_count", score_operators_expectations
)
def test_get_hospitals_by_score_operator(
    mocker: MockerFixture, score_compare_operator, expected_count
):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info-filters-score.csv",
        hospital_treatment_csv_file_name="tests/service/test-measures-filters-score.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)

    score = 2
    actual_hospitals: List[Hospital] = get_hospitals_by_criteria(
        score=score, score_compare_operator=score_compare_operator
    )

    assert len(actual_hospitals) == expected_count
