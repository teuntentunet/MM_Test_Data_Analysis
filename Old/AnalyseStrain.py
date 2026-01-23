import numpy as np
import matplotlib.pyplot as plt


def makeScatterPlotData(straindata: dict, test: str):
    numberOfPlotsToPlot = len(straindata[f"Test-{test}-25"][0]) // 2
    idx = 0
    for fig in range(numberOfPlotsToPlot // 9 + 1):
        # Create a 3x3 subplot grid
        fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(14, 10))
        
        # Plot something in each subplot
        for i in range(3):
            for j in range(3):
                ax = axes[i, j]
                
                if idx < 70:
                    for key in DataSet.keys():
                        ax.plot(straindata[key][1:, idx + 1], straindata[key][1:, idx], label=f"{key[7:]}")
                        ax.set_title(f'{DataSet[key][0, idx]}')
                    
                    ax.legend()
                    ax.set_xlabel("Time [s]")
                    ax.set_ylabel("Strain [-]")
                
                idx += 2
    
    plt.show()


def analyseStrain(dataset: dict, test: str):
    strainData = calculateStrain(dataset, test)
    
    makeScatterPlotData(strainData, test=test)


def calculateStrain(dataset: dict, test: str):
    # Determine measured strain
    measuredStrainData = {}
    for key in dataset.keys():
        measuredStrain = np.zeros(np.shape(dataset[key]), dtype=object)
        measuredStrain[0] = dataset[key][0]
        
        for i in range(int(len(dataset[key][0]) / 2)):
            # For the first box, take voltage measured in channel 1
            # For second box, take voltage measured in channel 221
            if i < 20:
                U_s = dataset[key][1:, 0]
            else:
                U_s = dataset[key][1:, 2*20]
            
            U_m = dataset[key][1:, 2 * i]
            
            strainStrainGauge = strainFormula(U_m, U_s, 2.12)
            
            measuredStrain[1:, 2 * i] = strainStrainGauge
            measuredStrain[1:, 2 * i + 1] = dataset[key][1:, 2 * i + 1]
        
        measuredStrainData[key] = measuredStrain
    
    realStrainData = {}
    nullStrain = measuredStrainData[f"Test-{test}-NULL"]

    for key in measuredStrainData.keys():
        numberOfMeasurements = min(len(measuredStrainData[key][1:, 0]), len(nullStrain[1:, 0]))
        realStrainStrainGauge = np.zeros((numberOfMeasurements + 1, len(measuredStrainData[key][0])), dtype=object)
        realStrainStrainGauge[0] = dataset[key][0]
        
        for i in range(int(len(dataset[key][0]) / 2)):
            numberOfMeasurements = min(len(measuredStrainData[key][1:, 2*i]), len(nullStrain[1:, 2*i]))
    
            realStrainStrainGauge[1:numberOfMeasurements+1, 2*i] = measuredStrainData[key][1:numberOfMeasurements+1, 2*i] - nullStrain[1:numberOfMeasurements+1, 2*i]
            realStrainStrainGauge[1:, 2*i + 1] = dataset[key][1:numberOfMeasurements+1, 2*i + 1]
        
        realStrainData[key] = realStrainStrainGauge
    
    return realStrainData


def strainFormula(U_m, U_s, GaugeFactor: float = 2.12):
    return - 4 / (GaugeFactor * U_s) * U_m


if __name__ == "__main__":
    import LoadData as LD
    
    test_letter = "A"
    DataSet = LD.load_dataset(test_letter)
    analyseStrain(DataSet, test_letter)
