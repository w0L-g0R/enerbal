import os

import pytest
from enspect.paths import file_paths


@pytest.mark.dependency()
def test_stats(
    test_data_instance,
    test_dataset,
    test_provinces,
    test_stats_workbook,
    test_write_to_xlsx,
):

    years = list(range(2012, 2017))

    test_data_instance.create(
        years=years,
        provinces=test_provinces,
        file=file_paths["pickle_liv_space"],
        is_stat=True,
    )

    print("test_data_instance: ", test_data_instance)
    test_dataset.add_data(data=test_data_instance)

    test_data_objects = [_data for _data in test_dataset.objects.filter(is_stat=True)]

    # for test_data_object in test_data_objects:
    #     test_data_object.columns_to_percentages = True

    test_write_to_xlsx(
        wb=test_stats_workbook, data_objects=test_data_objects, sheet_name="AREA",
    )


# @pytest.mark.dependency(depends=["test_stats"])
# def test_launch(test_launch_xlsx, test_stats_workbook):

#     test_launch_xlsx(wb=test_stats_workbook)
