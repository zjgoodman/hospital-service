For hospitals with Measure ID = 'OP_31' AND Score >= 50 (Percentage of patients who had cataract surgery and had improvement in visual function within 90 days following the surgery), what are those hospitals' overall ratings?

Query
```
POST /hospitals
{
    filterByMeasure: [
        {
            measure
            score: {
                value
                compare
            }
        }
    ]
}
```
Response
```
[
    {
        id
        name
        overallRating
        state
        measures: [
            {
                name
                score
            }
        ]
    }
]
```

Which state has the highest number of patients who left the emergency department before being seen (OP_22)?

Query
```
GET /states/rankByMeasure?measure=OP_22
```
Response
```
{
    measure
    totalPatients
    states [
        {
            state
            rank
            totalPatients
            hospitals [ // extra credit
                {
                    name
                    rank
                    totalPatients
                }
            ]
        }
    ]
}
```

get hospitals that have measure OP_22
group by state
reduce to total number of patients affected
return sorted list