import datetime
import logging
from pathlib import Path
from typing import Dict, List, Union

import numpy as np
import pandas as pd
from enspect.conversion.energiebilanzen.check_errors import (
    check_column_errors,
    check_index_errors,
    check_sheetname_errors
)
from enspect.aggregates.eb import eb_sheet_names
from enspect.logger.setup import setup_logging
from enspect.paths import file_paths
from enspect.utils import timeit

IDX = pd.IndexSlice
# ///////////////////////////////////////////////////////////////////// INDICES


def create_indices(provinces: List, last_year: int):

    # Create a row multiindex from xlsx "midx_rows_eb"

    eb_row_midx = None
    res_row_midx = None

    path_midx_eb = file_paths["files_eb"] / "midx_rows_eb.xlsx"
    path_midx_res = file_paths["files_eb"] / "midx_rows_res.xlsx"

    for path, sheet_name in zip(
        [path_midx_eb, path_midx_res],
        ["MIDX_EB", "MIDX_RES"],
    ):

        midx = pd.MultiIndex.from_tuples(
            tuples=[
                tuple(x)
                for x in pd.read_excel(
                    io=path,
                    sheet_name=sheet_name,
                    na_filter=False,
                    header=None,
                ).values
            ],
            names=["BAGG_0", "BAGG_1", "BAGG_2", "BAGG_3", "BAGG_4"],
        )

        if "EB" in sheet_name:
            eb_row_midx = midx
        else:
            res_row_midx = midx

    # Extract and round column with unit conversions (pre-processed manually)
    res_conversion_factors = np.around(
        res_row_midx.get_level_values("BAGG_4"), 8)

    # Drop conversion unit and factors
    res_row_midx = res_row_midx.droplevel([-1, -2])

    # ______________________________________________________ COL MULTI INDEX
    # Create column midx with provinces, energy_sources, years
    eb_col_midx = pd.MultiIndex.from_product(
        [
            provinces,
            eb_sheet_names,  # energy sources
            list(range(1988, last_year + 1, 1)),  # years
        ],
        names=["PROV", "ES", "YEAR"],
    )

    # Create a column muliindex with levels [province, Jahre]
    res_col_midx = pd.MultiIndex.from_product(
        [
            provinces,
            list(range(1988, last_year + 1, 1)),
        ],  # years
        names=["PROV", "YEAR"],
    )

    return eb_row_midx, res_row_midx, eb_col_midx, res_col_midx, res_conversion_factors


# ///////////////////////////////////////////////////////////// INDEX TEMPLATES


def create_index_template(midx: pd.MultiIndex, data_type: str):

    # if "res" in data_type:

    # Flatten the multiindex to tuples
    template = list(midx.to_flat_index().unique())
    template = [dict.fromkeys(_tuple) for _tuple in template]
    template = [list(d.keys()) for d in template]

    single_index_values = []

    # Extract from tuples
    for _tuple in template:

        # Get rid of level values "Gesamt"
        if _tuple[-1] == "Gesamt":

            if len(_tuple) >= 2:
                single_index_values.append(_tuple[-2])

            else:
                single_index_values.append(_tuple[-1])
        else:
            single_index_values.append(_tuple[-1])

    template = pd.Index(single_index_values)

    return template


# //////////////////////////////////////////////////////// FETCH_ENERGY_SOURCES


