from dataclasses import dataclass, field
import pandas as pd
from datetime import datetime
from typing import List, Dict
from pprint import pprint, pformat
from enspect.models.utils import add_row_total, add_col_total

# NOTE:code_source=https://stackoverflow.com/questions/58309731/doing-class-objects-filter-pattern-in-python
IDX = pd.IndexSlice

from openpyxl.utils.dataframe import dataframe_to_rows, expand_levels


@dataclass
class Data:

    # Shown as chart name
    name: str = None
    _id: str = None

    # # Pickle file name
    # file: str = None

    # Origin of the data
    source: str = None
    created: datetime = datetime.now().strftime("%d_%m_%y_%Hh%Mm")

    # Values
    frame: pd.DataFrame = None
    # shares_over_rows: pd.DataFrame = None
    # shares_over_columns: pd.DataFrame = None
    # indexed: Dict = None
    unit: str = None

    # Data type
    balance_aggregates: List = None  # Balance aggregate e.g. "Importe"
    energy_sources: List = None  # e.g. "Steinkohle"
    energy_aggregates: List = None  # e.g. "Fossil-Fest"
    usage_categories: List = None
    emittents: List = None
    years: List = None
    provinces: List = None
    stats: List = None

    # Data classification
    per_balance_aggregate: bool = False
    per_energy_source: bool = False
    per_energy_aggregate: bool = False
    per_years: bool = False
    show_source_values_for_energy_aggregates: bool = False

    # Chart specific
    has_overlay: bool = False
    overlays: List = field(default_factory=lambda: [])

    # KPI
    is_KPI: bool = False
    denominator: pd.DataFrame = None
    numerator: pd.DataFrame = None

    # Search pattern
    order: str = None

    # @ order:
    # per_years: str
    # per_energy_sources: str
    # per_energy_aggregates: str
    # per_usage_categories: str
    # per_emittents: str

    def convert(self, *args):

        # TODO: Link to settings
        conversion = {
            "mwh_2_gwh": 0.001,
            "gwh_2_tj": (1 / 0.27778),
            "tj_2_pj": 0.001,
            "gwh_2_mwh": 1000,
            "tj_2_gwh": 0.27778,
            "tj_2_twh": 0.27778 / 1000,
            "pj_2_tj": 1000,
        }

        self.frame *= conversion[args]
        self.unit = args[0].split("_")[-1]

        return

    def __repr__(self):
        return pformat(
            dict(
                name=self.name,
                _id=self._id,
                frame=self.frame,
                unit=self.unit,
                balance_aggregates=self.balance_aggregates,
                energy_sources=self.energy_sources,
                energy_aggregates=self.energy_aggregates,
                years=self.years,
                provinces=self.provinces,
                per_balance_aggregate=self.per_balance_aggregate,
                per_energy_source=self.per_energy_source,
                per_energy_aggregate=self.per_energy_aggregate,
                per_years=self.per_years,
                show_source_values_for_energy_aggregates=self.show_source_values_for_energy_aggregates,
            )
        )

    def __eq__(self, other):
        return self._id == other._id

    def xlsx_formatted(self):

        dfs = {}
        # if self.per_balance_aggregate:

        #     for year in self.years:
        #         dfs[year] = {}

        #         for energy_source in self.energy_sources:
        #             print("energy_source: ", energy_source)

        #             df = (
        #                 self.frame.loc[IDX[:], IDX[year, energy_source, :,]]
        #                 .swaplevel(0, 1, axis=1)
        #                 .stack([0, 1])
        #                 # .sort_values(["ET_AGG",])
        #             )

        #             df = add_col_total(df=df)

        #             df.reset_index(inplace=True)

        #             # df_sums = df.groupby("ET").get_group("SUM")
        #             df.drop(["ET", "YEAR"], inplace=True, axis=1)
        #             df = add_row_total(df=df)
        #             df.iloc[-1, 0] = "SUM"

        #             dfs[year][energy_source] = df

        # All energy aggregates
        # elif self.per_energy_aggregate:

        #     for year in self.years:
        #         dfs[year] = {}

        #         for aggregate in self.balance_aggregates:

        #             df = (
        #                 self.frame.loc[IDX[:, :], IDX[year, aggregate, :,]]
        #                 .swaplevel(0, 1, axis=1)
        #                 .stack([0, 1])
        #                 # .sort_values(["ET_AGG",])
        #             )

        #             df = add_col_total(df=df)

        #             df.reset_index(inplace=True)

        #             df_sums = df.groupby("ET").get_group("SUM")
        #             df_sums.drop(["ET", "IDX_0", "YEAR"], inplace=True, axis=1)
        #             df_sums = add_row_total(df=df_sums)
        #             df_sums.iloc[-1, 0] = "SUM"

        #             _dfs = []
        #             _dfs.append(df_sums)

        #             df.drop(["IDX_0", "YEAR"], inplace=True, axis=1)
        #             _dfs.append(df)

        #             dfs[year][aggregate] = _dfs

        # # All years
        # else:
        #     for energy_source in self.energy_sources:

        #         dfs[energy_source] = {}

        #         for aggregate in self.balance_aggregates:

        #             df = (
        #                 self.frame.loc[IDX[:], IDX[energy_source, aggregate, :],]
        #                 .swaplevel(0, 1, axis=1)
        #                 .stack([0, 1])
        #                 .sort_values(["ET", "YEAR"])
        #             )

        #             df.reset_index(inplace=True)

        #             dfs[energy_source][aggregate] = df
        #     # data

        # return dfs


