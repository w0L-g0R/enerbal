import os

import pytest


@pytest.mark.dependency()
def test_res_midx_with_one_balance_aggregate(
    test_dataset,
    test_provinces,
    test_res_workbook,
    test_res_shares,
    test_res_intalled_cap_hydro,
    test_res_usage_time_hydro,
    test_res_generation_run_of_river,
    test_write_to_xlsx
):
    '''
        NOTE:
        Balance aggregates come as list of list, where each inner list contains up to three indices. If only one or two indices (inner list elements) gets provided, missing indices needs to added in the form of "Gesamt" entries.

    '''
    years = list(range(2015, 2019))

    ds = test_dataset

    ds.add_res_data(
        balance_aggregates=[test_res_generation_run_of_river],
        years=years,
        provinces=test_provinces,
    )

    # data_objects = [_data for _data in ds.objects.filter(per_years=True)]
    data_objects = ds.objects

    test_write_to_xlsx(
        wb=test_res_workbook, data_objects=data_objects, sheet_name="RES"
    )


# @pytest.mark.dependency(depends=["test_res_midx_with_one_balance_aggregate"])
# def test_launch(test_launch_xlsx, test_res_workbook):

#     test_launch_xlsx(wb=test_res_workbook)


# @pytest.mark.dependency()
# def test_res_shares(
#     test_dataset,
#     test_provinces,
#     test_res_workbook,
#     test_res_shares,
#     test_res_intalled_cap_hydro,
#     test_res_usage_time_hydro,
#     test_res_generation_run_of_river,
#     test_write_to_xlsx
# ):
#     '''
#         Test shows how to handle missing row index information:

#         NOTE:
#             "test_res_shares" comes as a list containing of only first level row indices.

#     '''
#     years = list(range(2015, 2019))

#     ds = test_dataset

#     ds.add_res_data(
#         balance_aggregates=test_res_shares,
#         years=years,
#         provinces=test_provinces,
#     )

#     # data_objects = [_data for _data in ds.objects.filter(per_years=True)]
#     data_objects = ds.objects

#     test_write_to_xlsx(
#         wb=test_res_workbook, data_objects=data_objects, sheet_name="RES"
#     )


# @pytest.mark.dependency(depends=["test_res_shares"])
# def test_launch(test_launch_xlsx, test_eb_workbook):

#     test_launch_xlsx(wb=test_eb_workbook)
