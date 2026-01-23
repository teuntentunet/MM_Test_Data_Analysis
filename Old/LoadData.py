import numpy as np
import os

ChannelToNumber = [
		[201, None],
		[202, 31],
		[203, 2],
		[204, 3],
		[205, 4],
		[206, 5],
		[207, 1],
		[208, 6],
		[209, 7],
		[210, 8],
		[211, 20],
		[212, 21],
		[213, 9],
		[214, 32],
		[215, 18],
		[216, 12],
		[217, 14],
		[218, 11],
		[219, 10],
		[220, 13],
		[221, None],
		[222, 19],
		[223, 17],
		[224, 16],
		[225, 15],
		[226, 28],
		[227, 29],
		[228, 23],
		[229, 30],
		[230, 22],
		[231, 33],
		[232, 27],
		[233, 24],
		[234, 26],
		[235, 25],
	]

DataKeys = [
	"NULL",
	"12.5",
	"25",
	"37.5",
	"50",
	"62.5",
	"75",
	"87.5",
	"100",
	"BREAKING",
	"RESIDUAL",
]

DataSet = {

}


def load_dataset(test: str = "A"):
	for data_key in DataKeys:
		for pump in ["", "-PUMP"]:
			path = f"OLD\\OLD_TEST DATA\\Test {test}\\STR-MM-TEST-{test}-STRAIN-{data_key}{pump}.csv"
			
			if os.path.exists(path):
				data = np.genfromtxt(path, delimiter=",", skip_header=3, usecols=np.arange(0, 70), max_rows=75).astype(object)
				
				header = ["Chn 201", "Time",
				          "Chn 202", "Time",
				          "Chn 203", "Time",
				          "Chn 204", "Time",
				          "Chn 205", "Time",
				          "Chn 206", "Time",
				          "Chn 207", "Time",
				          "Chn 208", "Time",
				          "Chn 209", "Time",
				          "Chn 210", "Time",
				          "Chn 211", "Time",
				          "Chn 212", "Time",
				          "Chn 213", "Time",
				          "Chn 214", "Time",
				          "Chn 215", "Time",
				          "Chn 216", "Time",
				          "Chn 217", "Time",
				          "Chn 218", "Time",
				          "Chn 219", "Time",
				          "Chn 220", "Time",
				          "Chn 221", "Time",
				          "Chn 222", "Time",
				          "Chn 223", "Time",
				          "Chn 224", "Time",
				          "Chn 225", "Time",
				          "Chn 226", "Time",
				          "Chn 227", "Time",
				          "Chn 228", "Time",
				          "Chn 229", "Time",
				          "Chn 230", "Time",
				          "Chn 231", "Time",
				          "Chn 232", "Time",
				          "Chn 233", "Time",
				          "Chn 234", "Time",
				          "Chn 235", "Time"]
				
				data = np.insert(data, 0, header, axis=0)
				
				# List to store rows without NaN values
				filtered_rows = []
				
				# Iterate through each row
				for row in data:
					# Check if the row contains NaN values
					if not any(
							np.isnan(value) if isinstance(value, (int, float, complex)) else value == '' for value in row):
						filtered_rows.append(row)
				
				# Convert the list of rows back to a NumPy array
				data = np.array(filtered_rows)
				
				for channelNumber, number in ChannelToNumber:
					data[np.where(data == f"Chn {channelNumber}")] = f"Strain Gauge {number} "
				
				DataSet[f"Test-{test}-{data_key}{pump}"] = data
	
	return DataSet


if __name__ == "__main__":
	load_dataset("G")

