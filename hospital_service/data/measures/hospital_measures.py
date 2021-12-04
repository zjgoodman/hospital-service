from pydantic import BaseModel


class HospitalMeasure(BaseModel):
    FacilityID: str
    Condition: str
    MeasureID: str
    MeasureName: str
    Score: str
    Sample: str
    Footnote: str
    StartDate: str
    EndDate: str
