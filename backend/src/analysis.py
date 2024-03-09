import pandas as pd
import pingouin as pg
import plotly.express as px
import statsmodels.api as sms
from .db_operations import (
    select_clinical_data_from_db,
    select_omics_data_from_db,
)


class Analyser:
    def __init__(
        self,
        samples_characteristics: dict,
        cpg: str,
        rs: str,
        phenotype: str,
    ):
        self.samples_characteristics = samples_characteristics
        self.cpg = cpg
        self.rs = rs
        self.phenotype = phenotype
        self.data = None

    def load_omics_data(self) -> None:
        df = select_omics_data_from_db(self.rs, self.cpg)

        df = df[~df[self.rs].str.contains("0")]
        df = df.dropna()

        self.data = df

    def load_pheno_data(self) -> None:
        df = select_clinical_data_from_db(
            columns=["sample_name", self.phenotype], **self.samples_characteristics
        )
        df = df.set_index("sample_name")
        self.data = pd.concat((self.data, df), axis=1, join="inner")

    def model(self) -> tuple[dict, dict]:
        data = self.data[[self.rs, self.cpg]].copy()
        data["Intercept"] = 1

        order = sorted(data[self.rs].unique())
        code = [cnt for cnt, _ in enumerate(order)]

        mapper = dict(zip(order, code))
        data[self.rs] = data[self.rs].map(mapper)

        model = sms.OLS(data[self.cpg], data.drop(self.cpg, axis=1))
        model = model.fit()

        table_a, table_b = (
            model.summary2().tables[0].to_dict(),
            model.summary2().tables[1].to_dict(),
        )

        return table_a, table_b

    def categorical_plot(self, y: str, y_range: tuple | None = None) -> str:
        fig = px.box(
            self.data,
            x=self.rs,
            y=y,
            labels={self.phenotype: self.phenotype.replace("_", " ")},
        )

        if y_range:
            fig.update_layout(
                font={"size": 16},
                yaxis={"range": y_range},
            )
        else:
            fig.update_layout(font={"size": 16})

        fig.update_xaxes(
            categoryorder="array", categoryarray=sorted(self.data[self.rs].unique())
        )

        fig = fig.to_json()
        return fig

    def plot_genotype_frequency(self) -> str:
        genotype_cnt = self.data[self.rs].value_counts().to_frame()
        fig = px.pie(genotype_cnt, values="count", names=genotype_cnt.index)

        fig.update_layout(font={"size": 16}, legend={"title": "Genotype"})
        fig = fig.to_json()

        return fig

    def scatter_plot(self) -> str:
        fig = px.scatter(
            self.data,
            x=self.cpg,
            y=self.phenotype,
            labels={self.phenotype: self.phenotype.replace("_", " ")},
            color=self.rs,
        )
        fig.update_layout(
            font={"size": 16}, xaxis={"range": (0, 1)}, legend={"title": "Genotype"}
        )
        fig = fig.to_json()

        return fig

    def genotype_phenotype_assoc(self) -> dict:
        stats = pg.pairwise_tests(
            dv=self.phenotype,
            between=self.rs,
            data=self.data,
            return_desc=True,
            effsize="hedges",
            padjust="fdr_bh",
        ).round(3)

        stats = stats.drop(
            ["Paired", "Parametric", "p-adjust", "alternative", "T", "dof"], axis=1
        )
        return stats.to_dict()

    def methyltype_phenotype_assoc(self) -> dict:
        stats = pg.corr(self.data[self.phenotype], self.data[self.cpg])
        stats = stats.round(3).to_dict()
        stats["CI95%"]["pearson"] = str(stats["CI95%"]["pearson"])

        return stats
