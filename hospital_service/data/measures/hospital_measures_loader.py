from typing import List, Optional

from pydantic.types import OptionalInt
from hospital_service.data.measures.hospital_measures import HospitalMeasure
from hospital_service.data.load_csv import get_string, load_csv
import hospital_service.config as config
from functools import lru_cache
import numpy as np


def load_measures() -> List[HospitalMeasure]:
    settings = config.get_settings()
    return load_measures_from_csv(settings.hospital_treatment_csv_file_name)


@lru_cache()
def load_measures_from_csv(csv_file_name: str) -> List[HospitalMeasure]:
    hospital_info = load_csv(csv_file_name)
    return parse_hospital_measures_from_csv(hospital_info)


def parse_hospital_measures_from_csv(csvData) -> List[HospitalMeasure]:
    return [
        parse_hospital_measure_from_row(csvData.loc[i]) for i in range(0, len(csvData))
    ]


def parse_hospital_measure_from_row(row):
    measure_id: str = get_string(row["Measure ID"])
    score: str = get_string(row["Score"])
    sample: str = get_string(row["Sample"])
    patients_affected: OptionalInt = get_patients_affected(measure_id, score, sample)
    return HospitalMeasure(
        FacilityID=get_string(row["Facility ID"]),
        Condition=get_string(row["Condition"]),
        MeasureName=get_string(row["Measure Name"]),
        Footnote=get_string(row["Footnote"]),
        StartDate=get_string(row["Start Date"]),
        EndDate=get_string(row["End Date"]),
        MeasureID=measure_id,
        Score=score,
        Sample=sample,
        PatientsAffected=patients_affected,
    )


def get_patients_affected(measure_id, score, sample) -> OptionalInt:
    if (
        not score
        or not sample
        or not measure_id == "OP_22"
        or score == "Not Available"
        or sample == "Not Available"
    ):
        return None
    return int(int(score) / 100 * int(float(sample)))
