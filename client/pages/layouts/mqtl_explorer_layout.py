from typing import Callable
import dash_bootstrap_components as dbc
from dash import dcc, html


def generate_mqtl_explorer_layout(id_: Callable) -> dbc.Container:
    alerts = dbc.Row(
        [
            dbc.Alert(
                "",
                id=id_("validation-alert"),
                is_open=False,
                duration=5000,
                dismissable=True,
                color="danger",
            ),
            dbc.Row(
                dbc.Alert(
                    "",
                    id=id_("status-alert"),
                    is_open=False,
                    dismissable=True,
                    color="success",
                )
            ),
        ]
    )

    sex_explorer_field = html.Div(
        [
            dbc.Label("Sex", html_for=id_("sex-field")),
            dcc.Dropdown(
                id=id_("sex-field"),
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

    sample_group_explorer_field = html.Div(
        [
            dbc.Label("Sample group", html_for=id_("sample_group-field")),
            dcc.Dropdown(
                id=id_("sample_group-field"),
                options=[
                    {"label": "Healthy samples", "value": "Healthy sample"},
                    {"label": "Melanoma samples", "value": "Melanoma"},
                ],
                placeholder="Select sample group",
                multi=False,
            ),
        ],
        className="mb-3",
    )

    tissue_explorer_field = html.Div(
        [
            dbc.Label("Tissue", html_for=id_("tissue-field")),
            dcc.Dropdown(
                id=id_("tissue-field"),
                options=[
                    {"label": "Whole blood", "value": "Blood"},
                    {"label": "Buccal swab", "value": "Swab"},
                ],
                placeholder="Select tissue",
                multi=False,
            ),
        ],
        className="mb-3",
    )

    age_explorer_field = html.Div(
        [
            dbc.Label("Age", html_for=id_("age-field")),
            dcc.RangeSlider(
                id=id_("age-field"),
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

    pheno_explorer_field = html.Div(
        [
            dbc.Label("Phenotype", html_for=id_("pheno-field")),
            dcc.Dropdown(
                id=id_("pheno-field"),
                options=[
                    {"label": "Epigenetic age", "value": "epigenetic_age"},
                ],
                placeholder="Select Phenotype",
                multi=False,
            ),
        ],
        className="mb-3",
    )

    rs_field = dbc.InputGroup(
        [
            dbc.InputGroupText("rs"),
            dbc.Input(placeholder="rs ID", id=id_("rsID-field")),
        ],
        className="mb-3",
    )

    cpg_field = dbc.InputGroup(
        [
            dbc.InputGroupText("cg"),
            dbc.Input(placeholder="cpg ID", id=id_("cpgID-field")),
        ],
        className="mb-3",
    )

    form = dbc.Form(
        [
            dbc.Row(
                [
                    dbc.Col(sex_explorer_field),
                    dbc.Col(sample_group_explorer_field),
                    dbc.Col(tissue_explorer_field),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(age_explorer_field),
                    dbc.Col(pheno_explorer_field),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(rs_field),
                    dbc.Col(cpg_field),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            "Submit", id=id_("submit"), className="button-interact"
                        ),
                        width="auto",
                        style={"margin": "5px"},
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Example",
                            id=id_("load_example"),
                            className="button-interact",
                        ),
                        width="auto",
                        style={"margin": "5px"},
                    ),
                ],
                className="g-0",
            ),
        ],
        className="custom-input-form",
    )

    output = dbc.Collapse(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Container(id=id_("tableA"))),
                    dbc.Col(dbc.Container(id=id_("tableB"))),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id=id_("association_plot"))),
                    dbc.Col(dcc.Graph(id=id_("frequency_plot"))),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(dbc.Container(id=id_("tableC"))),
                    dbc.Col(dbc.Container(id=id_("tableD"))),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id=id_("phenotype_genotype_plot"))),
                    dbc.Col(dcc.Graph(id=id_("phenotype_genotype_methyltype_plot"))),
                ]
            ),
        ],
        is_open=False,
        id=id_("results_area"),
        style={"margin-bottom": "25px"},
    )

    notifications = dbc.Row(dbc.Alert("", id=id_("n-samples-alert"), is_open=False))

    actions = dbc.Row(
        [
            dcc.Interval(
                id=id_("intervals"), interval=1000, n_intervals=0, disabled=True
            ),
            dcc.Store(id=id_("n-samples"), storage_type="memory"),
            dcc.Store(id=id_("client-task"), storage_type="memory"),
            dcc.Store(id=id_("client-result"), storage_type="memory"),
        ],
    )

    layout = dbc.Container(
        [alerts, form, notifications, output, actions], fluid=True, className=""
    )

    return layout
