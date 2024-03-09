import pandas as pd
from dash import dash_table


def create_dash_table(
    df: pd.DataFrame | dict, show_col_names: bool = True, reset_index: bool = True
) -> dash_table.DataTable:
    if isinstance(df, dict):
        df = pd.DataFrame.from_dict(df)

    if reset_index:
        df = df.reset_index()

    if show_col_names:
        col_names = [{"name": name, "id": name} for name in df.columns]
    else:
        col_names = [{"name": "", "id": name} for name in df.columns]

    df = df.round(4)

    table = dash_table.DataTable(
        data=df.to_dict("records"),
        columns=col_names,
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

    return table


def id_factory(page: str):

    if "." in page:
        page = page.split(".")[1]

    def func(_id: str):
        """
        # SETUP

        from system.utils.utils import id_factory
        id = id_factory(__name__) # create the id function for that page

        # LAYOUT

        layout = html.Div(
            id=id('main-div')
        )
        # CALLBACKS

        @app.callback(
            Output(id('main-div'),'children'),
            Input(id('main-div'),'style')
        )
        def funct(this):
            ...
        """
        return f"{_id}-{page}"

    return func
