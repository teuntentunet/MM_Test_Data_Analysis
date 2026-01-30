import numpy as np
import pandas as pd
import os

# Channel to number for test on 19/01
# ChannelToNumber = [
# 		[201, 'Temp_amb'],
# 		[202, 'Temp_mm'],
# 		[121, 'unknown'],
# 		[123, 5],
# 		[133, 6],
# 		[126, 7],
# 		[124, 8],
# 		[130, 9],
# 		[129, 10],
# 		[134, 11],
# 		[127, 12]
# 	]

# Channel to number for test on 23/01
ChannelToNumber = [
		[201, 'Temp_amb'],
		[202, 'Temp_mm'],
		[121, 'Us'],
		[132, 1],
		[123, 2],
		[124, 3],
		[125, 4],
		[126, 5],
		[127, 6],
		[128, 7],
		[129, 8],
		[130, 9],
		[131, 10],
		[134, 11],
		[135, 12],
		[138, 13],
		[136, 14],
		[139, 15],
		[137, 16],
		[135, 17],
		[140, 18]
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
	"RES",
	"Standing",
	"Onside"
]

DataSet = {

}

#cycle is either '' or '1.' to '5.'  with the period after the number

cycles = [''] + [f"{i}." for i in range(6)]

def load_dataset(test: str = "A"):
	for cycle in cycles:
		for data_key in DataKeys:
			for pump in ["", " NULL"]:
				path = f"TEST DATA\\Test {test}\\MM-Test{test}-{cycle}{data_key}{pump}.csv"
				
				if os.path.exists(path):
					data = pd.read_csv(path, header=1)
					#drop 0th row
					data = data.iloc[1:].reset_index(drop=True)
					#drop each 2nd column
					data = data.drop(data.columns[3::2], axis=1)
					#switch first and second column
					data = data[[data.columns[1]] + [data.columns[0]] + list(data.columns[2:])]
					#drop nan
					data = data.dropna().reset_index(drop=True)
					#rename Time column to time
					data = data.rename(columns={data.columns[0]: "time"})
					#rename channels according to ChannelToNumber
					for channel, number in ChannelToNumber:
						col_name = f"Chn {channel}"
						if col_name in data.columns:
							if number is not None:
								data = data.rename(columns={col_name: f"{number}"})
							else:
								data = data.drop(columns=[col_name])
					DataSet[f"Test-{test}-{cycle}{data_key}{pump}"] = data.to_numpy(dtype=object)
					#include headers
					DataSet[f"Test-{test}-{cycle}{data_key}{pump}"] = np.vstack([data.columns.to_numpy(), DataSet[f"Test-{test}-{cycle}{data_key}{pump}"]])
		
	return DataSet


if __name__ == "__main__":
	dataset = load_dataset("B 27")
	#convert all arrayes in the dataset to csv files.
	for key in dataset.keys():
		np.savetxt(f"{key}_processed.csv", dataset[key], delimiter=",", fmt="%s")
		print(f"Saved {key}_processed.csv")
	