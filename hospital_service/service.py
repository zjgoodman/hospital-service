from typing import Dict, List

from pydantic.main import BaseModel
from hospital_service.data.general_info.hospital_general_info_loader import (
    load_hospital_info,
)
from hospital_service.data.general_info.hospital_general_info import HospitalGeneralInfo
from hospital_service.data.measures.hospital_measures import HospitalMeasure
from hospital_service.data.measures.hospital_measures_loader import load_measures
from functools import lru_cache


class Hospital(BaseModel):
    general_info: HospitalGeneralInfo
    measures: List[HospitalMeasure]


def get_hospitals() -> List[Hospital]:
    hospitals = get_hospitals_as_dictionary().values()
    return [
        Hospital(general_info=hospital["general_info"], measures=hospital["measures"])
        for hospital in hospitals
    ]


def get_hospitals_by_criteria(
    measureId: str, score: int, compare: str
) -> List[Hospital]:
    def contains_measure(hospital: Hospital) -> bool:
        def measure_id_matches(measure: HospitalMeasure) -> bool:
            return not measureId or measure.MeasureID == measureId

        def score_matches(measure: HospitalMeasure) -> bool:
            # TODO compare operator
            return not score or (
                measure.Score.isdigit() and int(measure.Score) >= int(score)
            )

        def measure_id_and_score_matches(measure: HospitalMeasure) -> bool:
            return measure_id_matches(measure) and score_matches(measure)

        filter_criteria = (
            measure_id_and_score_matches if measureId and score else measure_id_matches
        )
        return len(list(filter(filter_criteria, hospital.measures))) > 0

    def contains_score(hospital: Hospital) -> bool:
        return True  # TODO

    def meets_criteria(hospital: Hospital) -> bool:
        return contains_measure(hospital) and contains_score(hospital)

    all_hospitals = get_hospitals()  # TODO database side filtering
    return list(filter(meets_criteria, all_hospitals))


@lru_cache()
def get_hospitals_as_dictionary() -> Dict:
    general_info: List[HospitalGeneralInfo] = load_hospital_info()

    hospitals_dict = {
        info.id: {"general_info": info, "measures": []} for info in general_info
    }

    add_measures_to_dictionary(hospitals_dict)

    return hospitals_dict


def add_measures_to_dictionary(hospitals_dict: Dict) -> None:
    measures: List[HospitalMeasure] = load_measures()
    for measure in measures:
        hospitals_dict[measure.FacilityID]["measures"] += [measure]
