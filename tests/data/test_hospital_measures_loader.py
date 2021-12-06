from hospital_service.data.load_csv import load_csv
from hospital_service.data.hospital_measures_loader import (
    parse_hospital_measures_from_csv,
)
from hospital_service.models.hospital_measures import HospitalMeasure
import pytest


def test_load_csv():
    csvData = load_csv("tests/data/sample-measures.csv")
    actual_measures = parse_hospital_measures_from_csv(csvData)

    assert len(actual_measures) == 1
    measure: HospitalMeasure = actual_measures[0]

    assert measure.FacilityID == "10001"
    assert measure.Condition == "Preventive Care"
    assert measure.MeasureID == "IMM_3"
    assert measure.MeasureName == "Healthcare workers given influenza vaccination"
    assert measure.Score == "99"
    assert measure.Sample == "4119"
    assert measure.Footnote == ""
    assert measure.StartDate == "10/01/2020"
    assert measure.EndDate == "03/31/2021"


op_22_patients_affected_expectations = [
    (0, 0),
    (1, 470),
    (2, 250),
    (3, 718),
]


@pytest.mark.parametrize(
    "score_to_match,expected_patients_affected", op_22_patients_affected_expectations
)
def test_patients_affected_op_22(score_to_match, expected_patients_affected):
    csvData = load_csv("tests/data/sample-measures-op-22-patients-affected.csv")
    actual_measures = parse_hospital_measures_from_csv(csvData)
    op_22_measures_with_matching_score = list(
        filter(
            lambda measure: measure.MeasureID == "OP_22"
            and measure.Score == str(score_to_match),
            actual_measures,
        )
    )

    assert len(op_22_measures_with_matching_score) == 1
    measure: HospitalMeasure = op_22_measures_with_matching_score[0]
    assert measure.PatientsAffected == expected_patients_affected


def test_patients_affected_is_null_when_op_22_score_not_available():
    csvData = load_csv("tests/data/sample-measures-op-22-patients-affected.csv")
    actual_measures = parse_hospital_measures_from_csv(csvData)
    score_not_available_measures = list(
        filter(
            lambda measure: measure.MeasureID == "OP_22"
            and measure.Score == "Not Available",
            actual_measures,
        )
    )

    assert len(score_not_available_measures) == 1
    assert score_not_available_measures[0].Score == "Not Available"
    assert not score_not_available_measures[0].PatientsAffected


def test_patients_affected_is_null_when_NOT_op_22():
    csvData = load_csv("tests/data/sample-measures-op-22-patients-affected.csv")
    actual_measures = parse_hospital_measures_from_csv(csvData)
    non_op_22_measures = list(
        filter(lambda measure: measure.MeasureID != "OP_22", actual_measures)
    )

    assert len(non_op_22_measures) == 1
    assert non_op_22_measures[0].Score == "99"
    assert not non_op_22_measures[0].PatientsAffected
