from pydantic import BaseModel
from pydantic.types import OptionalInt


class HospitalMeasure(BaseModel):
    FacilityID: str
    Condition: str
    MeasureID: str
    MeasureName: str
    PatientsAffected: OptionalInt = None
    Score: str
    Sample: str
    Footnote: str
    StartDate: str
    EndDate: str
