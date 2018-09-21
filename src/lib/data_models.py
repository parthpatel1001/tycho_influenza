class DataFile:
	def __init__(self, file_loc):
		self.file_loc = file_loc

	def iterate(self):
		with open(self.file_loc) as file:
			for line in file.readlines():
				yield line.strip().replace('"','').split(",")

	def row(self):
		return self.open_file

	def get(self, row, property):
		return row[self.headers[property]]

	def __enter__(self):
		self.open_file = self.iterate()
		self.headers = {v: i for i, v in enumerate(next(self.open_file))}
		return self

	def __exit__(self, *args):
		pass
		