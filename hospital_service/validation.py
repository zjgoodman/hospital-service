import operator
from typing import Optional
from fastapi import HTTPException

score_compare_operators = {
    "eq": operator.eq,
    "le": operator.le,
    "ge": operator.ge,
    "lt": operator.lt,
    "gt": operator.gt,
    "ne": operator.ne,
}

acceptable_score_compare_operators = [
    str(key) for key in score_compare_operators.keys()
]


def validate_score_compare_operator(
    score: Optional[int], score_compare_operator: Optional[str]
) -> None:
    if (score != None and not score_compare_operator) or (
        score_compare_operator
        and score_compare_operator not in acceptable_score_compare_operators
    ):
        raise HTTPException(
            status_code=400,
            detail="400 - Invalid 'score_compare_operator' param. Supported values are: "
            + str(acceptable_score_compare_operators),
        )
