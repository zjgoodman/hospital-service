from typing import List
from hospital_service.data.measures.hospital_measures import HospitalMeasure
from hospital_service.data.load_csv import get_string


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
