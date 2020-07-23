import dash_core_components as dcc
import dash_html_components as html

stores = html.Div(
    children=[
        dcc.Store(id="graph-A-setup", storage_type="memory"),
        # dcc.Store(id="graph-A", storage_type="memory"),
        dcc.Store(id="graph-B-setup", storage_type="memory"),
        # dcc.Store(id="graph-B", storage_type="memory"),
        # dcc.Store(id="eev-indices", storage_type="memory"),
        dcc.Store(id="graph-A-updates-table", storage_type="memory"),
        dcc.Store(id="graph-B-updates-table", storage_type="memory"),

        dcc.Store(id="graph-A-updates", storage_type="memory"),
        dcc.Store(id="graph-B-updates", storage_type="memory"),



        dcc.Store(id="graph-B-clicked-eev-update", storage_type="memory"),
        dcc.Store(id="graph-A-clicked-nea-update", storage_type="memory"),
        dcc.Store(id="graph-B-clicked-nea-update", storage_type="memory"),
        dcc.Store(id="graph-A-clicked-thg-update", storage_type="memory"),
        dcc.Store(id="graph-B-clicked-thg-update", storage_type="memory"),
        dcc.Store(id="graph-A-clicked-stats-update", storage_type="memory"),
        dcc.Store(id="graph-B-clicked-stats-update", storage_type="memory"),
        dcc.Store(id="graph-A-clicked-sectors-update", storage_type="memory"),
        dcc.Store(id="graph-A-clicked-renewables-update",
                  storage_type="memory"),
        dcc.Store(id="graph-B-clicked-renewables-update",
                  storage_type="memory"),
        dcc.Store(id="graph-B-clicked-sectors-update", storage_type="memory"),
        dcc.Store(id="graph-A-clicked-sector-energy-update",
                  storage_type="memory"),
        dcc.Store(id="graph-B-clicked-sector-energy-update",
                  storage_type="memory"),
    ]
)