@timeit
def fetch_from_xlsx(file: str, years: pd.Series):
    """
    Extracts all sheets (=energieträger) from file at once, per province

    NOTE: pd.read_excel with sheet_name=None creates a dictionary (=> energy_sources_sheets) with keys == sheetnames
    """

    # AT file needs to be treated differently
    if "AT" in file:

        # Exclude columns with years '70 until '88
        energy_sources_sheets = pd.read_excel(
            io=file,
            sheet_name=None,
            na_filter=False,
            usecols="A,T:AX",
        )

        # Exclude unwanted columns (==years)
        energy_sources_sheets["Mischgas"] = pd.read_excel(
            io=file,
            sheet_name="Mischgas",
            na_filter=False,
            usecols="A,P:X",
        )

        # This sheet only appears in "ET_AT_70_18"
        del energy_sources_sheets["Generatorgas"]

        # Don't fetcht the RES data from AT file
        res_sheet = None

    # All other provinces
    else:
        energy_sources_sheets = pd.read_excel(
            io=str(file),
            sheet_name=None,
            na_filter=False,
        )

    # Delete non relevant sheets
    del energy_sources_sheets["Deckblatt"]
    del energy_sources_sheets["Grundbegriffe"]
    del energy_sources_sheets["Klassifikation"]
    del energy_sources_sheets["Wirkungsgrade"]

    # Delete hidden sheets if existing
    try:
        del energy_sources_sheets["checkFormal"]
    except BaseException:
        pass

    # NOTE: RES sheet names differ (=> "EU-Richtlinie" vs. "EU Richtlinie")
    try:
        # Extract "Erneuerbaren RL" to a seperate variable
        res_sheet = energy_sources_sheets["Erneuerbare EU Richtlinie"].copy()

        del energy_sources_sheets["Erneuerbare EU Richtlinie"]

    except BaseException:

        # Extract "Erneuerbaren RL" to a seperate variable
        res_sheet = energy_sources_sheets["Erneuerbare EU-Richtlinie"].copy()

        del energy_sources_sheets["Erneuerbare EU-Richtlinie"]

    # Perform data checks and correct errors
    check_sheetname_errors(
        energy_sources_sheets=energy_sources_sheets,
        years=years)

    energy_sources_sheets = check_column_errors(
        energy_sources_sheets=energy_sources_sheets, years=years
    )

    return energy_sources_sheets, res_sheet


# ///////////////////////////////////////////////////////// CORRECT FILE ERRORS


def add_missing_row_indices(
    data: pd.DataFrame, data_type: str, template_index: pd.DataFrame = None
):

    if data.index[-1] == "":
        data = data.iloc[:-1, :]

    if data_type == "sectors":

        logging.getLogger().debug(
            "\t* Missing last index {}".format(province,
                                               energy_source, "Sonstige")
        )

        # Add the missing index
        df_with_additional_indices = pd.DataFrame(
            data=np.nan, index=["Sonstige"], columns=data.columns
        )

    elif data_type == "sector_energy":

        logging.getLogger().debug("\t* Missing last index '{}'".format("Gesamt"))

        # Add the missing index
        df_with_additional_indices = pd.DataFrame(
            data=np.nan, index=["Gesamt"], columns=data.columns
        )

    elif data_type == "sectors_data":

        # Extract missing indices from template
        missing_indices = template_index[len(data.index):]

        # Return original data if no differences in length
        if len(missing_indices) == 0:
            return data

        # Add the missing index
        df_with_additional_indices = pd.DataFrame(
            data=np.nan, index=missing_indices, columns=data.columns
        )

    return pd.concat([data, df_with_additional_indices], axis="index")


# ///////////////////////////////////////////////////////////// GET SECTOR DATA


