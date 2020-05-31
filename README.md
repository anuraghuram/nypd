# NYPD interactive crimemap

Using history crime data from NYC Open Data, I create an interactive crime map of NYC (2019). 

Primary features of the map:
- Crime density by offense type and crime premises, down to zipcode level
- Annual aggregates by offense type x borough region


Data sources:

[New York City Police Department complaint data](https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Historic/qgea-i56i)

[Department of City Planning GIS data for borough boundaries](https://data.cityofnewyork.us/City-Government/Borough-Boundaries/tqmj-j8zm)


Preview of map:
![](/crimemap.png)


Design decisions/evaluation:
- This map only charts offense types where there are at least 200 cases in a given year. These are considered 'commonly ocurring' crimes.
- Severity of crimes (misdemeanor, violation felony) are not included in this map, as the differences between boroughs were minimal (~0.5-1pp difference across the three levels)
- The raw data leveraged for this visualisation does not provide insight into repeat offenders, nor does it provide visibility at household level i.e. number of complaints filed by an individual/household. 
- Crime types are also not mutually exclusive. For instance, in this analysis, I classify an offense like 'grand larceny involving a motor vehicle' under 'THEFT,' however, it does also constitute as a 'TRANSPORT' related crime.
