import numpy as np
import matplotlib.pyplot as plt
import LoadData as LD
import pandas as pd



def analyseStrain(dataset: dict, test: str):
    strainData = calculateStrain(dataset, test)
    
    makeScatterPlotData(strainData, test=test)

def strainFormula(U_m, U_s, GaugeFactor: float = 2.12):
    return - 4 / (GaugeFactor * 2.16) * U_m

def calculateStrain(dataset: dict, test: str):
    # Determine measured strain
    measuredStrainData = {}
    for key in dataset.keys():
        df = pd.DataFrame(dataset[key][1:], columns=dataset[key][0])
        #display df
        print(df)
        #Us is the value in the column dataset['unknown']
        U_s = df['unknown'].astype(float).values
        #um is the values in the rest of the columns
        U_m = df.drop(columns=['time', 'unknown', 'Temp_amb', 'Temp_mm']).astype(float).values
        measuredStrain = np.zeros_like(U_m)
        for i in range(U_m.shape[1]):
            measuredStrain[:, i] =  strainFormula(U_m[:, i], U_s, 2.12)
        
        measuredStrainData[key] = measuredStrain
    # Correct for initial offset which is the strains in the null test
    realStrainData = {}
    nullStrains = measuredStrainData[f"Test-{test}-NULL"]
    #average
    nullStrain = np.mean(nullStrains, axis=0)

    for key in measuredStrainData.keys():
        realStrainData[key] = measuredStrainData[key] - nullStrain
    
    #add temperature columns back and time column
    for key in realStrainData.keys():
        df = pd.DataFrame(dataset[key][1:], columns=dataset[key][0])
        time_column = df['time'].astype(float).values.reshape(-1, 1)
        temp_amb_column = df['Temp_amb'].astype(float).values.reshape(-1, 1)
        temp_mm_column = df['Temp_mm'].astype(float).values.reshape(-1, 1)
        realStrainData[key] = np.hstack([time_column, temp_amb_column, temp_mm_column, realStrainData[key]])

    #include headers like this DataSet[f"Test-{test}-{data_key}{pump}"] = np.vstack([data.columns.to_numpy(), DataSet[f"Test-{test}-{data_key}{pump}"]])
    for key in realStrainData.keys():
        df = pd.DataFrame(dataset[key][1:], columns=dataset[key][0])
        headers = ['time', 'Temp_amb', 'Temp_mm'] + list(df.drop(columns=['time', 'unknown', 'Temp_amb', 'Temp_mm']).columns)
        realStrainData[key] = np.vstack([np.array(headers), realStrainData[key]])
    
    return realStrainData

def makeScatterPlotData(dataset: dict, test: str):
    numberOfPlotsToPlot = (len(dataset[f"Test-{test}-NULL"][0]) - 3) // 1  # minus 3 for time and temps
    idx = 0
    for fig in range(numberOfPlotsToPlot // 9 + 1):
        # Create a 3x3 subplot grid
        fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(14, 10))
        
        # Plot something in each subplot
        for i in range(3):
            for j in range(3):
                ax = axes[i, j]

                if idx < numberOfPlotsToPlot:
                    for key in dataset.keys():
                        ax.plot(dataset[key][1:, 0].astype(float), dataset[key][1:, idx + 3].astype(float), label=f"{key[7:]}")
                        ax.set_title(f'Strain Gauge {dataset[key][0, idx + 3]}')
                    
                    ax.legend()
                    ax.set_xlabel("Time [s]")
                    ax.set_ylabel("Strain")
                    
                idx += 1
                plt.tight_layout()
    #add temperature plots
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
    #Temp_amb
    ax = axes[0]
    for key in dataset.keys():
        ax.plot(dataset[key][1:, 0].astype(float), dataset[key][1:, 1].astype(float), label=f"{key[7:]}")
        ax.set_title('Ambient Temperature')
    ax.legend()
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Temperature [°C]")
    #Temp_mm
    ax = axes[1]
    for key in dataset.keys():
        ax.plot(dataset[key][1:, 0].astype(float), dataset[key][1:, 2].astype(float), label=f"{key[7:]}")
        ax.set_title('MM Temperature')
    ax.legend()
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Temperature [°C]")

    plt.tight_layout()
    plt.show()





if __name__ == "__main__":
    
    test_letter = "A 21"
    DataSet = LD.load_dataset(test_letter)
    realStrainData = calculateStrain(DataSet, test_letter)
    #save realStrainData to csv files
    for key in realStrainData.keys():
        np.savetxt(f"{key}_strain.csv", realStrainData[key], delimiter=",", fmt="%s")
        print(f"Saved {key}_strain.csv")

    analyseStrain(DataSet, test_letter)