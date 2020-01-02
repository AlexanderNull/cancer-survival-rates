# Initial data analysis notes:
* Very low levels of NaNs for demographics / vital status < 1%
* Very low levels of NaNs for primary site < 1%
* Very low levels of NaNs for disease type < 1%
* Absurdly high levels of NaNs for exposures info (smoking/drinking habits) ~85%

## Suggestions
It's unclear so far whether lack of exposure data was meaningful nulls (ie: patient had no drinking or smoking history) or is just missing data.
Most likely interpretation of NaNs here is of missing data as present exposures objects do have occasional values of "Not Reported" and "None".
Due to missing data here it is suggested to move ahead with building model primarily off of demographics data and omit exposures data for now as its smaller
sample size will draw less significant results and may be skewed towards confirmation bias by collectors and responses may be affected by other biases such
as social desirability bias, and demand characteristics.

Further analysis required if exposures needs to be included to determine whether there's any differences between demographic groups, disease type groups, or primary site groups on exposure data presense and responses.