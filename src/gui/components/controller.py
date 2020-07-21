# /////////////////////////////////////////////////////////////////////// VIEWS

from gui.components.callbacks.on_click_update import create_on_click_update
from gui.components.callbacks.on_graph_tab_change import create_on_graph_tab_change
from gui.components.views.graph_layout import graph_A_layout, graph_B_layout
from gui.components.views.table_layout import graph_AB_layout
from gui.components.views.graph_setup import graph_setup_A_layout, graph_setup_B_layout
from gui.components.views.header import layout as header_layout
from gui.components.views.provinces import layout as provinces_layout
from gui.components.views.years import layout as years_layout

# /////////////////////////////////////////////////////////////////// CALLBACKS
from gui.components.views.setup import create_eev_graph_view
from gui.components.callbacks.on_update_eev_graph import create_on_update_eev_graph
from gui.components.callbacks.on_update_data_table import create_on_update_data_table

from gui.components.callbacks.on_switch_eb_data_section import create_on_switch_eb_data_section

from gui.components.callbacks.on_select_eev_dropdowns import create_on_select_eev_dropdowns

views = {
    "years_layout": years_layout,
    "header_layout": header_layout,
    "provinces_layout": provinces_layout,
    "graph_setup_A_layout": graph_setup_A_layout,
    "graph_setup_B_layout": graph_setup_B_layout,
    "graph_A_layout": graph_A_layout,
    "graph_B_layout": graph_B_layout,
    "graph_AB_layout": graph_AB_layout,
}


def register_callbacks():

    for graph in ["graph-A", "graph-B"]:

        create_on_graph_tab_change(graph_id=graph)
        create_on_update_eev_graph(graph_id=graph)
        create_on_click_update(graph_id=graph)
        create_on_select_eev_dropdowns(graph_id=graph)
        # create_on_switch_eb_data_section(graph_id=graph)

    create_on_update_data_table(graph_id=graph)
