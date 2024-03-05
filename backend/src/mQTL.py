import pymongo
import pandas as pd
import plotly.express as px
import statsmodels.api as sms
from .url_utils import create_mongo_url


class mQTL:
    def __init__(
        self, samples: list[str], cpg: str, rs: str, model_type: str, reg: float
    ):

        self.samples = samples
        self.cpg = cpg
        self.rs = rs
        self.model_type = model_type
        self.reg = reg
        self.data = None
        self.mapper = None

    def load_data(self) -> None:
        url = create_mongo_url()
        client = pymongo.MongoClient(url)
        db = client["mQTL"]

        gse = pd.DataFrame(db["GSA"].find({"_id": self.rs})).set_index("_id").T
        epic = pd.DataFrame(db["EPIC"].find({"_id": self.cpg})).set_index("_id").T

        df = pd.concat((gse, epic), axis=1, join="inner")
        df = df.loc[self.samples]
        df = df[~df[self.rs].str.contains("0")]
        df = df.dropna()

        df["Intercept"] = 1
        self.data = df

    def model(self) -> tuple[dict, dict, dict]:
        order = sorted(self.data[self.rs].unique())
        code = [cnt for cnt, _ in enumerate(order)]

        self.mapper = dict(zip(order, code))
        data = self.data.copy()
        data[self.rs] = self.data[self.rs].map(self.mapper)

        model = sms.OLS(data[self.cpg], data.drop(self.cpg, axis=1))
        model = model.fit()

        table_a, table_b = (
            model.summary2().tables[0].to_dict(),
            model.summary2().tables[1].to_dict(),
        )
        model_predictions = model.predict(data.drop(self.cpg, axis=1)).to_dict()

        return table_a, table_b, model_predictions

    def plot(self) -> str:
        data = self.data
        data[self.rs] = data[self.rs]

        fig = px.box(self.data, x=self.rs, y=self.cpg)
        fig.update_layout(font={"size": 16}, yaxis={"range": (0, 1)})
        fig.update_xaxes(
            categoryorder="array", categoryarray=sorted(self.data[self.rs].unique())
        )
        fig = fig.to_json()

        return fig
