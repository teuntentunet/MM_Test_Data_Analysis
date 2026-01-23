import numpy as np
import matplotlib.pyplot as plt


def makeScatterPlotData(dataset: dict, test: str):
	numberOfPlotsToPlot = len(dataset[f"Test-{test}-NULL"][0]) // 2
	idx = 0
	for fig in range(numberOfPlotsToPlot // 9 + 1):
		# Create a 3x3 subplot grid
		fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(14, 10))
		
		# Plot something in each subplot
		for i in range(3):
			for j in range(3):
				ax = axes[i, j]

				if idx/2 < 35:
					for key in DataSet.keys():
						ax.plot(dataset[key][1:, idx+1], dataset[key][1:, idx], label=f"{key[7:]}")
						ax.set_title(f'{DataSet[key][0, idx]}')
					
					ax.legend()
					ax.set_xlabel("Time [s]")
					ax.set_ylabel("Volt [V]")
					
				idx += 2
	
	plt.show()


def analyseStrainVoltage(dataset: dict, test: str):
	makeScatterPlotData(dataset, test=test)


if __name__ == "__main__":
	import LoadData as LD
	DataSet = LD.load_dataset("B")
	for key in DataSet.keys():
		print(key)
	analyseStrainVoltage(DataSet, "B")
	