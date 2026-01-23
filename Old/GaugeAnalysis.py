import numpy as np
from matplotlib import pyplot as plt

import LoadData as LD
import AnalyseStrain as AS


def showStrainGaugeData(strainData: dict, straingaugenumber: int):
	fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
	
	categories = []
	strainAverages = []
	
	for key in strainData.keys():
		# Find correct column for strain gauge number
		strainColumnNumber = int(np.where(np.char.find(strainData[key][0].astype(str), ' ' + str(straingaugenumber) + ' ') != -1)[0][0])

		strainGaugeData = strainData[key][1:, strainColumnNumber]
		timeData = strainData[key][1:, strainColumnNumber + 1]
		
		avgStrainGauge = np.average(strainGaugeData)
		strainAverages.append(avgStrainGauge)
		categories.append(key)
		print(f"Average strain {key}: {avgStrainGauge} [-]")
		
		# Plot the strain over time
		axes[0].plot(timeData, strainGaugeData, label=f"{key}")
	
	axes[0].legend()
	axes[0].set_xlabel("Time [s]")
	axes[0].set_ylabel("Strain [-]")
	axes[0].set_title("Strain over Time")
	
	# Plot the average values of the strain
	axes[1].scatter(categories, strainAverages)
	axes[1].set_xlabel("Test Measurements")
	axes[1].set_ylabel("Average strain [-]")
	axes[1].set_title("Average strain over measurements")
	
	plt.show()


def AnalyseStrainGauge(straindata: dict):
	
	running = True
	while running:
		strainGaugeNumber = input("Enter strain gauge number (up to and including 33): ")

		# Check if given input is indeed a number
		try:
			if 1 <= int(strainGaugeNumber) <= 33:
				
				showStrainGaugeData(straindata, int(strainGaugeNumber))
		except ValueError:
			if strainGaugeNumber.lower() == "stop":
				running = False
		
		
if __name__ == "__main__":
	test_letter = ("A")
	DataSet = LD.load_dataset(test_letter)
	StrainData = AS.calculateStrain(DataSet, test_letter)
	
	AnalyseStrainGauge(StrainData)
