from typing import List
from hospital_service.data.measures.hospital_measures import HospitalMeasure
from hospital_service.data.load_csv import get_string, load_csv
import hospital_service.config as config


def load_measures() -> List[HospitalMeasure]:
    settings = config.get_settings()
    hospital_info = load_csv(settings.hospital_treatment_csv_file_name)
    return parse_hospital_measures_from_csv(hospital_info)


def parse_hospital_measures_from_csv(csvData) -> List[HospitalMeasure]:
    return [
        parse_hospital_measure_from_row(csvData.loc[i]) for i in range(0, len(csvData))
    ]


def parse_hospital_measure_from_row(row):
    return HospitalMeasure(
        FacilityID=get_string(row["Facility ID"]),
        Condition=get_string(row["Condition"]),
        MeasureID=get_string(row["Measure ID"]),
        MeasureName=get_string(row["Measure Name"]),
        Score=get_string(row["Score"]),
        Sample=get_string(row["Sample"]),
        Footnote=get_string(row["Footnote"]),
        StartDate=get_string(row["Start Date"]),
        EndDate=get_string(row["End Date"]),
    )
