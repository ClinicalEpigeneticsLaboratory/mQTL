import dash
from dash import Input, Output, State, callback
from plotly.io import from_json

from .layouts.mqtl_explorer_layout import generate_mqtl_explorer_layout
from .utils.utils import create_dash_table, id_factory
from .src.connector import Client

id_ = id_factory(__name__)
dash.register_page(__name__, title="mQTL explorer")
layout = generate_mqtl_explorer_layout(id_)


@callback(
    Output(id_("sex-field"), "value"),
    Output(id_("sample_group-field"), "value"),
    Output(id_("tissue-field"), "value"),
    Output(id_("pheno-field"), "value"),
    Output(id_("rsID-field"), "value"),
    Output(id_("cpgID-field"), "value"),
    Input(id_("load_example"), "n_clicks"),
    prevent_initial_call=True,
)
def load_example(_) -> ...:
    return (
        ["Male", "Female"],
        "Healthy sample",
        "Blood",
        "epigenetic_age",
        "rs1671064",
        "cg24851651",
    )


@callback(
    Output(id_("alert"), "children"),
    Output(id_("alert"), "is_open"),
    State(id_("sex-field"), "value"),
    State(id_("sample_group-field"), "value"),
    State(id_("tissue-field"), "value"),
    State(id_("pheno-field"), "value"),
    State(id_("rsID-field"), "value"),
    State(id_("cpgID-field"), "value"),
    Input(id_("submit"), "n_clicks"),
    prevent_initial_call=True,
)
def validate_inputs(
    sex: list[str],
    sample_group: str,
    tissue: str,
    pheno: str,
    rs: str,
    cpg: str,
    _,
) -> ...:
    if (
        not sex
        or not sample_group
        or not tissue
        or not pheno
        or not rs
        or not cpg
    ):
        return "Please fill missing field(s)", True

    if not rs.startswith("rs") or not cpg.startswith("cg"):
        return "Make sure that rsID starts with 'rs' and cpgID starts with 'cg'", True

    return dash.no_update


@callback(
    Output(id_("n-samples-alert"), "children"),
    Output(id_("n-samples-alert"), "is_open"),
    Input(id_("sex-field"), "value"),
    Input(id_("sample_group-field"), "value"),
    Input(id_("tissue-field"), "value"),
    Input(id_("pheno-field"), "value"),
    Input(id_("age-field"), "value"),
    prevent_initial_call=True,
)
def show_number_of_samples(
    sex: list[str], sample_group: str, tissue: str, phenotype: str, age: list[int]
) -> tuple:
    if sex and sample_group and tissue and phenotype:
        analysis = Client(
            sex=sex,
            sample_group=sample_group,
            phenotype=phenotype,
            tissue=tissue,
            age=age,
        )

        samples = len(analysis.get_samples_names())
        return f"Number of samples for selected conditions --> {samples}.", True

    return dash.no_update


@callback(
    Output(id_("submit"), "disabled", allow_duplicate=True),
    Output(id_("client-task"), "data", allow_duplicate=True),
    Output(id_("intervals"), "disabled", allow_duplicate=True),
    State(id_("sex-field"), "value"),
    State(id_("sample_group-field"), "value"),
    State(id_("tissue-field"), "value"),
    State(id_("age-field"), "value"),
    State(id_("pheno-field"), "value"),
    State(id_("rsID-field"), "value"),
    State(id_("cpgID-field"), "value"),
    Input(id_("submit"), "n_clicks"),
    prevent_initial_call=True,
)
def start_analysis(
    sex: list[str],
    sample_group: str,
    tissue: str,
    age: list[int],
    phenotype: str,
    rs: str,
    cpg: str,
    _,
) -> ...:
    if (
        sex
        and sample_group
        and tissue
        and age
        and rs
        and cpg
    ):
        if rs.startswith("rs") and cpg.startswith("cg"):
            mqtl = Client(
                sex=sex,
                sample_group=sample_group,
                phenotype=phenotype,
                tissue=tissue,
                age=age,
                rs=rs,
                cpg=cpg,
            )
            mqtl.get_samples_names()
            mqtl.start_analysis()

            return True, mqtl.task_id, False

    return dash.no_update


@callback(
    Output(id_("intervals"), "disabled"),
    Output(id_("status"), "children"),
    Output(id_("status"), "is_open"),
    Output(id_("client-result"), "data", allow_duplicate=True),
    Output(id_("client-task"), "data"),
    Input(id_("client-task"), "data"),
    Input(id_("intervals"), "n_intervals"),
    prevent_initial_call=True,
)
def check_task_status(task_id: str, _):
    if task_id:
        result = Client.get_result(task_id)

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
    Output(id_("submit"), "disabled"),
    Output(id_("tableA"), "children"),
    Output(id_("tableB"), "children"),
    Output(id_("association_plot"), "figure"),
    Output(id_("frequency_plot"), "figure"),
    Output(id_("tableC"), "children"),
    Output(id_("tableD"), "children"),
    Output(id_("phenotype_genotype_plot"), "figure"),
    Output(id_("phenotype_genotype_methyltype_plot"), "figure"),
    Output(id_("results_area"), "is_open"),
    Output(id_("client-result"), "data"),
    Input(id_("client-result"), "data"),
    prevent_initial_call=True,
)
def render_output(data: dict) -> ...:
    if data:
        table_a, table_b, table_c, table_d = (
            data["tableA"],
            data["tableB"],
            data["tableC"],
            data["tableD"],
        )

        table_a = create_dash_table(table_a, show_col_names=False, reset_index=False)
        table_b = create_dash_table(table_b)
        table_c = create_dash_table(table_c, reset_index=False)
        table_d = create_dash_table(table_d)

        (
            mqtl_plot,
            genotype_frequency_plot,
            phenotype_genotype_plot,
            phenotype_genotype_methyltype_plot,
        ) = (
            data["mqtl_plot"],
            data["genotype_frequency_plot"],
            data["phenotype_genotype_plot"],
            data["phenotype_genotype_methyltype_plot"],
        )

        return (
            False,
            table_a,
            table_b,
            from_json(mqtl_plot),
            from_json(genotype_frequency_plot),
            table_c,
            table_d,
            from_json(phenotype_genotype_plot),
            from_json(phenotype_genotype_methyltype_plot),
            True,
            None,
        )

    return dash.no_update
