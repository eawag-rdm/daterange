# Summary

Evaluates whether a date-time string conforms to
the DateRangeField specification of SOLR 5.4.

See https://cwiki.apache.org/confluence/display/solr/Working+with+Dates

Notes on its interpretation:

+ Points in time, i.e. not truncated or "implicit" ranges    
	have to end with character "Z", indicating UTC.
+ "hh" for hours run from 00 to 23.

This validator checks for valid dates considering leap years.

# Usage

~~~python
from validate_solr_daterange import SolrDaterange

datestr = '[-0324-12-31T00:07:34.123Z TO 2016]' #passes
SolrDaterange.validate(datestr)

datestr = '[-0324-12-31T00:07:34.123Z TO 2016-12-]' #fails
SolrDaterange.validate(datestr)
~~~

# Tests

~~~bash
nosetests
~~~