class UnknownOperator(Exception):
    """ custom exception """


class FilterData:
    def __init__(self, data):
        self.data = data

    # def __repr__(self):
    #     return [x.name for x in self.data]

    def _filter_step(self, key, value, data):
        if not "__" in key:
            return (entry for entry in data if getattr(entry, key) == value)
        else:
            key, operator = key.split("__")
            if operator == "gt":  # greater than
                return (entry for entry in data if getattr(entry, key) > value)
            elif operator == "lt":  # less than
                return (entry for entry in data if getattr(entry, key) < value)
            elif operator == "startswith":  # starts with
                return (
                    entry for entry in data if getattr(entry, key).startswith(value)
                )
            elif operator == "in":  # is in
                return (entry for entry in data if getattr(entry, key) in value)
            elif operator == "contains":  # contains
                return (entry for entry in data if value in getattr(entry, key))
            else:
                raise UnknownOperator("operator %s is unknown" % operator)

    def _exclude_step(self, key, value, data):
        if not "__" in key:
            return (entry for entry in data if getattr(entry, key) != value)
        else:
            key, operator = key.split("__")
            if operator == "gt":  # greater than
                return (entry for entry in data if getattr(entry, key) <= value)
            elif operator == "lt":  # less than
                return (entry for entry in data if getattr(entry, key) >= value)
            elif operator == "startswith":  # starts with
                return (
                    entry for entry in data if not getattr(entry, key).startswith(value)
                )
            elif operator == "in":  # starts with
                return (entry for entry in data if getattr(entry, key) not in value)
            elif operator == "is_kpi":  # starts with
                return (entry for entry in data if getattr(entry, key) not in value)
            else:
                raise UnknownOperator("operator %s is unknown" % operator)

    def filter(self, **kwargs):
        data = (entry for entry in self.data)
        for key, value in kwargs.items():
            data = self._filter_step(key, value, data)

        return FilterData(data)

    def exclude(self, **kwargs):
        data = (entry for entry in self.data)
        for key, value in kwargs.items():
            data = self._exclude_step(key, value, data)

        return FilterData(data)

    def all(self):
        return FilterData(self.data)

    def count(self):
        cnt = 0
        for cnt, entry in enumerate(self.data, 1):
            pass
        return cnt

    def __iter__(self):
        for entry in self.data:
            yield entry

    # def __repr__(self):
    #     return [entry for entry in self.data]


# make it even more look like django managers / filters


# DATA = [
#     Data(
#         name="BTU_ONE_12",
#         unit="TJ",
#         years=[2017, 2018],
#         _type="per_years"
#     ),
#     Data(
#         name="BTU_TWO_222",
#         unit="TJ",
#         years=[2017, 2018],
#         _type="per_sectors"
#     ),
#     Data(
#         name="BTU_ONE_123",
#         unit="GWh",
#         years=[2000],
#         _type="per_years"
#     )
# ]

# fdata = FilterData(DATA)

# p = [v.unit for v in fdata.filter(name="BTU_ONE_12")]
# print('p: ', p)

# assert [v["id"] for v in fdata.filter(color="red")] == [1, 3]
# assert [v["id"] for v in fdata.filter(id__gt=2)] == [3, 4, 5, 6]
# assert [v["id"] for v in fdata.filter(color__startswith="gr")] == [5, 6]

# fmgr = DataManager(DATA)

# p = [v.name for v in fmgr.objects.filter(unit="TJ")]
# p = [v.name for v in fmgr.objects.all()]
# print('p: ', p)

# assert [v["id"] for v in fmgr.objects.filter(name="paul")] == [3]
# assert [v["id"] for v in fmgr.objects.filter(color="red")] == [1, 3]
# assert [v["id"] for v in fmgr.objects.filter(id__gt=2)] == [3, 4, 5, 6]
# assert [v["id"] for v in fmgr.objects.filter(color__startswith="gr")] == [5, 6]
# assert [v["id"] for v in fmgr.objects.filter(
#     color__startswith="gr", id__lt=6)] == [5]
# assert [v["id"] for v in fmgr.objects.filter(
#     color__startswith="gr", id__lt=6)] == [5]

# assert [v["id"] for v in fmgr.objects.filter(
#     color__startswith="gr").filter(id__lt=6)] == [5]

# assert fmgr.objects.filter(
#     color__startswith="gr").filter(id__lt=6).count() == 1
# assert fmgr.objects.filter(id__gt=2).count() == 4
# assert fmgr.objects.count() == 6
# assert [v["id"] for v in fmgr.objects.all()] == list(range(1, 7))
