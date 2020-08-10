from dataclasses import dataclass, field
import pandas as pd
from datetime import datetime
from typing import List, Dict

# NOTE:code_source=https://stackoverflow.com/questions/58309731/doing-class-objects-filter-pattern-in-python


@dataclass
class Data:

    # Shown as chart name
    title: str = "Ein toller plot"
    name: str = None
    # Pickle file name
    file: str = None
    # Origin of the data
    source: str = None
    created: datetime = datetime.now().strftime("%d_%m_%y_%Hh%Mm")
    unit: str = None
    # Values
    frame: pd.DataFrame = None
    shares_over_rows: pd.DataFrame = None
    shares_over_columns: pd.DataFrame = None
    indexed: Dict = None
    # Data sub categories
    aggregate: str = None
    energy_source: str = None
    provinces: List = None
    years: List = None
    usage_categories: List = None
    emittents: List = None
    sectors: List = None
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
    # per_sectors: str
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

    # def get_data(self, *args):
    #     if "absolute" in args:
    #         return self.absolute
    #     if "shares_over_rows" in args:
    #         return self.shares_over_rows
    #     if "shares_over_columns" in args:
    #         return self.shares_over_columns
    #     if "denominator" in args:
    #         return self.denominator
    #     if "numerator" in args:
    #         return self.numerator


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
                return (entry for entry in data if getattr(entry, key).startswith(value))
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
                return (entry for entry in data if not getattr(entry, key).startswith(value))
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
