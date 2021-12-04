from pydantic import BaseModel


class HospitalService:
    def get_hospitals(self):
        return []


class HospitalGeneralInfo(BaseModel):
    id: str
    name: str
    streetAddress: str
    city: str
    state: str
    zip: str
    county: str
    phone: str
    type: str
    ownership: str
    offersEmergencyServices: str
    meetsEHRCriteria: str
    overallRating: str
    overallRatingNote: str
    mortGroupMeasureCount: str
    countOfFacilityMortMeasures: str
    countOfMortMeasuresBetter: str
    CountofMORTMeasuresNoDifferent: str
    CountofMORTMeasuresWorse: str
    MORTGroupFootnote: str
    SafetyGroupMeasureCount: str
    CountofFacilitySafetyMeasures: str
    CountofSafetyMeasuresBetter: str
    CountofSafetyMeasuresNoDifferent: str
    CountofSafetyMeasuresWorse: str
    SafetyGroupFootnote: str
    READMGroupMeasureCount: str
    CountofFacilityREADMMeasures: str
    CountofREADMMeasuresBetter: str
    CountofREADMMeasuresNoDifferent: str
    CountofREADMMeasuresWorse: str
    READMGroupFootnote: str
    PtExpGroupMeasureCount: str
    CountofFacilityPtExpMeasures: str
    PtExpGroupFootnote: str
    TEGroupMeasureCount: str
    CountofFacilityTEMeasures: str
    TEGroupFootnote: str
