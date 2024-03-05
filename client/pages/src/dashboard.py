import requests
import pandas as pd
from plotly.graph_objects import Figure
import plotly.express as px


class Dashboard:
    def __init__(
        self, sex: list[str], age: list[int], tissue: list[str], pheno: list[str]
    ):
        self.endpoint = "http://localhost:8000/data"
        self.sex = sex
        self.age = age
        self.tissue = tissue
        self.pheno = pheno
        self.data = None
        self.figures = {}

    def load_data(self) -> None:
        body = {
            "age": self.age,
            "sex": self.sex,
            "phenotype": self.pheno,
            "tissue": self.tissue,
        }

        try:
            result = requests.post(self.endpoint, json=body, timeout=100)
            result.raise_for_status()

        except requests.HTTPError as ex:
            raise ex

        except requests.Timeout as ex:
            raise ex

        result = result.json()
        result = pd.DataFrame.from_dict(result)
        result.columns = ["Row", "Sample_ID", "Phenotype", "Age", "Sex", "Tissue"]

        self.data = result

    def bar_plot(self, column: str):
        cnt = self.data[column].value_counts()
        fig = px.bar(cnt)

        fig.update_layout(width=600, height=600, font={"size": 16})
        self.figures[column] = fig

    def box_plot(self, column: str):
        cnt = self.data[column]
        fig = px.box(cnt)

        fig.update_layout(width=600, height=600, font={"size": 16})
        self.figures[column] = fig

    @property
    def get_figures(self) -> dict[str, Figure]:
        figures = {}
        for key, figure in self.figures.items():
            figure.update_layout(
                title=key,
                width=600,
                height=600,
                font={"size": 16},
                showlegend=False,
                yaxis={"title": ""},
                xaxis={"title": ""},
            )
            figures[key] = figure

        return figures
