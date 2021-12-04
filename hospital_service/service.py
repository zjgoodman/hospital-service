from typing import List
from hospital_service.data.general_info.hospital_general_info_loader import (
    load_hospital_info,
)
from hospital_service.data.general_info.hospital_general_info import HospitalGeneralInfo


class HospitalService:
    def get_hospitals(self) -> List[HospitalGeneralInfo]:
        return load_hospital_info()
