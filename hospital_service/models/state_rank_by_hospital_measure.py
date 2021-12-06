from typing import List, Optional
from pydantic.main import BaseModel


class StateRankByHospitalMeasure(BaseModel):
    state: str
    rank: Optional[int]
    total_patients_impacted_by_measure: Optional[int]
