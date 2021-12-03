from fastapi import Depends, FastAPI
from hospital_service.service import HospitalService

app = FastAPI()


@app.get("/hello")
def hello_world():
    return {"msg": "Hello World"}


def get_hospital_service():
    return HospitalService()


@app.get("/hospitals")
def get_hospitals(hospital_service: HospitalService = Depends(get_hospital_service)):
    return hospital_service.get_hospitals()
