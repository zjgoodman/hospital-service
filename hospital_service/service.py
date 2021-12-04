from typing import List
from pydantic import BaseModel
from hospital_service.data.loader import load_hospital_info
from hospital_service.data.hospital_general_info import HospitalGeneralInfo


class HospitalService:
    def get_hospitals(self) -> List[HospitalGeneralInfo]:
        return load_hospital_info()
