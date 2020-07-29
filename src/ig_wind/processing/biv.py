from typing import List, Union
from pathlib import Path
import pandas as pd
import pickle
import xlwings as xw
from settings import conversion_multiplicators as conversion
from xlsx.charts import xlsx_chart

IDX = pd.IndexSlice
# ///////////////////////////////////////////////////////////////////// INPUTS


def get_biv_gesamt_data(
    eev_df: pd.DataFrame,
    field: str,
    energy_sources: Union[str, List],
    years: List,
    provinces: List
):

    # ///////////////////////////////////////////////////////////////////// DATA
    dfs = []

    for province in provinces:

        eev_data = eev_df.loc[
            IDX[field, "Gesamt", "Gesamt", "Gesamt",
                "Gesamt"], IDX[province, energy_sources, years]
        ].round(0)

        name = "-".join([x for x in eev_data.name if x != "Gesamt"])
        eev_data.name = province
        eev_data = eev_data.droplevel([0, 1], axis=0)
        dfs.append(eev_data)

    # ///////////////////////////////////////////////////////////////////// OUTPUTS
    biv_gesamt_tj = pd.concat(dfs, axis=1)
    biv_gesamt_pj = (biv_gesamt_tj * conversion["tj_2_pj"]).round(0)
    biv_gesamt_gwh = (biv_gesamt_tj * conversion["tj_2_gwh"]).round(0)
    biv_gesamt_twh = (biv_gesamt_tj * conversion["tj_2_twh"]).round(0)

    biv_gesamt = {
        "source": "Energiebilanzen Bundesländer, Bruttoinlandsverbrauch, Gesamtenergiebilanz",
        "TJ": biv_gesamt_tj,
        "PJ": biv_gesamt_pj,
        "GWh": biv_gesamt_gwh,
        "TWh": biv_gesamt_twh
    }

    return biv_gesamt


def biv_gesamt_2018_xlsx(
    wb: xw.Book,
    biv_gesamt: pd.DataFrame,
    sheet_name: str,
    title: str,
    unit: str,
    energy_units: List,
    provinces: List,
    width: int,
    height: int,
):

    try:
        wb.sheets.add(sheet_name)
        ws = wb.sheets[sheet_name]
    except:
        ws = wb.sheets[sheet_name]

    ws.clear_contents()

    ws.range("K1").value = f"Titel: {title}"
    ws.range('K1').api.Font.Bold = True
    ws.range("K2").value = f'Quelle: {biv_gesamt["source"]}'
    # next_row_number = ws.range("K1").end('down').row

    ws.range("K4").options(
        expand='table').value = biv_gesamt[unit].iloc[-1, :].to_frame().T
    ws.range("K4").value = unit

    # next_column_number = ws.range("K5").end('right').get_address(0, 0)[0]
    next_row_name_2 = "W4"

    for u in energy_units:

        ws.range(next_row_name_2).options(
            expand='table').value = biv_gesamt[u].iloc[-1, :].to_frame().T

        ws.range(next_row_name_2).value = u

        next_row_number_2 = ws.range(next_row_name_2).end('down').row + 2
        next_row_name_2 = "W" + str(next_row_number_2)

        # next_row_name = "K" + str(next_row_number)

    # ws.range(next_row_name).value = unit
    # next_row = ws.range("K({str(next_row+1)})").end('down').row

    # next_row = ws.range(next_row_name).end('down').row
    # last_column = ws.range("K3").end('right').get_address(0, 0)[0]
    # print("The last row is {row}.".format(row=next_row))
    # print("The last col is {col}.".format(col=last_column))

    xlsx_chart(
        ws=ws,
        df=biv_gesamt[unit],
        xaxis_values=provinces,
        title=title,
        chart_type="column_clustered",
        source_data=ws.range("L5").expand(),
        provinces=provinces,
        width=width,
        height=height,
        xaxis_title=" ",
        yaxis_title=unit
    )


