import dash
import dash_bootstrap_components as dbc
from plotly.graph_objects import Figure

from .src.dashboard import Dashboard
from dash import Input, Output, State, callback, dcc, html

dash.register_page(__name__)

sex_dashboard_field = html.Div(
    [
        dbc.Label("Sex", html_for="sex-field-dashboard"),
        dcc.Dropdown(
            id="sex-field-dashboard",
            options=[
                {"label": "Male", "value": "Male"},
                {"label": "Female", "value": "Female"},
            ],
            placeholder="Select sex",
            multi=True,
        ),
    ],
    className="mb-3",
)

pheno_dashboard_field = html.Div(
    [
        dbc.Label("Phenotype", html_for="pheno-field-dashboard"),
        dcc.Dropdown(
            id="pheno-field-dashboard",
            options=[
                {"label": "Healthy samples", "value": "Healthy sample"},
                {"label": "Melanoma samples", "value": "Melanoma"},
            ],
            placeholder="Select phenotype",
            multi=True,
        ),
    ],
    className="mb-3",
)

tissue_dashboard_field = html.Div(
    [
        dbc.Label("Tissue", html_for="tissue-field-dashboard"),
        dcc.Dropdown(
            id="tissue-field-dashboard",
            options=[
                {"label": "Whole blood", "value": "Blood"},
                {"label": "Buccal swab", "value": "Swab"},
            ],
            placeholder="Select tissue",
            multi=True,
        ),
    ],
    className="mb-3",
)

age_dashboard_field = html.Div(
    [
        dbc.Label("Age", html_for="age-field-dashboard"),
        dcc.RangeSlider(
            id="age-field-dashboard",
            min=0,
            max=100,
            value=[45, 55],
            allowCross=False,
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
        ),
    ],
    className="mb-3",
)

form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Col(sex_dashboard_field),
                dbc.Col(pheno_dashboard_field),
                dbc.Col(tissue_dashboard_field),
                dbc.Col(age_dashboard_field),
            ]
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Submit", id="submit-dashboard", className="button-interact")
            )
        ),
    ],
    className="custom-input-form",
)

layout = dbc.Container(
    [
        dbc.Row(dbc.Alert("", id="alert-dashboard", is_open=False, duration=4000)),
        form,
        dbc.Collapse(
            [
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(id="plot-dashboard-sex")),
                        dbc.Col(dcc.Graph(id="plot-dashboard-age")),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(id="plot-dashboard-tissue")),
                        dbc.Col(dcc.Graph(id="plot-dashboard-pheno")),
                    ]
                ),
            ],
            is_open=False,
            id="dashboard-plot-area",
        ),
    ],
    fluid=True,
    className="main-container",
)


@callback(
    Output("alert-dashboard", "children"),
    Output("alert-dashboard", "is_open"),
    State("sex-field-dashboard", "value"),
    State("pheno-field-dashboard", "value"),
    State("tissue-field-dashboard", "value"),
    Input("submit-dashboard", "n_clicks"),
    prevent_initial_call=True,
)
def validate_sex(sex: list[str], pheno: list[str], tissue: list[str], _) -> ...:
    if not sex or not pheno or not tissue:
        return "Please fill missing field(s)", True
    return "", False


@callback(
    Output("dashboard-plot-area", "is_open"),
    Output("plot-dashboard-sex", "figure"),
    Output("plot-dashboard-age", "figure"),
    Output("plot-dashboard-tissue", "figure"),
    Output("plot-dashboard-pheno", "figure"),
    State("sex-field-dashboard", "value"),
    State("age-field-dashboard", "value"),
    State("tissue-field-dashboard", "value"),
    State("pheno-field-dashboard", "value"),
    Input("submit-dashboard", "n_clicks"),
    prevent_initial_call=True,
)
def generate_content(
    sex: list[str], age: list[int], tissue: list[str], pheno: list[str], _
) -> tuple[Figure, ...]:
    if sex and age and tissue and pheno:
        d = Dashboard(sex=sex, age=age, tissue=tissue, pheno=pheno)
        d.load_data()

        d.bar_plot("Sex")
        d.bar_plot("Tissue")
        d.bar_plot("Phenotype")
        d.box_plot("Age")

        figures = d.get_figures
        return (
            True,
            figures["Sex"],
            figures["Age"],
            figures["Tissue"],
            figures["Phenotype"],
        )
    return False, {}, {}, {}, {}
