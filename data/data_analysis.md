# Initial data analysis notes:
* Very low levels of NaNs for demographics / vital status < 1%
* Very low levels of NaNs for primary site < 1%
* Very low levels of NaNs for disease type < 1%
* Absurdly high levels of NaNs for exposures info (smoking/drinking habits) ~85%
* demographic.age_at_index appears to have a number of incorrect values with age of 0
* demographic.race is heavily skewed towards white, will not be able to generate good model for american indian or hawaiian native values
* vital_status known for only 23% of records, still results in 10s of thousands of results
* diagnoses & exposures series are all only max length of 1, can flatten
* survival rate calculated for patients released based off of diagnoses.days_to_last_follow_up column
* survival rate calculated for deceased patients based off of demographic.days_to_death
* primary_site includes 68 unique values, need to simplify with better bins

## Suggestions
It's unclear so far whether lack of exposure data was meaningful nulls (ie: patient had no drinking or smoking history) or is just missing data.
Most likely interpretation of NaNs here is of missing data as present exposures objects do have occasional values of "Not Reported" and "None".
Due to missing data here it is suggested to move ahead with building model primarily off of demographics data and omit exposures data for now as its smaller
sample size will draw less significant results and may be skewed towards confirmation bias by collectors and responses may be affected by other biases such
as social desirability bias, and demand characteristics.

Further analysis required if exposures needs to be included to determine whether there's any differences between demographic groups, disease type groups, or primary site groups on exposure data presense and responses.