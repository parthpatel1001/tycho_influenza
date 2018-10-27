import sys
import pandas
from datetime import datetime
import json

# from lib import get_dates, between
# assert len(sys.argv) > 1

# file_loc = sys.argv[1]

def between(s, e, d):
    return s <= d <= e


def is_row_between(prev, cur):
    """ 
        returns if the date range of r1 
        has any overlap 
        with the date range r2 
    """
    (_, r1), (_, r2) = prev, cur
    return between(
        r1.PeriodStartDate, 
        r1.PeriodEndDate,
        r2.PeriodStartDate
    ) or between(
        r1.PeriodStartDate, 
        r1.PeriodEndDate,
        r2.PeriodEndDate
    )

def combine_rows(prev, cur, df): #, r2_i, df
    """
        combines the two rows into r2, drops r_1
            date range is smallest date range that includes r1 & r2
            count is sum(counts) (the worst caste)
                this could be avg, min, max etc.
        returns the index of the previous row
    """
    (r1_i, r1), (r2_i, r2) = prev, cur
    dates = (r1.PeriodStartDate, r1.PeriodEndDate, r2.PeriodStartDate, r2.PeriodEndDate)
    counts = (r1.CountValue, r2.CountValue)
    df.at[r2_i, 'PeriodStartDate'] = min(*dates)
    df.at[r2_i, 'PeriodEndDate'] = max(*dates)
    df.at[r2_i, 'CountValue'] = sum(counts)
    return r1_i

def iter_with_prev(df):
    """ 
        return an iterator that gives back a tuple on next
        ((i, previous_row), (i+1, previous_row))
        first value is ((0, df[0]), (1, df[1]))
    """
    try:
        rows = df.iterrows()
        prev, curr = next(rows), next(rows)
        yield prev, curr
        prev = curr
        for row in rows:
            yield prev, row
            prev = row
    except StopIteration: # could yield back ((1, df[1]), None) ?
        pass

file_loc = 'data/influenza/US/US.6142004.csv'
count = 0
fmt = '%Y-%m-%d'
dateparse = lambda x: pandas.datetime.strptime(x, fmt)
df = pandas.read_csv(file_loc, low_memory=False, parse_dates=['PeriodStartDate', 'PeriodEndDate'], date_parser=dateparse)

cities = df.CityName.dropna().unique()



# for city in cities:
# for prev, curr in iter_with_prev(df.loc[df.CityName == city].sort_values(by=['PeriodStartDate'])):
drop_rows = []
for prev, curr in iter_with_prev(df.loc[df.CityName == 'PHILADELPHIA'].sort_values(by=['PeriodStartDate'])):
    if is_row_between(prev, curr):
        print('combining', prev, curr)
        drop_rows.append(combine_rows(prev, curr, df))
df.drop(drop_rows)
mask = (df.CityName == 'PHILADELPHIA') &(df.PeriodStartDate >= '1923-11-01') &(df.PeriodStartDate <= '1923-11-30')
df.loc[mask].sort_values(by=['PeriodStartDate', 'Fatalities'])
        # print(c_row)
# df.drop(drop_indexes)
# df.to_csv(file_loc + '-cleaned', date_format=fmt, mode='w', header=df.keys(), index=False)
