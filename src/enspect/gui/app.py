import dash
import dash_bootstrap_components as dbc

# /////////////////////////////////////////////////////////////////////// APP

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.SUPERHERO],
)

app.config.suppress_callback_exceptions = True
app.title = "balchartpy"
server = app.server
