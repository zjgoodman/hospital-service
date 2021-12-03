from fastapi.testclient import TestClient
from hospital_service.main import app, get_hospital_service
from hospital_service.service import HospitalService

client = TestClient(app)


def test_hello_world():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


class DummyHospitalService(HospitalService):
    def __init__(self, hospitals):
        self.hospitals = hospitals

    def get_hospitals(self):
        return self.hospitals


def test_get_hospitals():
    expectedHospitals = [{"id": "1234", "name": "some hospital"}]
    app.dependency_overrides[get_hospital_service] = lambda: DummyHospitalService(
        expectedHospitals
    )

    response = client.get("/hospitals")
    assert response.status_code == 200
    assert response.json() == expectedHospitals
