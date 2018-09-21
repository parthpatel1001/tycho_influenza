import sys
from tabulate import tabulate
from lib.data_models import DataFile

assert len(sys.argv) > 1
file_loc = sys.argv[1]

# 0  : "ConditionName"
# 1  : "ConditionSNOMED"
# 2  : "PathogenName"
# 3  : "PathogenTaxonID"
# 4  : "Fatalities"
# 5  : "CountryName"
# 6  : "CountryISO"
# 7  : "Admin1Name"
# 8  : "Admin1ISO"
# 9  : "Admin2Name"
# 10 : "CityName"
# 11 : "PeriodStartDate" YYYY-MM-DD
# 12 : "PeriodEndDate" YYYY-MM-DD
# 13 : "PartOfCumulativeCountSeries"
# 14 : "AgeRange"
# 15 : "Subpopulation"
# 16 : "PlaceOfAcquisition"
# 17 : "DiagnosisCertainty"
# 18 : "SourceName"
# 19 : "CountValue"

with DataFile(file_loc) as file:
	# do things w/ the data
	instances_over_year = {}
	for row in file.row():
		date = file.get(row, "PeriodStartDate")
		year = date.split('-')[0].replace('"','')
		instances_over_year[year] = instances_over_year.setdefault(year, 0) + 1

print(tabulate(
	# print sorted by years
	sorted(instances_over_year.items(), key=lambda x: x[0]),
	headers=['Year', '# of Instances'],
	tablefmt='psql'
))