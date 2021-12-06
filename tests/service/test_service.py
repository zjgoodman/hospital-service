from typing import Dict, List
from hospital_service.service import (
    get_hospitals,
    get_hospitals_as_dictionary,
    get_hospitals_by_criteria,
    get_hospitals_by_state_ranked_by_measure,
    get_total_patients_impacted_by_measure,
    get_total_patients_in_all_states,
    rank_states_by_patients_affected,
)
from hospital_service.models.hospital import Hospital
from hospital_service.models.rank_states_by_hospital_measure import (
    RankStatesByHospitalMeasure,
)
from hospital_service.models.state_rank_by_hospital_measure import (
    StateRankByHospitalMeasure,
)
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


# to verify the count, grep the file
# grep OP_31 tests/service/test-measures-filters.csv | wc -l
measure_expectations = [
    ("OP_31", 176),
    ("OP_22", 177),
]


@pytest.mark.parametrize("measureId,expected_count", measure_expectations)
def test_get_hospitals_by_measure(mocker: MockerFixture, measureId, expected_count):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info-filters.csv",
        hospital_treatment_csv_file_name="tests/service/test-measures-filters.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)

    actual_hospitals: List[Hospital] = get_hospitals_by_criteria(measureId)

    assert len(actual_hospitals) == expected_count


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


measure_and_score_expectations = [
    ("OP_22", "ge", 1, 92),
    ("OP_22", "ge", 2, 56),
    ("OP_22", "ge", 3, 22),
    ("OP_22", "ge", 3, 22),
    ("OP_22", "ge", 4, 10),
    ("OP_22", "ge", 5, 5),
    ("OP_22", "ge", 6, 2),
    ("OP_22", "ge", 7, 0),
    ("OP_18b", "ge", None, 177),
    ("OP_18b", "ge", 50, 150),
    ("OP_18b", "ge", 100, 140),
    ("OP_18b", "ge", 150, 75),
    ("OP_18b", "ge", 200, 32),
    ("OP_18b", "ge", 250, 4),
    ("OP_18b", "ge", 300, 0),
]


@pytest.mark.parametrize(
    "measureId,score_compare_operator,score,expected_count",
    measure_and_score_expectations,
)
def test_get_hospitals_by_measure_and_score(
    mocker: MockerFixture, measureId, score_compare_operator, score, expected_count
):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info-filters.csv",
        hospital_treatment_csv_file_name="tests/service/test-measures-filters.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)

    actual_hospitals: List[Hospital] = get_hospitals_by_criteria(
        score=score, measureId=measureId, score_compare_operator=score_compare_operator
    )

    assert len(actual_hospitals) == expected_count


def test_get_hospitals_by_state_ranked_by_measure_total_patients(mocker: MockerFixture):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info-state.csv",
        hospital_treatment_csv_file_name="tests/service/test-measures-state.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)

    rank_report: RankStatesByHospitalMeasure = get_hospitals_by_state_ranked_by_measure(
        "OP_22"
    )

    assert rank_report.measure == "OP_22"
    assert len(rank_report.states) == 2

    stateAL = list(filter(lambda state: state.state == "AL", rank_report.states))[0]

    assert stateAL.state == "AL"
    assert stateAL.total_patients_impacted_by_measure == 32038

    stateAK = list(filter(lambda state: state.state == "AK", rank_report.states))[0]

    assert stateAK.state == "AK"
    assert stateAK.total_patients_impacted_by_measure == 238


def test_get_hospitals_by_state_ranked_by_measure_total_patients_for_all_states(
    mocker: MockerFixture,
):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info-state.csv",
        hospital_treatment_csv_file_name="tests/service/test-measures-state.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)

    rank_report: RankStatesByHospitalMeasure = get_hospitals_by_state_ranked_by_measure(
        "OP_22"
    )

    assert rank_report.measure == "OP_22"
    assert rank_report.total_patients_impacted_by_measure == 32276
    assert len(rank_report.states) == 2


