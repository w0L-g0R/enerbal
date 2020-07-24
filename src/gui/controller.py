# /////////////////////////////////////////////////////////////////////// VIEWS
from gui.callbacks.dropdowns.on_plot import create_on_plot
# from gui.callbacks.dropdowns.on_reset import create_on_reset_dropdowns
# //////////////////////////////////////////////////////////////// CB DROPDOWNS
from gui.callbacks.dropdowns.on_select_eev import (
    create_on_select_eev_dropdowns
)
from gui.callbacks.dropdowns.on_select_renewables import (
    create_on_select_renewables_dropdowns
)
from gui.callbacks.on_setup import create_on_setup

# ////////////////////////////////////////////////////////////////// CB ROUTING
from gui.callbacks.routing.on_graph_tab_change import (
    create_on_graph_tab_change
)
from gui.callbacks.routing.on_switch_eb_data_section import create_on_switch_eb_data_section


# ////////////////////////////////////////////////////////////////// CB SELECTS
from gui.callbacks.on_select_index_year import create_on_select_index_year
from gui.callbacks.on_select_aggregate import create_on_select_aggregate
# from gui.callbacks.on_select_xaxis import create_on_select_xaxis
# from gui.callbacks.on_update_graph import create_on_update_graph


from gui.views.graph import graph_A, graph_B
from gui.views.header import layout as header
from gui.views.provinces import layout as provinces
from gui.views.setup import setup_A, setup_B
from gui.views.table import table
from gui.views.years import layout as years

# from gui.callbacks.routing.on_click_update import create_on_click_update


views = {
    "years": years,
    "header": header,
    "provinces": provinces,
    "setup_A": setup_A,
    "setup_B": setup_B,
    "graph_A": graph_A,
    "graph_B": graph_B,
    "table": table,
}


def register_callbacks():

    for graph in ["graph-A", "graph-B"]:

        create_on_graph_tab_change(graph_id=graph)
        create_on_setup(graph_id=graph)
        create_on_select_eev_dropdowns(graph_id=graph)
        create_on_plot(graph_id=graph)
        create_on_switch_eb_data_section(graph_id=graph)
        create_on_select_renewables_dropdowns(graph_id=graph)
        # create_on_select_xaxis(graph_id=graph)
        create_on_select_index_year(graph_id=graph)
        create_on_select_aggregate(graph_id=graph)
        # create_on_update_graph(graph_id=graph)

    # create_on_update_data_table(graph_id=graph)
