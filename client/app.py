import logging

import dash
import dash_bootstrap_components as dbc

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    filename="log.log",
    level=logging.INFO,
    datefmt="%Y/%m/%d %I:%M:%S %p",
)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.UNITED, dbc.icons.BOOTSTRAP],
    external_scripts=[
        {"src": "//cdn.cookie-script.com/s/bb3fe642e6b1cbf070e2252fcfafc06b.js"}
    ],
    use_pages=True,
)

server = app.server

pages = [
    dbc.ListGroupItem("Home", href="/"),
    dbc.ListGroupItem("Dashboard", href="/dashboard"),
]

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.DropdownMenu(
            children=[dbc.DropdownMenuItem("Pages", header=True, divider=True), *pages],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand=f"mQTL DB",
    brand_href="/",
    color="primary",
    dark=True,
)

footer = dash.html.Footer(
    [
        dbc.Row(
            dbc.Col(
                "Powered by Independent Clinical Epigenetics Laboratory. Research use only.",
                style={"color": "white"},
            ),
        ),
    ],
    className="footer-custom",
)

app.layout = dbc.Container([navbar, dash.page_container, footer], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
