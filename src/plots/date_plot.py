import matplotlib.pyplot as plt
from matplotlib.dates import strpdate2num
import sys
from src.lib.data_models import DataFile
import numpy as np

# %matplotlib inline

assert len(sys.argv) > 3
file_loc, x_column, y_columns = sys.argv[1], sys.argv[2], sys.argv[3]

# convert the requested y_column(s) provided as string header names to indexes
# TODO assumes strings are "quoted", that could be smarter
headers = open(file_loc).readline().rstrip().replace('"','').split(',')
x_col_index = headers.index(x_column)
y_col_indexes = [headers.index(y) for y in y_columns.rstrip().replace('"','').split(',')]
assert x_col_index != -1
assert all(y_i != -1 for y_i in y_col_indexes)

def convert_date(date_bytes):
    return strpdate2num('"%Y-%m-%d"')(date_bytes.decode('ascii'))

def parse_num(b):
	return float(b.decode('ascii').replace('"',''))

# create list of columns to pluck from the dataset
usecols = [x_col_index] + y_col_indexes

# build converters dict
# TODO assumes all y values are floats, that could be smarter
converters = {
	**{x_col_index: convert_date}, 
	**{y:parse_num for y in y_col_indexes}
}


# load the dataset
data = np.loadtxt(
	file_loc,
	delimiter=',',
	skiprows=1,
	unpack=True,
	usecols=usecols,
	converters=converters
)

plt.figure(figsize=(10,10))
# add all of the requested y column plots
x, columns = data[0], data[1:]
for i in range(0, len(y_col_indexes)):
	plt.plot_date(x, columns[i])

# plt.plot_date(x,y_1, xdate=True)
# plt.plot_date(x,y_2, xdate=True)
# # plt.xticks(rotation=90)
# # plt.yscale('log')

plt.show()