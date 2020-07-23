from settings import renewables_indices
from settings import eev_indices
import inspect
import os
from typing import List

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from gui.app import app
from gui.utils import show_callback_context
from dash import no_update

IDX = pd.IndexSlice


def callback_on_select_renewables_dropdown(
    # setup_data: bool = True,
    idx_0: object = no_update,
    idx_1: object = no_update,
    idx_2: object = no_update,
    idx_0_disabled: object = no_update,
    idx_1_disabled: object = no_update,
    idx_2_disabled: object = no_update,
):

    return [
        # setup_data,
        idx_0,
        idx_1,
        idx_2,
        idx_0_disabled,
        idx_1_disabled,
        idx_2_disabled,
    ]


def create_on_select_renewables_dropdowns(graph_id: str):
    @app.callback(
        [
            Output(f"idx-res-0-{graph_id}", "options"),
            Output(f"idx-res-1-{graph_id}", "options"),
            Output(f"idx-res-2-{graph_id}", "options"),
            Output(f"idx-res-0-{graph_id}", "disabled"),
            Output(f"idx-res-1-{graph_id}", "disabled"),
            Output(f"idx-res-2-{graph_id}", "disabled"),

        ],
        [
            Input(f"idx-res-0-{graph_id}", "value"),
            Input(f"idx-res-1-{graph_id}", "value"),
            Input(f"idx-res-2-{graph_id}", "value"),
        ],
    )
    def on_select_renewables_dropdowns(
        idx_0_value: str,
        idx_1_value: str,
        idx_2_value: str,
    ):

        show_callback_context(
            verbose=True,
            func_name=inspect.stack()[0][3],
            file_name=inspect.stack()[0][1].rsplit(os.sep, 1)[-1].upper(),
        )
        # Get callback information to define the triggered input
        ctx = callback_context
        triggered = ctx.triggered
        states = ctx.states
        inputs = ctx.inputs

        if triggered:

            # Store the selected dropdown item in a variable
            triggered_prop_id = triggered[0]["prop_id"]
            triggered_value = triggered[0]["value"]

            only_total = [
                {"label": "Gesamt", "value": "Gesamt"},
            ]

            ee_verbrauch = [
                "Gesamt",
                "Scheitholz",
                "Holzbasierte Energieträger",
                "Sonstige Biogene fest",
                "Biogas",
                "Biotreibstoffe nachhaltig pur",
                "Biotreibstoffe nachhaltig beigemengt",
                "Laugen",
                "Müll erneuerbar",
                "Solarwärme",
                "Geothermie",
                "Umgebungswärme",

            ]

            ee_produktion = [
                "Gesamt",
                "Wasserkraft ohne Pumpe normalisiert (GWh)",
                "Wasserkraft mit Pumpe normalisiert (GWh)",
                "Primärstrom Wind normalisiert (GWh)",
                "Primärstrom Fotovoltaik (GWh)",
                "Primärstrom Geothermie (GWh)",
                "Sekundärstrom erneuerbar (GWh)",
                "Gesamtstrom erneuerbar (GWh)",
            ]

            ee_fernwärme = [
                "Gesamt",
                "Müll erneuerbar",
                "Holzbasierte Energieträger",
                "Biogas",
                "Sonstige Biogene flüssig",
                "Laugen",
                "Sonstige Biogene fest",
                "Geothemie",

            ]
            ee_verbrauch = [{"label": x, "value": x} for x in ee_verbrauch]
            ee_produktion = [{"label": x, "value": x} for x in ee_produktion]
            ee_fernwärme = [{"label": x, "value": x} for x in ee_fernwärme]

            # print()
            print('idx_0_value: ', idx_0_value)

            if "Energetischer Endverbrauch Erneuerbare (TJ)" == idx_0_value:

                return callback_on_select_renewables_dropdown(
                    idx_1_disabled=False,
                    idx_2_disabled=True,
                    idx_1=ee_verbrauch,
                    idx_2=only_total,
                )

            if "Elektrische Energie Produktion erneuerbar (TJ)" == idx_0_value:

                if "Wasserkraft ohne Pumpe normalisiert (GWh)" == idx_1_value:

                    categories = ["Installierte Kapazität ohne Pumpe (MW)",
                                  "Ausnutzungsdauer (h)",
                                  "Primärstrom Wasser real (GWh)",
                                  "Gesamt",
                                  ]

                elif "Wasserkraft mit Pumpe normalisiert (GWh)" in idx_1_value:

                    categories = ["Installierte Kapazität mit Pumpe (MW)",
                                  "Erzeugung aus natürlichem Zufluß (GWh)",
                                  "Ausnutzungsdauer (h)",
                                  "Primärstrom Wasser real (GWh)",
                                  "Erzeugung aus gepumptem Zufluß (GWh)",
                                  "Gesamt",

                                  ]

                elif "Primärstrom Wind normalisiert (GWh)" in idx_1_value:

                    categories = ["Installierte Kapazität real (MW)",
                                  "Installierte Kapazität normalisiert (MW)",
                                  "Primärstrom Wind real (GWh)",
                                  "Gesamt",
                                  ]

                elif "Sekundärstrom erneuerbar (GWh)" == idx_1_value:

                    categories = [
                        "Müll erneuerbar",
                        "Holz-basiert",
                        "Biogas",
                        "Biogene flüssig",
                        "Laugen",
                        "sonst Biogene fest",
                        "Gesamt",
                    ]

                else:
                    categories = [
                        "Gesamt",
                    ]

                    return callback_on_select_renewables_dropdown(
                        idx_1_disabled=False,
                        idx_2_disabled=True,
                        idx_1=ee_produktion,
                        idx_2=[
                            {"label": x, "value": x} for x in categories
                        ],
                    )

                return callback_on_select_renewables_dropdown(
                    idx_1_disabled=False,
                    idx_2_disabled=False,
                    idx_1=ee_produktion,
                    idx_2=[
                        {"label": x, "value": x} for x in categories
                    ],
                )

            if "Fernwärme" in idx_0_value:

                return callback_on_select_renewables_dropdown(
                    idx_1_disabled=False,
                    idx_2_disabled=True,
                    idx_1=ee_fernwärme,
                    idx_2=only_total,
                )
            else:

                return callback_on_select_renewables_dropdown(
                    idx_1_disabled=True,
                    idx_2_disabled=True,
                    idx_1=only_total,
                    idx_2=only_total,
                )

        else:
            raise PreventUpdate
