import sys
from datetime import datetime
from src.lib.data_models import DataFile
from IPython.display import HTML, display
from tabulate import tabulate

assert len(sys.argv) > 4

file_loc, p_start, p_end, val = tuple(sys.argv[1:5])
prev_start, prev_end = None, None
fmt = '%Y-%m-%d'

def get_date(row, col, fmt):
	return datetime.strptime(file.get(row, col), fmt)

def get_dates(row, fmt, *cols):
	return (get_date(row, col, fmt) for col in cols)

def between(start, end, d):
	return start <= d <= end

ranges = []
with DataFile(file_loc) as file:
	row = next(file.row())
	prev_start, prev_end = get_dates(row, fmt, p_start, p_end)

	for row in file.row():
		start, end = get_dates(row, fmt, p_start, p_end)
		if between(prev_start, prev_end, start) or between(prev_start, prev_end, end):
			ranges.append([
				"(%s) - (%s)" % (start.strftime(fmt), end.strftime(fmt)),
				"(%s) - (%s)" % (prev_start.strftime(fmt), prev_end.strftime(fmt))
			])
		prev_start, prev_end = start, end

display(HTML(tabulate(
	ranges,
	headers=['Date range', 'Overlaps with'],
	tablefmt='html'
)))