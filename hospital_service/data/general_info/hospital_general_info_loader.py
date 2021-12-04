from typing import List
from hospital_service.data.general_info.hospital_general_info import HospitalGeneralInfo
from hospital_service.data.load_csv import load_csv, get_string
import hospital_service.config as config


def load_hospital_info() -> List[HospitalGeneralInfo]:
    settings = config.get_settings()
    hospital_info = load_csv(settings.hospital_info_csv_file_name)
    return parse_hospital_info_from_csv(hospital_info)


def parse_hospital_info_from_csv(csvData) -> List[HospitalGeneralInfo]:
    return [
        parse_hospital_info_from_row(csvData.loc[i]) for i in range(0, len(csvData))
    ]


def parse_hospital_info_from_row(row):
    return HospitalGeneralInfo(
        id=get_string(row["Facility ID"]),
        name=get_string(row["Facility Name"]),
        streetAddress=get_string(row["Address"]),
        city=get_string(row["City"]),
        state=get_string(row["State"]),
        zip=get_string(row["ZIP Code"]),
        county=get_string(row["County Name"]),
        phone=get_string(row["Phone Number"]),
        type=get_string(row["Hospital Type"]),
        ownership=get_string(row["Hospital Ownership"]),
        offersEmergencyServices=get_string(row["Emergency Services"]),
        meetsEHRCriteria=get_string(
            row["Meets criteria for promoting interoperability of EHRs"]
        ),
        overallRating=get_string(row["Hospital overall rating"]),
        overallRatingNote=get_string(row["Hospital overall rating footnote"]),
        mortGroupMeasureCount=get_string(row["MORT Group Measure Count"]),
        countOfFacilityMortMeasures=get_string(row["Count of Facility MORT Measures"]),
        countOfMortMeasuresBetter=get_string(row["Count of MORT Measures Better"]),
        CountofMORTMeasuresNoDifferent=get_string(
            row["Count of MORT Measures No Different"]
        ),
        CountofMORTMeasuresWorse=get_string(row["Count of MORT Measures Worse"]),
        MORTGroupFootnote=get_string(row["MORT Group Footnote"]),
        SafetyGroupMeasureCount=get_string(row["Safety Group Measure Count"]),
        CountofFacilitySafetyMeasures=get_string(
            row["Count of Facility Safety Measures"]
        ),
        CountofSafetyMeasuresBetter=get_string(row["Count of Safety Measures Better"]),
        CountofSafetyMeasuresNoDifferent=get_string(
            row["Count of Safety Measures No Different"]
        ),
        CountofSafetyMeasuresWorse=get_string(row["Count of Safety Measures Worse"]),
        SafetyGroupFootnote=get_string(row["Safety Group Footnote"]),
        READMGroupMeasureCount=get_string(row["READM Group Measure Count"]),
        CountofFacilityREADMMeasures=get_string(
            row["Count of Facility READM Measures"]
        ),
        CountofREADMMeasuresBetter=get_string(row["Count of READM Measures Better"]),
        CountofREADMMeasuresNoDifferent=get_string(
            row["Count of READM Measures No Different"]
        ),
        CountofREADMMeasuresWorse=get_string(row["Count of READM Measures Worse"]),
        READMGroupFootnote=get_string(row["READM Group Footnote"]),
        PtExpGroupMeasureCount=get_string(row["Pt Exp Group Measure Count"]),
        CountofFacilityPtExpMeasures=get_string(
            row["Count of Facility Pt Exp Measures"]
        ),
        PtExpGroupFootnote=get_string(row["Pt Exp Group Footnote"]),
        TEGroupMeasureCount=get_string(row["TE Group Measure Count"]),
        CountofFacilityTEMeasures=get_string(row["Count of Facility TE Measures"]),
        TEGroupFootnote=get_string(row["TE Group Footnote"]),
    )
