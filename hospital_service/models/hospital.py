from pydantic.main import BaseModel
from typing import List, Optional

from hospital_service.models.hospital_general_info import HospitalGeneralInfo
from hospital_service.models.hospital_measures import HospitalMeasure


class Hospital(BaseModel):
    general_info: Optional[HospitalGeneralInfo]
    measures: List[HospitalMeasure]
