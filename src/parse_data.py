import sys
assert len(sys.argv) > 1
file_loc = sys.argv[1]

def read_file(file_loc):
	""" yield stripped row in file_loc """
	with open(file_loc) as file:
		for line in file.readlines():
			yield line.strip()
def get(headers, row, property):
	""" get the property given headers and the row"""
	return row[headers.index(property)]


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


file = read_file(file_loc)
headers = next(file)
print(headers)

# the rest of the rows
# for row in file:
	# # do stuff
	# pass