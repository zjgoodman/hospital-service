# Hospital Service
The goal of this project is to provide an api that supports queries on hospital data. See [instructions.md](instructions.md) for additional background.

- [Hospital Service](#hospital-service)
- [Running the app](#running-the-app)
  - [Running the app via docker](#running-the-app-via-docker)
  - [Running the app from source](#running-the-app-from-source)
    - [Building the project](#building-the-project)
- [Using the app](#using-the-app)
  - [Swagger kinda sucks for large payloads](#swagger-kinda-sucks-for-large-payloads)
  - [Sample queries](#sample-queries)
    - [Querying for measures and scores of hospitals](#querying-for-measures-and-scores-of-hospitals)
    - [Querying for state rankings by measure](#querying-for-state-rankings-by-measure)
    - [Querying for hospitals grouped by state](#querying-for-hospitals-grouped-by-state)
- [Retrospective](#retrospective)

# Running the app
There are two ways to run the app:
- [from source](#running-the-app-from-source)
- [docker](#running-the-app-via-docker)

For ease of use, I recommend running from docker. Installing from source requires development dependencies to be installed on your machine.

## Running the app via docker
The docker image for this app is hosted on [docker hub](https://hub.docker.com/r/zjgoodman/hospital-service). You can download and run the image with the following command:
```
docker run --rm -d -p 8000:8000 --name hospital-service zjgoodman/hospital-service
```

Once the app starts, see [#using-the-app](#using-the-app).
## Running the app from source
To run the app from source, first [build the project](#building-the-project). Then run `poetry run uvicorn hospital_service.main:app --reload`

### Building the project
- build: to build the project, use `poetry install`
- test: to test the project, use `poetry run pytest`
# Using the app
Once you have [started the app](#running-the-app) you can interact with it. Swagger API documentation is provided by the app and is available at [http://localhost:8000/docs](http://localhost:8000/docs) **while** [running the app](#running-the-app).

## Swagger kinda sucks for large payloads
**NOTE** that the swagger docs don't handle large payloads well. So if you try to query for a large amount of data (load all hospitals) swagger won't be able to handle it and it'll just appear to be loading forever. I recommend invoking the api directly through your browser, `postman` or via `curl` if you are making a large query.

## Sample queries
The project [instructions](instructions.md) ask for support for two different types of queries:
1. [#querying-for-measures-and-scores-of-hospitals](#querying-for-measures-and-scores-of-hospitals)
2. Which state has the highest number of patients who left the emergency department before being seen (OP_22)?

### Querying for measures and scores of hospitals
> For hospitals with Measure ID = 'OP_31' AND Score >= 50, what are those hospitals' overall ratings?

For the above query we're interested `Measure ID = 'OP_31' AND Score >= 50`. We can acheive this by using the available query params `measureId=OP_31`, `score=50` and `score_compare_operator=ge` of the `/hospitals` api.

Example query:
```
http://localhost:8000/hospitals?measureId=OP_31&score=50&score_compare_operator=ge
```
Response (truncated):
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

Hospital overall ratings can be obtained via `hospital -> hospital.general_info.overallRating`.

The app supports several score compare operators. For example we can search for scores < 50 using `lt` or >50 with `gt`.

Note that if you provide a value for `score` you MUST provide a score compare operator so that the app knows how to compare the data to the score you provided. If you fail to provide an operator or if you provide an invalid operator you will receive an error like this:
```json
{
  "detail": "400 - Invalid 'score_compare_operator' param. Supported values are: ['eq', 'le', 'ge', 'lt', 'gt', 'ne']"
}
```

Also note that the app supports querying by measure, score and measure+score.

Example 1: if you just want to see all the `OP_22` hospitals, use `http://localhost:8000/hospitals?measureId=OP_22`.

Example 2: if you just want to see hospitals that have scored >=50 in any measure, use `http://localhost:8000/hospitals?score=50&score_compare_operator=ge`.

### Querying for state rankings by measure
> Which state has the highest number of patients who left the emergency department before being seen (OP_22)?

To satisfy this request, we can use the `measureId` query param on the `/hospitals/getByState/rankByMeasure` api. 

Example query:
```
http://localhost:8000/hospitals/getByState/rankByMeasure?measureId=OP_22
```
Response (truncated):
```json
{
  "measure": "OP_22",
  "total_patients_impacted_by_measure": 1891626,
  "states": [
    {
      "state": "AL",
      "rank": 21,
      "total_patients_impacted_by_measure": 32038
    },
    {
      "state": "AK",
      "rank": 46,
      "total_patients_impacted_by_measure": 3376
    },
    {
      "state": "AZ",
      "rank": 13,
      "total_patients_impacted_by_measure": 52963
    },
    {
      "state": "AR",
      "rank": 30,
      "total_patients_impacted_by_measure": 18082
    },
    {
      "state": "CA",
      "rank": 0,
      "total_patients_impacted_by_measure": 146222
    },
    {
      "state": "CO",
      "rank": 31,
      "total_patients_impacted_by_measure": 16948
    },
    {
      "state": "CT",
      "rank": 32,
      "total_patients_impacted_by_measure": 16609
    },
    {
      "state": "DE",
      "rank": 36,
      "total_patients_impacted_by_measure": 10489
    },
    {
      "state": "DC",
      "rank": 39,
      "total_patients_impacted_by_measure": 8069
    },
    {
      "state": "FL",
      "rank": 4,
      "total_patients_impacted_by_measure": 91870
    },
    {
      "state": "GA",
      "rank": 7,
      "total_patients_impacted_by_measure": 65276
    },
    {
      "state": "HI",
      "rank": 44,
      "total_patients_impacted_by_measure": 3767
    }
  ]
}
```

The response includes a ranking of all the states. The rankings are 0 indexed, with 0 being the highest ranking state. The grand total of affected patients is also included in the response and is broken up by state.

Note that at this time only `OP_22` is a supported ranking measure. However the api was designed with flexibility in mind so adding additional functionality will be a natural extension.

### Querying for hospitals grouped by state
Note that the app also supports returning hospitals grouped by state.

Example query:
```
http://localhost:8000/hospitals/getByState
```
Response (truncated):
```json
[
    {
        "state": "AL",
        "hospitals": [
            {
                "general_info": {
                    "id": "010001",
                    "name": "SOUTHEAST HEALTH MEDICAL CENTER",
                    "streetAddress": "1108 ROSS CLARK CIRCLE",
                    "city": "DOTHAN",
                    "state": "AL",
                    "zip": "36301",
                    "county": "Houston",
                    "phone": "(334) 793-8701",
                    "type": "Acute Care Hospitals",
                    "ownership": "Government - Hospital District or Authority",
                    "offersEmergencyServices": "Yes",
                    "meetsEHRCriteria": "",
                    "overallRating": "3",
                    "overallRatingNote": "",
                    "mortGroupMeasureCount": "7",
                    "countOfFacilityMortMeasures": "7",
                    "countOfMortMeasuresBetter": "0",
                    "CountofMORTMeasuresNoDifferent": "6",
                    "CountofMORTMeasuresWorse": "1",
                    "MORTGroupFootnote": "",
                    "SafetyGroupMeasureCount": "8",
                    "CountofFacilitySafetyMeasures": "8",
                    "CountofSafetyMeasuresBetter": "2",
                    "CountofSafetyMeasuresNoDifferent": "6",
                    "CountofSafetyMeasuresWorse": "0",
                    "SafetyGroupFootnote": "",
                    "READMGroupMeasureCount": "11",
                    "CountofFacilityREADMMeasures": "11",
                    "CountofREADMMeasuresBetter": "1",
                    "CountofREADMMeasuresNoDifferent": "9",
                    "CountofREADMMeasuresWorse": "1",
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
                        "FacilityID": "010001",
                        "Condition": "Emergency Department",
                        "MeasureID": "EDV",
                        "MeasureName": "Emergency department volume",
                        "PatientsAffected": null,
                        "Score": "high",
                        "Sample": "",
                        "Footnote": "",
                        "StartDate": "01/01/2019",
                        "EndDate": "12/31/2019"
                    }
                ]
            }
        ]
    },
    {
        "state": "AK",
        "hospitals": [
            {
                "general_info": {
                    "id": "02013F",
                    "name": "673rd Medical Group (Joint Base Elmendorf-Richardson)",
                    "streetAddress": "673 MDG 5955 Zeamer Ave",
                    "city": "JBER",
                    "state": "AK",
                    "zip": "99506",
                    "county": "Anchorage",
                    "phone": "(907) 384-1110",
                    "type": "Acute Care - Department of Defense",
                    "ownership": "Department of Defense",
                    "offersEmergencyServices": "Yes",
                    "meetsEHRCriteria": "",
                    "overallRating": "Not Available",
                    "overallRatingNote": "22.0",
                    "mortGroupMeasureCount": "Not Available",
                    "countOfFacilityMortMeasures": "Not Available",
                    "countOfMortMeasuresBetter": "Not Available",
                    "CountofMORTMeasuresNoDifferent": "Not Available",
                    "CountofMORTMeasuresWorse": "Not Available",
                    "MORTGroupFootnote": "22.0",
                    "SafetyGroupMeasureCount": "Not Available",
                    "CountofFacilitySafetyMeasures": "Not Available",
                    "CountofSafetyMeasuresBetter": "Not Available",
                    "CountofSafetyMeasuresNoDifferent": "Not Available",
                    "CountofSafetyMeasuresWorse": "Not Available",
                    "SafetyGroupFootnote": "22.0",
                    "READMGroupMeasureCount": "Not Available",
                    "CountofFacilityREADMMeasures": "Not Available",
                    "CountofREADMMeasuresBetter": "Not Available",
                    "CountofREADMMeasuresNoDifferent": "Not Available",
                    "CountofREADMMeasuresWorse": "Not Available",
                    "READMGroupFootnote": "22.0",
                    "PtExpGroupMeasureCount": "Not Available",
                    "CountofFacilityPtExpMeasures": "Not Available",
                    "PtExpGroupFootnote": "22.0",
                    "TEGroupMeasureCount": "Not Available",
                    "CountofFacilityTEMeasures": "Not Available",
                    "TEGroupFootnote": "22.0"
                },
                "measures": [
                    {
                        "FacilityID": "02013F",
                        "Condition": "Emergency Department",
                        "MeasureID": "EDV",
                        "MeasureName": "Emergency department volume",
                        "PatientsAffected": null,
                        "Score": "medium",
                        "Sample": "",
                        "Footnote": "",
                        "StartDate": "01/01/2019",
                        "EndDate": "12/31/2019"
                    }
                ]
            }
        ]
    }
]
```

# Retrospective
TODO