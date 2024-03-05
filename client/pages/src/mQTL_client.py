import requests


class mqtlClient:
    def __init__(
        self,
        age: tuple | list,
        sex: tuple | list,
        pheno: tuple | list,
        tissue: tuple | list,
        cpg: str,
        rs: str,
    ):
        self.endpoint = "http://localhost:8000"
        self.age = age
        self.sex = sex
        self.pheno = pheno
        self.tissue = tissue
        self.cpg = cpg
        self.rs = rs
        self.samples = None
        self.task_id = None

    def get_samples_names(self) -> None:
        body = {
            "age": self.age,
            "sex": self.sex,
            "phenotype": self.pheno,
            "tissue": self.tissue,
        }
        try:
            result = requests.post(f"{self.endpoint}/samples", json=body, timeout=1000)
            result.raise_for_status()

        except requests.HTTPError as ex:
            raise ex

        except requests.Timeout as ex:
            raise ex

        result = result.json()
        self.samples = tuple(result)

    def start_analysis(self) -> None:
        body = {
            "samples": self.samples,
            "cpg": self.cpg,
            "rs": self.rs,
            "model_type": "OLS",
            "reg": 1,
        }
        try:
            result = requests.post(f"{self.endpoint}/analyse", json=body, timeout=1000)
            result.raise_for_status()

        except requests.HTTPError as ex:
            raise ex

        except requests.Timeout as ex:
            raise ex

        result = result.json()
        self.task_id = result["TaskID"]

    @staticmethod
    def get_result(task_id: str) -> dict:
        try:
            result = requests.get(f"http://localhost:8000/result/{task_id}")
            result.raise_for_status()

        except requests.HTTPError as ex:
            raise ex

        except requests.Timeout as ex:
            raise ex

        result = result.json()
        return result
