import requests


class Client:
    def __init__(
        self,
        age: tuple | list,
        sex: tuple | list,
        sample_group: str,
        tissue: str,
        phenotype: str,
        cpg: str | None = None,
        rs: str | None = None,
    ):
        self.endpoint = "http://localhost:8000"
        self.age = age
        self.sex = sex
        self.sample_group = sample_group
        self.tissue = tissue
        self.phenotype = phenotype
        self.cpg = cpg
        self.rs = rs
        self.task_id = None

    def get_samples_names(self) -> list:
        body = {
            "age": self.age,
            "sex": self.sex,
            "phenotype": self.phenotype,
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
        return result

    def start_analysis(self) -> None:
        body = {
            "age": self.age,
            "sex": self.sex,
            "sample_group": self.sample_group,
            "tissue": self.tissue,
            "phenotype": self.phenotype,
            "cpg": self.cpg,
            "rs": self.rs,
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
