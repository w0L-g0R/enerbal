import pytest


# def test_add_sources_for_each_agg_and_year(
#     test_dataset,
#     test_workbook,
#     test_provinces,
#     test_main_energy_aggregates,
#     test_balance_aggregates_index_0,
# ):
#     years = [2000, 2018]

#     test_dataset.add_eb_data(
#         energy_sources=test_main_energy_aggregates,
#         balance_aggregates=test_balance_aggregates_index_0,
#         years=years,
#         provinces=test_provinces,
#         conversion="TJ_2_TWh",
#         per="sources_for_each_agg_and_year"
#         # 1) sources_for_each_agg_and_year
#         # 2) aggs_for_each_source_and_year
#         # 3) agg_and_source_for_all_years
#     )

#     data_objects = [
#         _data
#         for _data in test_dataset.objects.filter(
#             # order="per_sector",
#             # aggregate__in=["Bruttoinlandsverbrauch", "Importe"],
#             # is_KPI=False
#         )
#     ]

#     data_object_names = [
#         _data.name
#         for _data in test_dataset.objects.filter(
#             # order="per_sector",
#             # aggregate__in=["Bruttoinlandsverbrauch", "Importe"],
#             # is_KPI=False
#         )
#     ]

#     test_workbook.add_sheets(sheets=data_object_names)

#     for data in data_objects:

#         # if data.order == "per_sector":

#         test_workbook.write(data=data, sheet=data.name)
#         # else:
#         #     test_workbook.write(data=data, sheet=data.aggregate)

#     for sheet in test_workbook.book.sheetnames:
#         print("sheet: ", sheet)

#         dimension = test_workbook.book[sheet].calculate_dimension()
#         test_workbook.book[sheet].move_range(dimension, rows=0, cols=10)

#         test_workbook.style(ws=test_workbook.book[sheet])

#     test_workbook.book.save(test_workbook.path)
#     test_workbook.launch()


def test_aggs_for_each_source_and_year(
    test_dataset,
    test_workbook,
    test_provinces,
    test_main_energy_aggregates,
    test_balance_aggregates_index_0,
):
    years = [2000, 2018]

    test_dataset.add_eb_data(
        energy_sources=test_main_energy_aggregates,
        balance_aggregates=test_balance_aggregates_index_0,
        years=years,
        provinces=test_provinces,
        conversion="TJ_2_TWh",
        per="aggs_for_each_source_and_year"
        # 1) sources_for_each_agg_and_year
        # 2) aggs_for_each_source_and_year
        # 3) agg_and_source_for_all_years
    )

    data_objects = [
        _data
        for _data in test_dataset.objects.filter(
            # order="per_sector",
            # aggregate__in=["Bruttoinlandsverbrauch", "Importe"],
            # is_KPI=False
        )
    ]

    data_object_names = [
        _data.name
        for _data in test_dataset.objects.filter(
            # order="per_sector",
            # aggregate__in=["Bruttoinlandsverbrauch", "Importe"],
            # is_KPI=False
        )
    ]

    test_workbook.add_sheets(sheets=data_object_names)

    for data in data_objects:

        # if data.order == "per_sector":

        test_workbook.write(data=data, sheet=data.name)
        # else:
        #     test_workbook.write(data=data, sheet=data.aggregate)

    for sheet in test_workbook.book.sheetnames:
        print("sheet: ", sheet)

        dimension = test_workbook.book[sheet].calculate_dimension()
        test_workbook.book[sheet].move_range(dimension, rows=0, cols=10)

        test_workbook.style(ws=test_workbook.book[sheet])

    test_workbook.book.save(test_workbook.path)
    # test_workbook.launch()
