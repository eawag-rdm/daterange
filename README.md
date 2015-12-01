~~~python
def solr_datetime_eval(datestr):
    '''
    Evaluates whether a date-time string conforms to
    the DateRangeField specification of SOLR 5.4. Only ranges implicitly
    formulated as truncated dates are considered at the moment.
    https://cwiki.apache.org/confluence/display/solr/Working+with+Dates
    '''
~~~
