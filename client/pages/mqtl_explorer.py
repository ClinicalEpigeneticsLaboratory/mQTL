import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, callback, dcc, html
from plotly.io import from_json
from dash import dash_table
from .src.mQTL_client import mqtlClient

dash.register_page(__name__)

sex_explorer_field = html.Div(
    [
        dbc.Label("Sex", html_for="sex-field-explorer"),
        dcc.Dropdown(
            id="sex-field-explorer",
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

pheno_explorer_field = html.Div(
    [
        dbc.Label("Phenotype", html_for="pheno-field-explorer"),
        dcc.Dropdown(
            id="pheno-field-explorer",
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

tissue_explorer_field = html.Div(
    [
        dbc.Label("Tissue", html_for="tissue-field-explorer"),
        dcc.Dropdown(
            id="tissue-field-explorer",
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

age_explorer_field = html.Div(
    [
        dbc.Label("Age", html_for="age-field-explorer"),
        dcc.RangeSlider(
            id="age-field-explorer",
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
                dbc.Col(sex_explorer_field),
                dbc.Col(pheno_explorer_field),
                dbc.Col(tissue_explorer_field),
                dbc.Col(age_explorer_field),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("rs"),
                            dbc.Input(placeholder="rsID", id="rsID-field-explorer"),
                        ],
                        className="mb-3",
                    )
                ),
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("cg"),
                            dbc.Input(placeholder="cpgID", id="cpgID-field-explorer"),
                        ],
                        className="mb-3",
                    )
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Submit", id="submit-explorer", className="button-interact")
            )
        ),
    ],
    className="custom-input-form",
)

layout = dbc.Container(
    [
        dbc.Row(dbc.Alert("", id="alert-mqtl-explorer", is_open=False, duration=4000)),
        dbc.Row(
            dbc.Alert("", id="status-mqtl-explorer", is_open=False, color="danger")
        ),
        dcc.Interval(
            id="intervals-mqtl-explorer", interval=1000, n_intervals=0, disabled=True
        ),
        form,
        dbc.Collapse(
            [
                dbc.Row(
                    [
                        dbc.Col(dbc.Container(id="tableA-mQTL-explorer")),
                        dbc.Col(dbc.Container(id="tableB-mQTL-explorer")),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(id="plot-mQTL-explorer"),
                            style={"margin-bottom": "10px"},
                        )
                    ]
                ),
            ],
            is_open=False,
            id="mqtl-explorer-plot-area",
        ),
        dcc.Store(id="mqtl-client-task", storage_type="memory"),
        dcc.Store(id="mqtl-client-results", storage_type="memory"),
    ],
    fluid=True,
    className="main-container",
)


@callback(
    Output("alert-mqtl-explorer", "children"),
    Output("alert-mqtl-explorer", "is_open"),
    State("sex-field-explorer", "value"),
    State("pheno-field-explorer", "value"),
    State("tissue-field-explorer", "value"),
    State("rsID-field-explorer", "value"),
    State("cpgID-field-explorer", "value"),
    Input("submit-explorer", "n_clicks"),
    prevent_initial_call=True,
)
def validate_sex(
    sex: list[str], pheno: list[str], tissue: list[str], rs: str, cpg: str, _
) -> ...:
    if not sex or not pheno or not tissue or not rs or not cpg:
        return "Please fill missing field(s)", True

    if not rs.startswith("rs") or not cpg.startswith("cg"):
        return "Make sure that rsID starts with 'rs' and cpgID starts with 'cg'", True

    return dash.no_update


@callback(
    Output("submit-explorer", "disabled", allow_duplicate=True),
    Output("mqtl-client-task", "data", allow_duplicate=True),
    Output("intervals-mqtl-explorer", "disabled", allow_duplicate=True),
    State("sex-field-explorer", "value"),
    State("pheno-field-explorer", "value"),
    State("tissue-field-explorer", "value"),
    State("age-field-explorer", "value"),
    State("rsID-field-explorer", "value"),
    State("cpgID-field-explorer", "value"),
    Input("submit-explorer", "n_clicks"),
    prevent_initial_call=True,
)
def start_analysis(
    sex: list[str],
    pheno: list[str],
    tissue: list[str],
    age: list[int],
    rs: str,
    cpg: str,
    _,
) -> ...:
    if sex and pheno and tissue and age and rs and cpg:
        if rs.startswith("rs") and cpg.startswith("cg"):
            mqtl = mqtlClient(
                sex=sex, pheno=pheno, tissue=tissue, age=age, rs=rs, cpg=cpg
            )
            mqtl.get_samples_names()
            mqtl.start_analysis()

            return True, mqtl.task_id, False

    return dash.no_update


@callback(
    Output("intervals-mqtl-explorer", "disabled"),
    Output("status-mqtl-explorer", "children"),
    Output("status-mqtl-explorer", "is_open"),
    Output("mqtl-client-results", "data"),
    Output("mqtl-client-task", "data"),
    Input("mqtl-client-task", "data"),
    Input("intervals-mqtl-explorer", "n_intervals"),
    prevent_initial_call=True,
)
def check_task_status(task_id: str, _):
    if task_id:
        result = mqtlClient.get_result(task_id)

        if result["Status"] == "SUCCESS":
            return (
                True,
                f"Task {result['TaskID']} has status --> SUCCESS",
                True,
                result["Result"],
                None,
            )

        else:
            return (
                False,
                f"New task --> {result['TaskID']} has status {result['Status']}. Please do not close your browser",
                True,
                None,
                task_id,
            )

    return dash.no_update


@callback(
    Output("submit-explorer", "disabled"),
    Output("tableA-mQTL-explorer", "children"),
    Output("tableB-mQTL-explorer", "children"),
    Output("plot-mQTL-explorer", "figure"),
    Output("mqtl-explorer-plot-area", "is_open"),
    Input("mqtl-client-results", "data"),
    prevent_initial_call=True,
)
def render_output(data: dict) -> ...:
    if data:
        table_a, table_b, plot = data["tableA"], data["tableB"], data["Plot"]
        table_a = pd.DataFrame.from_dict(table_a)
        table_b = pd.DataFrame.from_dict(table_b)

        table_a = dash_table.DataTable(
            data=table_a.to_dict("records"),
            columns=[{"name": "", "id": str(i)} for i in table_a.columns],
            style_table={
                "overflowX": "auto",
                "overflowY": "auto",
                "width": "100%",
                "minWidth": "100%",
                "maxWidth": "100%",
                "padding": "1%",
            },
            export_format="csv",
            virtualization=False,
            style_data={"whiteSpace": "normal", "height": "auto"},
        )

        table_b = dash_table.DataTable(
            data=table_b.to_dict("records"),
            columns=[{"name": "", "id": str(i)} for i in table_b.columns],
            style_table={
                "overflowX": "auto",
                "overflowY": "auto",
                "width": "100%",
                "minWidth": "100%",
                "maxWidth": "100%",
                "padding": "1%",
            },
            export_format="csv",
            virtualization=False,
            style_data={"whiteSpace": "normal", "height": "auto"},
        )

        return False, table_a, table_a, from_json(plot), True

    return dash.no_update
