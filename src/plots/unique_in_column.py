import matplotlib.pyplot as plt
from IPython.display import HTML, display
from tabulate import tabulate
import sys
from src.lib.data_models import DataFile

# %matplotlib inline

assert len(sys.argv) > 2
file_loc, column_name = sys.argv[1], sys.argv[2]

print("#### Reading data from '%s'" % file_loc)
pathogen_names = set()

with DataFile(file_loc) as file:
	for row in file.row():
		pathogen_names.add(
			file.get(row, column_name)
		)

display(HTML(tabulate(
	sorted([list(pathogen_names)]),
	headers=['Unique %s Values' % column_name],
	tablefmt='html'
)))