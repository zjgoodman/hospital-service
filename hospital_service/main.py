from typing import Optional
from fastapi import Depends, FastAPI
import hospital_service.service as hospital_service

app = FastAPI()


@app.get("/hello")
def hello_world():
    return {"msg": "Hello World"}


@app.get("/hospitals")
def get_hospitals(
    measureId: Optional[str] = None,
    score: Optional[int] = None,
    compare: str = "eq",
):
    return (
        hospital_service.get_hospitals_by_criteria(measureId, score, compare)
        if measureId or score
        else hospital_service.get_hospitals()
    )
