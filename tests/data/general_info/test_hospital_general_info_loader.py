from hospital_service.data.general_info.hospital_general_info_loader import (
    parse_hospital_info_from_csv,
)
from hospital_service.data.general_info.hospital_general_info import HospitalGeneralInfo
from hospital_service.data.load_csv import load_csv


def test_load_csv():
    csvData = load_csv("tests/data/general_info/test-hospital-info.csv")
    actual_hospital_info_list = parse_hospital_info_from_csv(csvData)

    assert len(actual_hospital_info_list) == 1
    hospital: HospitalGeneralInfo = actual_hospital_info_list[0]

    assert hospital.id == "10001"
    assert hospital.name == "SOUTHEAST HEALTH MEDICAL CENTER"
    assert hospital.streetAddress == "1108 ROSS CLARK CIRCLE"
    assert hospital.city == "DOTHAN"
    assert hospital.state == "AL"
    assert hospital.zip == "36301"
    assert hospital.county == "Houston"
    assert hospital.phone == "(334) 793-8701"
    assert hospital.type == "Acute Care Hospitals"
    assert hospital.ownership == "Government - Hospital District or Authority"
    assert hospital.offersEmergencyServices == "Yes"
    assert hospital.meetsEHRCriteria == ""
    assert hospital.overallRating == "3"
    assert hospital.overallRatingNote == ""
    assert hospital.mortGroupMeasureCount == "7"
    assert hospital.countOfFacilityMortMeasures == "7"
    assert hospital.countOfMortMeasuresBetter == "0"
    assert hospital.CountofMORTMeasuresNoDifferent == "6"
    assert hospital.CountofMORTMeasuresWorse == "1"
    assert hospital.MORTGroupFootnote == ""
    assert hospital.SafetyGroupMeasureCount == "8"
    assert hospital.CountofFacilitySafetyMeasures == "8"
    assert hospital.CountofSafetyMeasuresBetter == "2"
    assert hospital.CountofSafetyMeasuresNoDifferent == "6"
    assert hospital.CountofSafetyMeasuresWorse == "0"
    assert hospital.SafetyGroupFootnote == ""
    assert hospital.READMGroupMeasureCount == "11"
    assert hospital.CountofFacilityREADMMeasures == "11"
    assert hospital.CountofREADMMeasuresBetter == "1"
    assert hospital.CountofREADMMeasuresNoDifferent == "9"
    assert hospital.CountofREADMMeasuresWorse == "1"
    assert hospital.READMGroupFootnote == ""
    assert hospital.PtExpGroupMeasureCount == "8"
    assert hospital.CountofFacilityPtExpMeasures == "8"
    assert hospital.PtExpGroupFootnote == ""
    assert hospital.TEGroupMeasureCount == "14"
    assert hospital.CountofFacilityTEMeasures == "11"
    assert hospital.TEGroupFootnote == ""
