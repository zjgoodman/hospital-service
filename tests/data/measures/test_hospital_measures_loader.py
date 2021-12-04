from hospital_service.data.load_csv import load_csv
from hospital_service.data.measures.hospital_measures_loader import (
    parse_hospital_measures_from_csv,
)
from hospital_service.data.measures.hospital_measures import HospitalMeasure


def test_load_csv():
    csvData = load_csv("tests/data/measures/sample-measures.csv")
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