def biv_gesamt_2018_pro_einwohner_xlsx(
    wb: xw.Book,
    biv_gesamt: pd.DataFrame,
    sheet_name: str,
    bevölkerung: pd.DataFrame,
    title: str,
    unit: str,
    energy_units: List,
    width: int,
    provinces: List,
    height: int,
):

    try:
        wb.sheets.add(sheet_name)
        ws = wb.sheets[sheet_name]
    except:
        ws = wb.sheets[sheet_name]

    ws.clear_contents()

    ws.range("K1").value = f"Titel: {title}"
    ws.range('K1').api.Font.Bold = True
    ws.range(
        "K2").value = f'Quelle: {biv_gesamt["source"]}, {bevölkerung["df"].index.name}'

    data = biv_gesamt[unit].iloc[-1, :] / \
        bevölkerung["df"].loc[2018, provinces]

    # Ratio
    ws.range("K4").options(
        expand='table').value = data
    ws.range("K4").value = f"{unit} / Person"

    # Energy
    ws.range("N4").options(
        expand='table').value = biv_gesamt[unit].iloc[-1, :].T
    ws.range("N4").value = f"{unit}"

    # Personen
    ws.range("Q4").options(
        expand='table').value = bevölkerung["df"].loc[2018, provinces].T
    ws.range("Q4").value = "Personen"

    # next_column_number = ws.range("K5").end('right').get_address(0, 0)[0]
    next_row_name_2 = "W4"

    for u in energy_units:

        ws.range(next_row_name_2).options(
            expand='table').value = biv_gesamt[u].iloc[-1, :].to_frame().T

        ws.range(next_row_name_2).value = u

        next_row_number_2 = ws.range(next_row_name_2).end('down').row + 2
        next_row_name_2 = "W" + str(next_row_number_2)

    xlsx_chart(
        ws=ws,
        df=data,
        xaxis_values=provinces,
        title=title,
        chart_type="column_clustered",
        source_data=ws.range("L5").expand(),
        provinces=provinces,
        width=width,
        height=height,
        xaxis_title="",
        yaxis_title=unit
    )


def biv_gesamt_entwicklung_xlsx(
    wb: xw.Book,
    biv_gesamt: pd.DataFrame,
    sheet_name: str,
    title: str,
    unit: str,
    energy_units: List,
    provinces: List,
    years: List,
    width: int,
    height: int,
):

    try:
        wb.sheets.add(sheet_name)
        ws = wb.sheets[sheet_name]
    except:
        ws = wb.sheets[sheet_name]

    ws.clear_contents()

    ws.range("K1").value = f"Titel: {title}"
    ws.range('K1').api.Font.Bold = True
    ws.range("K2").value = f'Quelle: {biv_gesamt["source"]}'
    # next_row_number = ws.range("K1").end('down').row

    ws.range("K4").options(
        expand='table').value = biv_gesamt[unit].iloc[:, :] / biv_gesamt[unit].loc[2000, :]
    ws.range("K4").value = unit

    # next_column_number = ws.range("K5").end('right').get_address(0, 0)[0]
    next_row_name_2 = "W4"

    # for u in energy_units:

    #     ws.range(next_row_name_2).options(
    #         expand='table').value = biv_gesamt[u].iloc[-1, :].to_frame().T

    #     ws.range(next_row_name_2).value = u

    #     next_row_number_2 = ws.range(next_row_name_2).end('down').row + 2
    #     next_row_name_2 = "W" + str(next_row_number_2)

    # next_row_name = "K" + str(next_row_number)

    # ws.range(next_row_name).value = unit
    # next_row = ws.range("K({str(next_row+1)})").end('down').row

    # next_row = ws.range(next_row_name).end('down').row
    # last_column = ws.range("K3").end('right').get_address(0, 0)[0]
    # print("The last row is {row}.".format(row=next_row))
    # print("The last col is {col}.".format(col=last_column))

    xlsx_chart(
        ws=ws,
        df=biv_gesamt[unit],
        xaxis_values=years,
        title=title,
        chart_type="line",
        source_data=ws.range("L5").expand(),
        provinces=provinces,
        years=years,
        width=width,
        height=height,
        xaxis_title=" ",
        yaxis_title=unit
    )
