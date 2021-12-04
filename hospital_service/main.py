from fastapi import Depends, FastAPI
import hospital_service.service as hospital_service

app = FastAPI()


@app.get("/hello")
def hello_world():
    return {"msg": "Hello World"}


@app.get("/hospitals")
def get_hospitals():
    return hospital_service.get_hospitals()
