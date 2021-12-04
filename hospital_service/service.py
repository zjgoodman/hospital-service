from typing import Dict, List

from pydantic.main import BaseModel
from hospital_service.data.general_info.hospital_general_info_loader import (
    load_hospital_info,
)
from hospital_service.data.general_info.hospital_general_info import HospitalGeneralInfo
from hospital_service.data.measures.hospital_measures import HospitalMeasure
from hospital_service.data.measures.hospital_measures_loader import load_measures


class Hospital(BaseModel):
    general_info: HospitalGeneralInfo
    measures: List[HospitalMeasure]


def get_hospitals() -> Dict:
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
