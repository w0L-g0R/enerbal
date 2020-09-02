# /////////////////////////////////////////////////////////////////////// VIEWS
from gui.assets.logos import setup_logo_A, setup_logo_B

# from gui.callbacks.dropdowns.on_reset import create_on_reset_dropdowns
# //////////////////////////////////////////////////////////////// CB DROPDOWNS
from gui.callbacks.dropdowns.on_select_eev import create_on_select_eev_dropdowns
from gui.callbacks.dropdowns.on_select_renewables import (
    create_on_select_renewables_dropdowns,
)

# ////////////////////////////////////////////////////////////////// CB SELECTS
# from gui.callbacks.on_select_index_year import create_on_select_index_year
from gui.callbacks.on_select_aggregate import create_on_select_aggregate
from gui.callbacks.on_setup import create_on_setup

# ////////////////////////////////////////////////////////////////// CB UPDATES
from gui.callbacks.on_update import create_on_update
from gui.callbacks.plots.on_plot import create_on_plot

# ////////////////////////////////////////////////////////////////// CB ROUTING
from gui.callbacks.routing.on_graph_tab_change import create_on_graph_tab_change
from gui.callbacks.routing.on_switch_eb_data_section import (
    create_on_switch_eb_data_section,
)
from gui.views.control import create_control_box_layout
from gui.views.graph import create_graph_box_layout
from gui.views.header import layout as header
from gui.views.provinces import layout as provinces
from gui.views.setup.view import create_setup_layout
from gui.views.table import table
from gui.views.years import layout as years

# from gui.callbacks.on_switch_axes import create_on_switch_axes
# from gui.callbacks.on_update_graph import create_on_update_graph

# from gui.callbacks.on_select_aggregate import create_on_select_aggregate
# from gui.callbacks.on_select_xaxis import create_on_select_xaxis
# from gui.callbacks.on_update_graph import create_on_update_graph


# from gui.callbacks.routing.on_click_update import create_on_click_update


setup_A = create_setup_layout(graph_id="graph-A", title=setup_logo_A)
setup_B = create_setup_layout(graph_id="graph-B", title=setup_logo_B)
# setup_C = create_setup_layout(
#     graph_id="graph-C", title=logo_B)

graph_A = create_graph_box_layout(graph_id="graph-A")
graph_B = create_graph_box_layout(graph_id="graph-B")
# graph_C = create_graph_box_layout(graph_id="graph-C")

control_A = create_control_box_layout(graph_id="graph-A")
control_B = create_control_box_layout(graph_id="graph-B")

views = {
    "years": years,
    "header": header,
    "provinces": provinces,
    "setup_A": setup_A,
    "setup_B": setup_B,
    # "setup_C": setup_C,
    "graph_A": graph_A,
    "graph_B": graph_B,
    "control_A": control_A,
    "control_B": control_B,
    # "graph_C": graph_C,
    "table": table,
}


def register_callbacks():

    for graph in ["graph-A", "graph-B"]:

        create_on_graph_tab_change(graph_id=graph)
        create_on_setup(graph_id=graph)
        create_on_select_eev_dropdowns(graph_id=graph)
        create_on_plot(graph_id=graph)
        # create_on_switch_eb_data_section(graph_id=graph)
        create_on_select_renewables_dropdowns(graph_id=graph)
        # create_on_switch_axes(graph_id=graph)
        # create_on_select_index_year(graph_id=graph)
        create_on_select_aggregate(graph_id=graph)
        create_on_update(graph_id=graph)

    # create_on_update_data_table(graph_id=graph)
