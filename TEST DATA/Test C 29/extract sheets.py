import pandas as pd


xls = pd.ExcelFile("TEST DATA/Test C 29/MM-TestC-29012026.xlsx")

for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet)
    df.to_csv(f"TEST DATA/Test C 29/MM-TestC 29-{sheet}.csv", index=False)