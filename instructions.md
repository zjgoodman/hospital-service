### Project overview

We're interested in creating an ETL pipeline that processes hospital and provider information. Other teams will query
this output to gain actionable insights. Here are some sample queries:

* For hospitals with `Measure ID = 'OP_31' AND Score >= 50` (Percentage of patients who had cataract surgery and had
  improvement in visual function within 90 days following the surgery), what are those hospitals' overall ratings?
* Which state has the highest number of patients who left the emergency department before being seen (`OP_22`)?

Given the above queries, we should design the output data in a way that's readable and can be easily queried
against. We'll be working with the below data. Data dictionaries and datasets are both listed on the webpage. Please
download them to your environment.

1. [Hospital General Information](https://data.cms.gov/provider-data/dataset/xubh-q36u)
1. [Timely and Effective Care - Hospital](https://data.cms.gov/provider-data/dataset/yv7e-xc69)

### Project requirements

The project should contain these pieces:

1. An ETL process that will:
    * read in the data
    * apply transformations (if any)
        * for example, for `OP_22`,
          in [Timely and Effective Care - Hospital](https://data.cms.gov/provider-data/dataset/yv7e-xc69), `Score` is
          the percentage of `Sample` population, you may want to create a new column that represents the actual number
          of patients.
    * handle erroneous data
    * handle schema evolution
    * persist the cleaned output to a storage layer
1. Runnable in any machine

### What we're looking for

* Coding standards and best practices
  * Appropriately unit tested
  * Type annotations
  * Type checked (e.g. mypy)
  * Documentation
* Project organization
* Scalable and maintainable production ready code

### Questions?

1. Feel free to make your own assumptions about things that are not clear. Be sure to document those assumptions.
1. If it's been over 5 hours, feel free to submit it and document what you would do to finish it.
1. If you're able to finish in less than 5 hours, feel free to add extra glitter and sparkles on top of the project
   (maybe dockerize the project).

***
