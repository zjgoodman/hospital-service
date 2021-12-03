from hospital_service.data.loader import load_csv, parse_hospital_info_from_csv


def test_load_csv():
    csvData = load_csv("tests/data/test-hospital-info.csv")
    actual_hospital_info_list = parse_hospital_info_from_csv(csvData)
    assert len(actual_hospital_info_list) == 1
    assert actual_hospital_info_list[0].id == "10001"
