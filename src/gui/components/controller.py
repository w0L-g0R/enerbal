# /////////////////////////////////////////////////////////////////////// VIEWS

from gui.components.callbacks.on_click_update import create_on_click_update
from gui.components.callbacks.on_graph_tab_change import create_on_graph_tab_change
from gui.components.views.box_graph import box_A, box_B
from gui.components.views.box_table import box_table
from gui.components.views.setup import setup_A, setup_B
from gui.components.views.header import layout as header
from gui.components.views.provinces import layout as provinces
from gui.components.views.years import layout as years

# /////////////////////////////////////////////////////////////////// CALLBACKS
from gui.components.callbacks.on_update_graph import create_on_update_graph

from gui.components.callbacks.on_update_data_table import create_on_update_data_table

from gui.components.callbacks.on_switch_eb_data_section import create_on_switch_eb_data_section

from gui.components.callbacks.on_select_eev_dropdowns import create_on_select_eev_dropdowns

from gui.components.callbacks.on_select_graph_dropdowns import create_on_select_graph_dropdowns

from gui.components.callbacks.on_select_renewables_dropdowns import create_on_select_renewables_dropdowns


views = {
    "years": years,
    "header": header,
    "provinces": provinces,
    "setup_A": setup_A,
    "setup_B": setup_B,
    "box_A": box_A,
    "box_B": box_B,
    "box_table": box_table,
}


def register_callbacks():

    for graph in ["graph-A", "graph-B"]:

        create_on_graph_tab_change(graph_id=graph)
        create_on_update_graph(graph_id=graph)
        create_on_click_update(graph_id=graph)
        create_on_select_eev_dropdowns(graph_id=graph)
        create_on_select_graph_dropdowns(graph_id=graph)
        create_on_switch_eb_data_section(graph_id=graph)
        create_on_select_renewables_dropdowns(graph_id=graph)

    create_on_update_data_table(graph_id=graph)