def test_rank_states_by_patients_affected():
    state_reports = {
        "TX": StateRankByHospitalMeasure(
            state="TX", total_patients_impacted_by_measure=1, hospitals=[]
        ),
        "TN": StateRankByHospitalMeasure(
            state="TN", total_patients_impacted_by_measure=2, hospitals=[]
        ),
        "FL": StateRankByHospitalMeasure(
            state="FL", total_patients_impacted_by_measure=3, hospitals=[]
        ),
    }
    rank_states_by_patients_affected(list(state_reports.values()))
    assert state_reports["TX"].rank == 2
    assert state_reports["TN"].rank == 1
    assert state_reports["FL"].rank == 0


def test_rank_states_by_patients_affected_tie():
    state_reports = {
        "TX": StateRankByHospitalMeasure(
            state="TX", total_patients_impacted_by_measure=1, hospitals=[]
        ),
        "TN": StateRankByHospitalMeasure(
            state="TN", total_patients_impacted_by_measure=1, hospitals=[]
        ),
        "FL": StateRankByHospitalMeasure(
            state="FL", total_patients_impacted_by_measure=3, hospitals=[]
        ),
    }
    rank_states_by_patients_affected(list(state_reports.values()))
    assert state_reports["TX"].rank == 1
    assert state_reports["TN"].rank == 1
    assert state_reports["FL"].rank == 0


def test_rank_states_by_patients_affected_none():
    state_reports = {
        "TX": StateRankByHospitalMeasure(state="TX", hospitals=[]),
        "TN": StateRankByHospitalMeasure(
            state="TN", total_patients_impacted_by_measure=5, hospitals=[]
        ),
        "FL": StateRankByHospitalMeasure(
            state="FL", total_patients_impacted_by_measure=3, hospitals=[]
        ),
    }
    rank_states_by_patients_affected(list(state_reports.values()))
    assert state_reports["TX"].rank == None
    assert state_reports["TN"].rank == 0
    assert state_reports["FL"].rank == 1


def test_get_hospitals_by_state_ranked_by_measure_rank(mocker: MockerFixture):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info-state.csv",
        hospital_treatment_csv_file_name="tests/service/test-measures-state.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)

    rank_report: RankStatesByHospitalMeasure = get_hospitals_by_state_ranked_by_measure(
        "OP_22"
    )

    assert rank_report.measure == "OP_22"
    assert len(rank_report.states) == 2

    stateAL = list(filter(lambda state: state.state == "AL", rank_report.states))[0]

    assert stateAL.state == "AL"
    assert stateAL.rank == 0

    stateAK = list(filter(lambda state: state.state == "AK", rank_report.states))[0]

    assert stateAK.state == "AK"
    assert stateAK.rank == 1


def test_get_total_patients_impacted_by_measure(mocker: MockerFixture):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info.csv",
        hospital_treatment_csv_file_name="tests/data/sample-measures-op-22-patients-affected.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)

    hospitals: List[Hospital] = get_hospitals()
    measure_id: str = "OP_22"

    actual_total = get_total_patients_impacted_by_measure(hospitals, measure_id)
    assert actual_total == 1438


def test_get_total_patients_impacted_by_measure_unsupported_measure(
    mocker: MockerFixture,
):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info.csv",
        hospital_treatment_csv_file_name="tests/data/sample-measures-op-22-patients-affected.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)

    hospitals: List[Hospital] = get_hospitals()
    measure_id: str = "OP_31"

    actual_total = get_total_patients_impacted_by_measure(hospitals, measure_id)
    assert actual_total == None


def test_get_total_patients_impacted_by_measure_none(mocker: MockerFixture):
    mock_settings: Settings = Settings(
        hospital_info_csv_file_name="tests/service/test-hospital-info.csv",
        hospital_treatment_csv_file_name="tests/service/test-measures-op-22-score-not-available.csv",
    )

    mocker.patch("hospital_service.config.get_settings", return_value=mock_settings)

    hospitals: List[Hospital] = get_hospitals()
    measure_id: str = "OP_22"

    actual_total = get_total_patients_impacted_by_measure(hospitals, measure_id)
    assert actual_total == None


def test_get_total_patients_in_all_states():
    state_reports: List[StateRankByHospitalMeasure] = [
        StateRankByHospitalMeasure(state="TX", total_patients_impacted_by_measure=1),
        StateRankByHospitalMeasure(state="TN", total_patients_impacted_by_measure=None),
    ]
    actual_total: int = get_total_patients_in_all_states(state_reports)
    assert actual_total == 1
