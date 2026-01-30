import pandas as pd


xls = pd.ExcelFile("TEST DATA/Test NULLextra/MM-TestNULL-extra.xlsx")

for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet)
    df.to_csv(f"TEST DATA/Test NULLextra/MM-TestNULL-extra{sheet}.csv", index=False)