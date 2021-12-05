from typing import Dict, List, Optional

from pydantic.main import BaseModel
from hospital_service.data.general_info.hospital_general_info_loader import (
    load_hospital_info,
)
from hospital_service.data.general_info.hospital_general_info import HospitalGeneralInfo
from hospital_service.data.measures.hospital_measures import HospitalMeasure
from hospital_service.data.measures.hospital_measures_loader import load_measures
from functools import reduce
import operator
from fastapi import HTTPException


class Hospital(BaseModel):
    general_info: Optional[HospitalGeneralInfo]
    measures: List[HospitalMeasure]


class StateRankByHospitalMeasure(BaseModel):
    state: str
    rank: Optional[int]
    total_patients_impacted_by_measure: Optional[int]
    hospitals: List[Hospital]


class RankStatesByHospitalMeasure(BaseModel):
    measure: str
    total_patients_impacted_by_measure: Optional[int]
    states: List[StateRankByHospitalMeasure]


def get_hospitals() -> List[Hospital]:
    hospitals = get_hospitals_as_dictionary().values()
    return [
        Hospital(general_info=hospital["general_info"], measures=hospital["measures"])
        for hospital in hospitals
    ]


score_compare_operators = {
    "eq": operator.eq,
    "le": operator.le,
    "ge": operator.ge,
    "lt": operator.lt,
    "gt": operator.gt,
    "ne": operator.ne,
}


def get_hospitals_by_criteria(
    measureId: Optional[str] = None,
    score: Optional[int] = None,
    score_compare_operator: str = "eq",
) -> List[Hospital]:
    filter_criteria = get_filter_criteria(measureId, score, score_compare_operator)
    all_hospitals = get_hospitals()  # TODO database side filtering
    return list(filter(filter_criteria, all_hospitals))


def get_filter_criteria(
    measureId: Optional[str],
    score: Optional[int],
    score_compare_operator: str,
):
    def hospital_matches_criteria(hospital: Hospital) -> bool:
        def measure_id_matches(measure: HospitalMeasure) -> bool:
            return measure.MeasureID == measureId

        def score_matches(measure: HospitalMeasure) -> bool:
            score_compare_operator_function = score_compare_operators[
                score_compare_operator
            ]
            if not score_compare_operator_function:
                raise HTTPException(status_code=404, detail="Unsupported operator")
            return measure.Score.isdigit() and score_compare_operator_function(
                int(measure.Score), int(score)
            )

        filter_predicates = []
        if measureId:
            filter_predicates += [measure_id_matches]
        if score:
            filter_predicates += [score_matches]

        filter_predicate = reduce(
            lambda previousPredicate, thisPredicate: lambda measure: previousPredicate(
                measure
            )
            and thisPredicate(measure),
            filter_predicates,
            lambda measure: True,
        )
        return len(list(filter(filter_predicate, hospital.measures))) > 0

    return hospital_matches_criteria


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
        if measure.FacilityID in hospitals_dict:
            hospitals_dict[measure.FacilityID]["measures"] += [measure]
        else:
            hospitals_dict[measure.FacilityID] = {
                "measures": [measure],
                "general_info": None,
            }


def get_hospitals_by_state(measureId: Optional[str] = None):
    # hospitals: List[Hospital] = get_hospitals_by_criteria(measureId=measureId)
    hospitals: List[Hospital] = get_hospitals()
    states_to_hospitals = {}
    for hospital in filter(
        lambda hospital: hospital.general_info and hospital.general_info.state,
        hospitals,
    ):
        state = hospital.general_info.state
        if not state in states_to_hospitals:
            states_to_hospitals[state] = []
        states_to_hospitals[state] += [hospital]
        # should use generator for better performance
    return [
        {"state": key, "hospitals": value} for key, value in states_to_hospitals.items()
    ]


def get_hospitals_by_state_ranked_by_measure(measureId) -> RankStatesByHospitalMeasure:
    states_to_hospitals = get_hospitals_by_state(measureId)
    return RankStatesByHospitalMeasure(
        measure=measureId,
        total_patients_impacted_by_measure=None,
        states=[
            StateRankByHospitalMeasure(
                state=entry["state"],
                rank=None,
                total_patients_impacted_by_measure=None,
                hospitals=entry["hospitals"],
            )
            for entry in states_to_hospitals
        ],
    )
