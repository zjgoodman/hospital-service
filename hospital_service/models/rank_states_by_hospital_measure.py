from typing import List, Optional
from pydantic.main import BaseModel
from hospital_service.models.state_rank_by_hospital_measure import (
    StateRankByHospitalMeasure,
)


class RankStatesByHospitalMeasure(BaseModel):
    measure: str
    total_patients_impacted_by_measure: Optional[int]
    states: List[StateRankByHospitalMeasure]
