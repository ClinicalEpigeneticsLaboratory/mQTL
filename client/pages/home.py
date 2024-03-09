import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

dash.register_page(__name__, path="/")

card_1_content = [
    dbc.CardHeader("Tool", className="text-align"),
    dbc.CardBody(
        [
            html.H5("Analyse custom mQTL", className="card-title text-align"),
            html.P(
                "Conduct analysis here ....",
                className="card-text text-align card-text",
            ),
            dbc.Button(
                "Go",
                href="/mqtl-explorer",
                className="button-home-style button-interact",
            ),
        ],
    ),
]

card_2_content = [
    dbc.CardHeader("Tool", className="text-align"),
    dbc.CardBody(
        [
            html.H5("mQTL browser", className="card-title text-align"),
            html.P(
                "Browse mQTL here .....",
                className="card-text text-align card-text",
            ),
            dbc.Button(
                "Go",
                href="/cluster-explorer",
                className="button-home-style button-interact",
            ),
        ],
    ),
]

layout = dbc.Container(
    [
        dbc.Row(html.Br()),
        dbc.Row(
            dbc.Col(
                dcc.Markdown(
                    "### mQTL-DB this is mQTL database",
                    style={"text-align": "center"},
                ),
                xs=12,
                sm=12,
                md=12,
                lg=12,
                xl=12,
            ),
            justify="center",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Markdown(
                    """
                    ----

                    This application was designed to enable user-friendly analysis and visualization of
                    interactions between genome and methylome (mQTL).

                    If you want to report a bug or request a new feature, please use [GitHub](https://github.com/ClinicalEpigeneticsLaboratory/eDAVE/issues).

                    ----
                    """,
                    style={"text-align": "center"},
                ),
                xs=12,
                sm=12,
                md=12,
                lg=12,
                xl=12,
            )
        ),
        dbc.Row(html.Br()),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(card_1_content, className="card-style-custom"),
                    xs=12,
                    sm=12,
                    md=4,
                    lg=4,
                    xl=4,
                ),
                dbc.Col(
                    dbc.Card(card_2_content, className="card-style-custom"),
                    xs=12,
                    sm=12,
                    md=4,
                    lg=4,
                    xl=4,
                ),
            ],
            justify="center",
            style={"margin-top": "5%"},
        ),
    ],
    fluid=True,
)
