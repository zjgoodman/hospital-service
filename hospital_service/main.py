from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException
import hospital_service.service as hospital_service
from hospital_service.validation import validate_score_compare_operator

app = FastAPI()


@app.get("/hospitals")
def get_hospitals(
    measureId: Optional[str] = None,
    score: Optional[int] = None,
    score_compare_operator: Optional[str] = None,
):
    validate_score_compare_operator(score, score_compare_operator)
    return hospital_service.get_hospitals_by_criteria(
        measureId, score, score_compare_operator
    )


@app.get("/hospitals/getByState")
def get_hospitals_by_state(measureId: Optional[str] = None):
    return hospital_service.get_hospitals_by_state(measureId)


@app.get("/hospitals/getByState/rankByMeasure")
def get_hospitals_by_state_ranked_by_measure(measureId: str):
    return hospital_service.get_hospitals_by_state_ranked_by_measure(measureId)