def get_sectors_data(df: pd.DataFrame, energy_source: str, province: str):
    """
    This function tries to merge the values for the consumption of the different sectors (sectors_data) with the values of the sector energy (sector_energy_data).
    """

    # Check row index as integer
    sectors_index = df.index.get_indexer_for(["Sektoraler Energetischer Endverbrauch"])[
        0
    ]
    sector_energy_index = df.index.get_indexer_for(
        ["Verbrauch Sektor Energie"])[0]

    # Iter over indices
    for enum, idx in enumerate([sectors_index, sector_energy_index]):

        # Check if sheet has no sector information (in terajoules)
        if idx == [-1] or df.index[idx] == "in Tonnen":

            # Sectors
            if enum == 0:

                logging.getLogger().debug("\tNo sectors consumption values")
                sectors_data = None

            # Sector energy
            elif enum == 1:

                logging.getLogger().debug("\tNo sector energy consumption values")
                sector_energy_data = None

        else:

            # Sectors
            if enum == 0:

                logging.getLogger().debug(
                    "\tSectors consumptions starts @ xlsx row nr.: {}".format(
                        sectors_index
                    )
                )

                # Extract data from sheet
                sectors_data = df.iloc[
                    sectors_index + 3: sectors_index + 27, : len(df.columns)
                ]

                # Check if data ends with wrong index
                if sectors_data.index[-1] != "Sonstige":
                    # print("sectors_data.index[-1]: ", sectors_data.index[-1])

                    sectors_data = add_missing_row_indices(
                        data=sectors_data, data_type="sectors"
                    )

                # Assign col midx
                sectors_data.columns = df.columns

            # Sector energy
            elif enum == 1:

                logging.getLogger().debug(
                    "\tSector energy consumption starts @ xlsx row nr.: {}".format(
                        sector_energy_index
                    )
                )

                # Extract data from sheet
                sector_energy_data = df.iloc[
                    sector_energy_index + 3: sector_energy_index + 10,
                    : len(df.columns),
                ]

                # Check if data ends with wrong index
                if sector_energy_data.index[-1] != "Gesamt":

                    sector_energy_data = add_missing_row_indices(
                        data=sector_energy_data, data_type="sector_energy"
                    )

                # Assign col midx
                sector_energy_data.columns = df.columns

    # No sector data at all
    if sectors_data is None and sector_energy_data is None:
        return

    # Only sector energy data
    elif sectors_data is None and sector_energy_data is not None:
        return sector_energy_data

    # Only sectors data
    elif sector_energy_data is None and sectors_data is not None:
        return sectors_data

    # Both exist
    else:
        return pd.concat([sectors_data, sector_energy_data], axis="index")


@timeit
def copy_eb_data(
    province: str,
    eb_df: pd.DataFrame,
    eb_sheets: Dict,
    eb_idx_template: pd.Index,
    eb_row_midx: pd.MultiIndex,
):

    # Iter over sheets (==energy sources)
    for enum, energy_source in enumerate(eb_sheet_names):

        # for energy_source in ["ÖL"]:
        logging.getLogger().debug(
            "{}\n{}-{}\n{}\n".format("_" * 79, enum + 1,
                                     energy_source, "_" * 79)
        )

        # Reassign current dataframe for better readibility
        df = (
            eb_sheets[energy_source]
            .iloc[:475, :]
            .set_index(eb_sheets[energy_source].columns[0], drop=True)
            .apply(pd.to_numeric, errors="coerce")
            .round(2)
        )

        eev_data, sectors_data = (
            # Extract relevant eev rows, convert to numeric and round
            df.iloc[3:193, : len(df.columns)],
            # Extract energetic end use data of sectors
            get_sectors_data(
                df=df,
                energy_source=energy_source,
                province=province),
        )

        # Combine data
        eb_data = pd.concat([eev_data, sectors_data], axis="index")

        # Add missing indices
        if len(eb_data.index) != len(eb_idx_template):

            eb_data = add_missing_row_indices(
                data_type="sectors_data",
                data=eb_data,
                template_index=eb_idx_template,
            )

        check_index_errors(
            data=eb_data,
            template_index=eb_idx_template,
        )

        eb_data.index, eb_data.columns = (
            eb_row_midx,
            eb_df.loc[IDX[:], IDX[province, energy_source, :]].columns,
        )

        # eb_data.sort_index(inplace=True, axis="rows", level=0)
        # eb_data.sort_index(inplace=True, axis="rows")

        # Copy current energy source data to container eb_df
        eb_df.loc[IDX[:], IDX[province, energy_source, :]] = eb_data  #

    return eb_df


