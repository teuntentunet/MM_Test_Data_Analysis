import pandas as pd


xls = pd.ExcelFile("TEST DATA/Test B 27/MM-TestB-27012026.xlsx")

for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet)
    #make sure that if the first two rows are empty, that you start saving from the second row. Because only one row should be empty
    df = df.iloc[1:] if df.iloc[0].isnull().all() else df
    #if a sheet has NULL in its name, save it with a space before NULL
    if 'NULL' in sheet:
        sheet = sheet.replace('NULL', ' NULL')
    

    df.to_csv(f"TEST DATA/Test B 27/MM-TestB 27-{sheet}.csv", index=False)