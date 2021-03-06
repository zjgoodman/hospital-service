from typing import Dict, List, Optional

from pydantic.types import OptionalInt
from hospital_service.data.hospital_general_info_loader import (
    load_hospital_info,
)
from hospital_service.data.hospital_measures_loader import load_measures
from hospital_service.models.hospital import Hospital
from hospital_service.models.hospital_general_info import HospitalGeneralInfo
from hospital_service.models.hospital_measures import HospitalMeasure
from hospital_service.models.state_rank_by_hospital_measure import (
    StateRankByHospitalMeasure,
)
from hospital_service.models.rank_states_by_hospital_measure import (
    RankStatesByHospitalMeasure,
)
from hospital_service.validation import score_compare_operators
from functools import reduce
from fastapi import HTTPException


def get_hospitals() -> List[Hospital]:
    hospitals = get_hospitals_as_dictionary().values()
    return [
        Hospital(general_info=hospital["general_info"], measures=hospital["measures"])
        for hospital in hospitals
    ]


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
            lambda _: True,
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
    hospitals: List[Hospital] = get_hospitals_by_criteria(measureId=measureId)
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


def get_state_reports(measureId: str) -> List[StateRankByHospitalMeasure]:
    states_to_hospitals = get_hospitals_by_state(measureId)
    return [
        StateRankByHospitalMeasure(
            state=state_to_hospital_mapping["state"],
            total_patients_impacted_by_measure=get_total_patients_impacted_by_measure(
                state_to_hospital_mapping["hospitals"], measureId
            ),
        )
        for state_to_hospital_mapping in states_to_hospitals
    ]


def get_total_patients_in_all_states(state_reports: List[StateRankByHospitalMeasure]):
    return sum(
        filter(
            lambda value: value != None,
            map(
                lambda state_report: state_report.total_patients_impacted_by_measure,
                state_reports,
            ),
        )
    )


def get_hospitals_by_state_ranked_by_measure(measureId) -> RankStatesByHospitalMeasure:
    state_reports: List[StateRankByHospitalMeasure] = get_state_reports(measureId)
    rank_states_by_patients_affected(state_reports)
    total_patients_in_all_states = get_total_patients_in_all_states(state_reports)
    return RankStatesByHospitalMeasure(
        measure=measureId,
        total_patients_impacted_by_measure=total_patients_in_all_states,
        states=state_reports,
    )


def rank_states_by_patients_affected(
    state_reports: List[StateRankByHospitalMeasure],
) -> None:
    patients_affected_in_each_state = get_ranked_patients_affected_in_each_state(
        state_reports
    )
    for state_report in state_reports:
        if (
            state_report.total_patients_impacted_by_measure
            in patients_affected_in_each_state
        ):
            state_rank: int = patients_affected_in_each_state.index(
                state_report.total_patients_impacted_by_measure
            )
            state_report.rank = state_rank


def get_ranked_patients_affected_in_each_state(
    state_reports: List[StateRankByHospitalMeasure],
) -> List[int]:
    patients_affected_in_each_state = list(
        sorted(
            list(
                set(
                    map(
                        lambda state_report: state_report.total_patients_impacted_by_measure,
                        filter(
                            lambda state_report: state_report.total_patients_impacted_by_measure,
                            state_reports,
                        ),
                    )
                )
            )
        )
    )
    patients_affected_in_each_state.reverse()
    return patients_affected_in_each_state


def get_total_patients_impacted_by_measure(
    hospitals: List[Hospital], measure_id: str
) -> OptionalInt:
    all_measures: List[HospitalMeasure] = [
        measure for hospital in hospitals for measure in hospital.measures
    ]
    patients_impacted_for_each_matching_measure = list(
        map(
            lambda measure: measure.PatientsAffected,
            filter(
                lambda measure: measure.MeasureID == measure_id
                and measure.PatientsAffected != None,
                all_measures,
            ),
        )
    )
    return (
        sum(patients_impacted_for_each_matching_measure)
        if patients_impacted_for_each_matching_measure
        else None
    )
