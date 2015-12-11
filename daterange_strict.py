import re
from nose.tools import *

class SolrDaterange(object):

    regex_elem = {'year': r'(?P<year>-?(0\d{3}|[1-9]\d{3,}))',
                  'month': r'(?P<month>\d{2})',
                  'day': r'(?P<day>\d{2})',
                  'hour': r'(?P<hour>([01][0-9]|2[0-3]))',
                  'minute': r'(?P<minute>[0-5][0-9])',
                  'second': r'(?P<second>[0-5][0-9](\.\d{1,3})?Z)'
                  }
    
    regex_implicit_range = re.compile(
        '^(' + regex_elem['year'] +
        '(-' + regex_elem['month'] +
        '(-' + regex_elem['day'] +
        '(T' + regex_elem['hour'] +
        '(:' + regex_elem['minute'] +
        '(:' + regex_elem['second'] +
        r')?)?)?)?)?|(?P<wildcard>\*))$'
    )

    regex_explicit_range = re.compile(
        r'^\[(?P<start>[\-TZ:\.\d]{4,}|\*)' +
        r' TO (?P<end>[\-TZ:\.\d]{4,}|\*)\]$'
    )
    
    @staticmethod
    def _solregex(regex):
        return(re.compile('^' + regex + '$'))
    
    @classmethod
    def check_date_element(cls, typ, elemstr):
        '''Checks an element of the DateRange string.
        <typ> = 'second', 'minute', hour', 'day', 'month', or 'year'.
        '''
        reg = cls.regex_elem[typ]
        matchres = re.match(cls._solregex(reg), elemstr)
        if matchres is None:
            raise ValueError("{}: not a valid {}".format(elemstr, typ))
        else:
            return(matchres.groupdict()[typ])

    @classmethod
    def check_implicit_range(cls, rangestr):
        matchres = re.match(cls.regex_implicit_range, rangestr)
        if matchres is None:
            raise ValueError("{}: not a valid DateRange - field"
                             .format(rangestr))
        else:
            return(matchres.groupdict())
    
    @classmethod
    def validate(cls, datestr):
        print("VALIDATE: {}".format(datestr))
        parsed = {}
        try:
            d = re.match(cls.regex_explicit_range, datestr).groupdict()
        except AttributeError:
            print("VALIDATE implicit")
            parsed['implicit'] = cls.check_implicit_range(datestr)
        else:
            print("VALIDATE start - end")
            parsed['start'] = cls.check_implicit_range(d['start'])
            parsed['end'] = cls.check_implicit_range(d['end'])
        return(parsed)

        
class TestSolrDaterange(object):

    fail = {'year': ['986z', '87t65', '876', '-456', '06754', '-06411', '87.9'],
            'month': ['u4', '011', '6', '-1', '123'],
            'day': ['9', '076', '8i', ' 2'],
            'hour': ['3', '8z', '022', '24', '-2'], 
            'minute': ['1', '012', '3i', '.'],
            'second': ['7Z', '60Z', '023Z', '00.Z', '12.8364Z', '12',
                        '12.23']
    }
    pas = {'year': ['2016', '0638', '-0124', '45919', '-72354393'],
           'month': ['02', '10', '12', '00'],
           'day': ['00', '35'],
           'hour': ['00', '15', '23'],
           'minute': ['00', '23', '59'],
           'second': ['00Z', '59Z', '23.3Z', '12.543Z']
    }

    pas_implicit_range = ['2016', '0638-02', '-0124-10-00', '45919-12-35T00',
                          '-72354393-00-35T15:00', '2016-02-00T23:23:00Z',
                          '0638-10-35T23:59:12.543Z']
    fail_implicit_range = ['986z', '0638-u4', '-0124-10-9', '45919-12-35T3',
                          '-72354393-00-35T15:012', '2016-02-00T23:23:7Z',
                          '0638-10-35T23:59:12.23']

    pas_explicit_range = ['[2016 TO 2020]', '[-72354393-01-35T15:00 TO 1000]',
                          '[0638-10-35T23:59:12.543Z TO 45919-12-35T00]',
                          '[* TO 2020]', '[-72354393-01-35T15:00 TO *]']
    fail_explicit_range = ['2016 TO 2020', '[-72354393-01-35T15:00 TO1000]',
                           '[0638-10-35T23:59:12.543Z TO 45919-12-35T00',
                           '2016 T 2020']

    def test_check_date_element(self):
        for typ in self.fail:
            print("FAIL: {}".format(typ))
            for e in self.fail[typ]:
                print(e)
                assert_raises(ValueError,
                              SolrDaterange.check_date_element, typ, e)
        for y in self.pas:
            print("PASS: {}".format(typ))
            for e in self.pas[typ]:
                print(e)
                assert (SolrDaterange.check_date_element(typ, e) == e)

    def test_check_implicit_range(self):
        for t in self.pas_implicit_range:
            print("PASS implicit: {}".format(t))
            gd = SolrDaterange.check_implicit_range(t)
            print("gd = {}".format(gd))
            check = gd['year']
            try:
                check += '-' + gd['month']
                check += '-' + gd['day']
                check += 'T' + gd['hour']
                check += ':' + gd['minute']
                check += ':' + gd['second']
            except TypeError:
                pass
            assert(check == t)
        for t in self.fail_implicit_range:
            print("FAIL implicit: {}".format(t))
            assert_raises(ValueError, SolrDaterange.check_implicit_range, t)

    def test_validate(self):
        for t in self.pas_explicit_range:
            print("PASS validate: {}".format(t))
            gd = SolrDaterange.validate(t)
            print(gd)
        for t in self.fail_explicit_range:
            print("FAIL validate: {}".format(t))
            assert_raises(ValueError, SolrDaterange.validate, t)

        
            

        


    
