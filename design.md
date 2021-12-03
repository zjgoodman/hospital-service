For hospitals with Measure ID = 'OP_31' AND Score >= 50 (Percentage of patients who had cataract surgery and had improvement in visual function within 90 days following the surgery), what are those hospitals' overall ratings?

Query
```
POST /hospitals
{
    filterByMeasures: [
        {
            measureId: "op_31",
            score: {
                value: 50
                operator: ge
            },
            plus: { // extra credit
                type: "or"
                criteria: {
                    measureId: "op_22"
                }
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

get hospitals that have measure OP_22
group by state
reduce to total number of patients affected
return sorted list

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