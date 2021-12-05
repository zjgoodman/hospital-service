from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
import hospital_service.service as hospital_service

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


acceptable_score_compare_operators = [
    str(key) for key in hospital_service.score_compare_operators.keys()
]


def validate_score_compare_operator(
    score: Optional[int], score_compare_operator: Optional[str]
):
    if (score and not score_compare_operator) or (
        score_compare_operator
        and score_compare_operator not in acceptable_score_compare_operators
    ):
        raise HTTPException(
            status_code=400,
            detail="400 - Invalid 'score_compare_operator' param. Supported values are: "
            + str(acceptable_score_compare_operators),
        )