# //////////////////////////////////////////// PREPROCESS_res_sheet


def preprocess_res_sheet(
    res_sheet: pd.DataFrame,
    res_conversion_factors: pd.Series,
    template_index: pd.Index,
    years: List,
):

    # First column includes the index data
    sheet_index = pd.Index(res_sheet.iloc[:, 0])

    # Exclude empty prevailing columns
    res_sheet = res_sheet.iloc[:, 19: 19 + len(years)]
    res_sheet.columns = years

    # Check for differences amongst indices
    deviations = sheet_index.difference(template_index)

    if deviations is not None:

        logging.getLogger().warning("\n\t{} WARNING {}".format("*" * 33, "*" * 33))

        deviation_idx = []
        for index in [
            "Verbrauch Sektor Energie: E5 & E7 (TJ)",
            "Verluste: E5 & E7 (TJ)",
            "Anrechenbare Erneuerbare (TJ)",
            "Anteil Erneuerbarer Energieträger insgesamt",
            "Anteil anrechenbare Erneuerbare Landwirtschaft",
            "Primärstrom Wasser real mit Pumpe (MWh)",
            "Primärstrom Wasser real ohne Pumpe (MWh)",
            "Umgebungswärme (anrechenbarer Anteil)",
        ]:

            if index in deviations:
                deviation_idx.append(index)
                deviations = deviations.drop([index])

        logging.getLogger().warning(
            r"\Deviating indices in res data:\n\t{}".format(deviation_idx)
        )

    # Set first column with indices as df index
    res_sheet.set_index(sheet_index, drop=True, inplace=True)

    # Drop rows that are not used
    res_sheet.drop(
        index=deviations,
        axis=0,
        inplace=True,
        errors="raise",
    )

    res_sheet = res_sheet.apply(pd.to_numeric, errors="coerce").round(2)

    # TODO: Replace with appropriate function
    # Turn all string values to NaN
    for i in res_sheet.index:
        for j in res_sheet.columns:
            if isinstance(res_sheet.loc[i, j], str):
                res_sheet.loc[i, j] = np.nan

    # Convert all values to TJ and MW
    res_sheet = res_sheet.mul(res_conversion_factors, axis=0)

    return res_sheet


@timeit
def copy_res_data(
    province: str,
    res_df: pd.DataFrame,
    res_sheet: pd.DataFrame,
    res_idx_template: pd.Index,
    res_row_midx: pd.MultiIndex,
    res_col_midx: pd.MultiIndex,
):

    logging.getLogger().debug("{}\n{}-{}\n{}\n".format("_" * 79, 82, "RES", "_" * 79))

    # Assign midx for rows and columns
    res_sheet.columns = res_df.loc[IDX[:], IDX[province, :]].columns

    res_sheet.index = res_row_midx

    # Copy res data to container res_df
    res_df.loc[IDX[:], IDX[province, :]] = res_sheet  #

    return res_df


def write_to_log_file(log_file: str, files: List, filename: str):

    setup_logging(
        console_log_actived=False,
        console_log_filter=None,
        console_out_level=logging.DEBUG,
        log_file=log_file,
    )

    logging.getLogger().warning(
        "{}\n\n{} FILE CONVERSION EB \n{}\n".format(
            "_" * 79, "\t" * 8, "_" * 79)
    )

    logging.getLogger().debug(
        "Started converting:\n {}\n".format(
            datetime.datetime.now().strftime("%Y, %d.%b - %Hh:%Mmin")
        )
    )

    logging.getLogger().debug(
        "Following files found:\n {}\n".format([f.stem for f in files])
    )

    # ////////////////////////////////////////////////////////// FETCH
    logging.getLogger().warning(
        "{}\n\n{} Province: {} - File: {}\n\n{}".format(
            "/" * 79, "\t" * 6, filename.split("_")[1], filename, "/" * 79
        )
    )
