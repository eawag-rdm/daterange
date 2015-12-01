import re

def solr_datetime_eval(datestr):
    '''Evaluates wheter a date-time string conforms to
    the DateRangeField specification of SOLR 5.4. Only ranges implicitly
    formulated as truncated dates are considered at the moment.
    https://cwiki.apache.org/confluence/display/solr/Working+with+Dates
    '''

    dateregex = '^(?P<year>-?\d{4,})(-(?P<month>\d{2})(-(?P<day>\d{2}))?)?$'
    timeregex = '^(?P<hours>\d{2})(:(?P<mins>\d{2})(:(?P<secs>\d{2}(\.\d+)?Z))?)?$'
    
    def split_dt(datestr):
        try:
            dat, tim = datestr.split('T')
        except ValueError:
            dat = datestr.split('T')[0]
            tim = ''
        return((dat, tim))

    def valdate(dat):
        m = re.match(dateregex, dat)
        if not m:
            raise ValueError("{} is not a valid date".format(dat))
        return(m.groupdict())

    def val_month_day(datedict):
        intyear = int(datedict['year'])
        try:
            intmonth = int(datedict['month'])
            # print("{} -> {}".format(datedict['month'], intmonth))
        except TypeError:
            intmonth = None
        try:
            intday = int(datedict['day'])
        except TypeError:
            intday = None
        if ((datedict['year'].startswith('0') and len(datedict['year'])) > 4 or
            (datedict['year'].startswith('-0') and len(datedict['year'])) > 5):
            raise ValueError("{} is not a valid year.".format(datedict['year']))
        noleapyear = intyear % 4 != 0 or (intyear % 100 == 0
                                          and intyear % 400 != 0)
        maxdays = [31, 28 if noleapyear else 29, 31, 30, 31, 30, 31, 31, 30, 31,
                   30, 31]
        if not (intmonth is None or 1 <= intmonth <= 12):
            raise ValueError("{} is not a valid month.".format(datedict['month']))
        if not (intday is None or 1 <= intday <= maxdays[intmonth - 1]):
            raise ValueError("{} is not a valid day.".format(datedict['day']))

    def valtime(tim):
        m = re.match(timeregex, tim)
        if not m:
            raise ValueError("{} is not a valid time.".format(tim))
        return(m.groupdict())
    
    def valhour_min_sec(timedict):
        inthour = int(timedict["hours"])
        try:
            intmins = int(timedict["mins"])
        except TypeError:
            intmins = None;
        secs = timedict["secs"]
        if secs is None:
            intsecs = None
        else:
            intsecs = float(timedict["secs"][0:-1])
        if inthour == 24 and ((intmins > 0 and not intmins is None) or
                              (intsecs > 0 and not intsecs is None)):
            raise ValueError("{} is not a valid hour".format(timedict["hours"]))
        if inthour >= 25:
            raise ValueError("{} is not a valid hour".format(timedict["hours"]))
        if intmins is not None and not (0 <= intmins <= 59):
            raise ValueError("{} are not valid minutes".format(timedict["mins"]))
        if intsecs is not None and not (0 <= intsecs < 60.):
            raise ValueError("{} are not valid seconds".format(timedict["secs"]))
        return()
 


    dat, tim = split_dt(datestr)
    val_month_day(valdate(dat))
    if tim != '':
        valhour_min_sec(valtime(tim))


############# Testing

timetest = ['', '0', '02:', ':04', '25', '02:2', '03:60',
    '03:59:','03:59:3Z', '04:48:967Z', '07:32:59.', '15:44:49.98',
    '01:00', '00','15:44:49.98Z', '24:07:00Z', '24:00:00.005Z',
    '04', '05:12', '17:54:12Z', '24', '24:00:00Z', '23:12:18.986754Z']
timetest = ['2015-11-30T' + x for x in timetest]

for t in timetest:
    try:
        solr_datetime_eval(t)
        print("{} -> OK".format(t))
    except ValueError as e:
        print("{} -> {}".format(t, e))


datetest = ['2014-02-29', '2300-02-29',  '01232-01-31',
            '-08765-12-31', '2016-32-03', '-987658-00-07', '87654-08-00',
            '2400-02-29', '2014-02-28', '0023', '0435-12', '-0987-05-31']
datetest = [x + 'T23:59:58.9997Z' for x in datetest]

for d in datetest:
    try:
        datedict = solr_datetime_eval(d)
        print("{} -> OK".format(d))
    except ValueError as e:
        print("{} -> {}".format(d, e.message))

