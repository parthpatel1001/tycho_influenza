def between(s, e, d):
    return s <= d <= e


def is_row_between(prev, cur, match_on):
    """ 
        returns if the date range of prev 
        has any overlap 
        with the date range cur
        and if they have matching match_on values
    """
    (_, r1), (_, r2) = prev, cur
    d1 = (r1.PeriodStartDate, r1.PeriodEndDate, r2.PeriodStartDate)
    d2 = (r1.PeriodStartDate, r1.PeriodEndDate, r2.PeriodEndDate)
    return all(r1[m] == r2[m] for m in match_on) and (between(*d1) or between(*d2))


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


def overlaps(df, match_on, sort_by):
    """
        yields the previous and current row
        given rows to match on, sort by and a data frame
    """
    for prev, curr in iter_with_prev(df.sort_values(by=match_on + sort_by)):
        if is_row_between(prev, curr, match_on):
            yield prev, curr