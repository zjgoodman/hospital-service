from typing import List
import pandas as pd
from fastapi import Depends
from hospital_service.config import Settings, get_settings
from hospital_service.service import HospitalGeneralInfo


def load_hospital_info_csv(settings: Settings = Depends(get_settings)):
    return load_csv(settings.hospital_info_csv_file_name)


def load_csv(fileName):
    return pd.read_csv(fileName)


def parse_hospital_info_from_csv(csvData) -> List[HospitalGeneralInfo]:
    return [
        parse_hospital_info_from_row(csvData.loc[i]) for i in range(0, len(csvData))
    ]


def parse_hospital_info_from_row(row):
    return HospitalGeneralInfo(
        id=str(row["Facility ID"]),
        name=str(row["Facility ID"]),
        streetAddress=str(row["Facility ID"]),
        city=str(row["Facility ID"]),
        state=str(row["Facility ID"]),
        zip=str(row["Facility ID"]),
        county=str(row["Facility ID"]),
        phone=str(row["Facility ID"]),
        type=str(row["Facility ID"]),
        ownership=str(row["Facility ID"]),
        offersEmergencyServices=None,
        meetsEHRCriteria=None,
        overallRating=None,
        overallRatingNote=str(row["Facility ID"]),
        mortGroupMeasureCount=None,
        countOfFacilityMortMeasures=None,
        countOfMortMeasuresBetter=None,
        CountofMORTMeasuresNoDifferent=str(row["Facility ID"]),
        CountofMORTMeasuresWorse=str(row["Facility ID"]),
        MORTGroupFootnote=str(row["Facility ID"]),
        SafetyGroupMeasureCount=str(row["Facility ID"]),
        CountofFacilitySafetyMeasures=str(row["Facility ID"]),
        CountofSafetyMeasuresBetter=str(row["Facility ID"]),
        CountofSafetyMeasuresNoDifferent=str(row["Facility ID"]),
        CountofSafetyMeasuresWorse=str(row["Facility ID"]),
        SafetyGroupFootnote=str(row["Facility ID"]),
        READMGroupMeasureCount=str(row["Facility ID"]),
        CountofFacilityREADMMeasures=str(row["Facility ID"]),
        CountofREADMMeasuresBetter=str(row["Facility ID"]),
        CountofREADMMeasuresNoDifferent=str(row["Facility ID"]),
        CountofREADMMeasuresWorse=str(row["Facility ID"]),
        READMGroupFootnote=str(row["Facility ID"]),
        PtExpGroupMeasureCount=str(row["Facility ID"]),
        CountofFacilityPtExpMeasures=str(row["Facility ID"]),
        PtExpGroupFootnote=str(row["Facility ID"]),
        TEGroupMeasureCount=str(row["Facility ID"]),
        CountofFacilityTEMeasures=str(row["Facility ID"]),
        TEGroupFootnote=str(row["Facility ID"]),
    )
