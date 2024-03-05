import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table
from models.models import Samples, Base


url = f"postgresql+psycopg2://user:pass@localhost:5432/mqtl-db"

engine = create_engine(url)
data = pd.read_csv("sample_sheet.csv", index_col=0)
data = data[["Sample_Name", "Age", "Sex", "Tissue", "7/1.Melanoma type"]]

data["7/1.Melanoma type"] = data["7/1.Melanoma type"].fillna("Healthy sample")
data["7/1.Melanoma type"] = [
    "Melanoma" if value != "Healthy sample" else value
    for value in data["7/1.Melanoma type"]
]

if data.isna().sum().any():
    raise Exception("NaN in original dataset!")

metadata = MetaData()
metadata.reflect(bind=engine)

if "samples" in metadata.tables:
    samples_table = Table("samples", metadata, autoload=True, autoload_with=engine)
    samples_table.drop(engine)
    print(f"Table already exists, dropping!")

Base.metadata.create_all(engine)

all_records = []
for _, row in data.iterrows():
    single_record = Samples(
        sample_name=row.Sample_Name,
        phenotype=row["7/1.Melanoma type"],
        age=row.Age,
        sex=row.Sex,
        tissue=row.Tissue,
    )
    all_records.append(single_record)

with Session(engine) as session:
    session.add_all(all_records)
    session.commit()
    print(f"DONE!")
