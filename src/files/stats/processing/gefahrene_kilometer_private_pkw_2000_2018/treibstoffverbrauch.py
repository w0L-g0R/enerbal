from pathlib import Path
import pandas as pd
import pickle
import xlwings as xw
import numpy as np
IDX = pd.IndexSlice
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

file = Path("C:/Code/enerbal/src/files/stats/processing/gefahrene_kilometer_private_pkw_2000_2018/fahrleistungen_privater_pkw.xlsx")
sheet_names = [
    "Österreich",
    "Burgenland",
    "Kärnten",
    "Niederösterreich",
    "Oberösterreich",
    "Salzburg",
    "Steiermark",
    "Tirol",
    "Vorarlberg",
    "Wien"
]
dfs = {}

for sheet_name in sheet_names:
    dfs[sheet_name] = pd.read_excel(file, sheet_name=sheet_name)

index = [1999]
index.extend(list(range(2003, 2015, 2)))
print(index)
df_output = pd.DataFrame(index=index, columns=sheet_names)

wb = xw.Book()

for enum, sheet_name in enumerate(sheet_names):

    df = dfs[sheet_name].iloc[:, :4]
    df.set_index(df.columns[0], inplace=True)
    # df.reset_index(inplace=True, drop=True)
    df = df[df.index.notnull()]

    # Get all indices with "Q-Statistik ..." as the row value
    i = []
    for idx in df[df.index.str.startswith("Q")].index:
        i.append(df.index.get_loc(idx))

    # Iter over indices and check row above for keyword "Zusammen"
    p = []
    for idx in i:

        col_idx = 3
        row_idx_offset = 4

        g = df.iloc[idx - row_idx_offset:idx, -1]
        g.name = sheet_name
        if g.index[-1] == "Zusammen":
            p.append(g)
        else:
            raise Error

    # for sheet_name in sheet_names:
        # try:
    wb.sheets.add(sheet_name)
    # except:
    #     pass
    last_column = "A2"

    df_fuel_liter = pd.DataFrame(
        columns=index, index=[
            "Benzin", "Diesel", "Zusammen"])

    df_fuel_TWh = pd.DataFrame(
        columns=index,
        index=[
            "Benzin",
            "Diesel",
            "Zusammen"])

    df_conversions = pd.DataFrame(
        columns=["Faktor", "Einheit"],
        index=[
            "Benzin", "Diesel"], data=[[8.777777778, "kWh/L"], [9.95, "kWh/L"]])

    for v, idx in zip(p, index):
        print(v)
        ws = wb.sheets[sheet_name]
        ws.range(last_column).api.Font.Bold = True
        ws.range(last_column).value = "Liter"
        try:
            v.drop("Sonstiger", inplace=True)
        except BaseException:
            pass

        try:
            v.drop("Insgesamt", inplace=True)
        except BaseException:
            pass
        v.index.name = idx
        v["Zusammen"] = v.iloc[:2].sum(axis=0)
        print('v: ', v)

        df_fuel_liter.loc[:, idx] = v

        df_fuel_TWh.iloc[0, :] = df_fuel_liter.iloc[0, :] * 8.777777778
        df_fuel_TWh.iloc[1, :] = df_fuel_liter.iloc[1, :] * 9.95
        df_fuel_TWh.iloc[2, :] = \
            df_fuel_TWh.iloc[0, :] \
            + df_fuel_TWh.iloc[1, :]
        # \
        #   np.array([8.777777778, 9.95]) / 1e9  # kWh -> TWh
        # v["Zusammen"] = v.iloc[:2].sum(axis=0)
        # df_fuel.loc[:, idx] = v

        df_fuel_TWh.index.name = "TWh"
        df_fuel_liter.index.name = "Liter"
        print(df_fuel_TWh)

    ws.range(last_column).value = np.around(df_fuel_TWh / 1e9, 2)
    ws.range(last_column).end('up').offset(
        0, 1).value = "Treibstoffverbrauch"

    ws.range(last_column).end('down').offset(2, 0).value = df_fuel_liter

    ws.range(last_column).end('down').offset(7, 0).value = df_conversions

    print(last_column)
