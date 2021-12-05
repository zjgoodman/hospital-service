
# Building the project
- build: to build the project, use `poetry install`
- test: to test the project, use `poetry run pytest`
## Running the app
- [from source](#running-the-app-from-source)
- [docker]

### Running the app via docker
```
docker run --rm -d -p 8000:8000 --name hospital-service zjgoodman/hospital-service
```
### Running the app from source
To run the app from source, use `poetry run uvicorn hospital_service.main:app --reload`. Make sure to install dependencies first via `poetry install`.
# Query options
- Query for hospitals
- Query for states

API docs available at [http://localhost:8000/docs](http://localhost:8000/docs) **while** [running the app](#running-the-app)
## Sample queries

### Query

For hospitals with `Measure ID = 'OP_31' AND Score >= 50`
```
http://localhost:8000/hospitals?measureId=OP_31&score=50&score_compare_operator=ge
```
### Response (truncated)
```json
[
    {
        "general_info": {
            "id": "050169",
            "name": "PIH HEALTH HOSPITAL-WHITTIER",
            "streetAddress": "12401 WASHINGTON BLVD",
            "city": "WHITTIER",
            "state": "CA",
            "zip": "90602",
            "county": "Los Angeles",
            "phone": "(526) 698-0811",
            "type": "Acute Care Hospitals",
            "ownership": "Voluntary non-profit - Private",
            "offersEmergencyServices": "Yes",
            "meetsEHRCriteria": "Y",
            "overallRating": "5",
            "overallRatingNote": "",
            "mortGroupMeasureCount": "7",
            "countOfFacilityMortMeasures": "7",
            "countOfMortMeasuresBetter": "1",
            "CountofMORTMeasuresNoDifferent": "6",
            "CountofMORTMeasuresWorse": "0",
            "MORTGroupFootnote": "",
            "SafetyGroupMeasureCount": "8",
            "CountofFacilitySafetyMeasures": "8",
            "CountofSafetyMeasuresBetter": "1",
            "CountofSafetyMeasuresNoDifferent": "7",
            "CountofSafetyMeasuresWorse": "0",
            "SafetyGroupFootnote": "",
            "READMGroupMeasureCount": "11",
            "CountofFacilityREADMMeasures": "11",
            "CountofREADMMeasuresBetter": "0",
            "CountofREADMMeasuresNoDifferent": "9",
            "CountofREADMMeasuresWorse": "2",
            "READMGroupFootnote": "",
            "PtExpGroupMeasureCount": "8",
            "CountofFacilityPtExpMeasures": "8",
            "PtExpGroupFootnote": "",
            "TEGroupMeasureCount": "14",
            "CountofFacilityTEMeasures": "11",
            "TEGroupFootnote": ""
        },
        "measures": [
            {
                "FacilityID": "050169",
                "Condition": "Emergency Department",
                "MeasureID": "EDV",
                "MeasureName": "Emergency department volume",
                "Score": "very high",
                "Sample": "",
                "Footnote": "",
                "StartDate": "01/01/2019",
                "EndDate": "12/31/2019"
            },
            {
                "FacilityID": "050169",
                "Condition": "Preventive Care",
                "MeasureID": "IMM_3",
                "MeasureName": "Healthcare workers given influenza vaccination",
                "Score": "88",
                "Sample": "5499",
                "Footnote": "",
                "StartDate": "10/01/2020",
                "EndDate": "03/31/2021"
            }
        ]
    }
]
```