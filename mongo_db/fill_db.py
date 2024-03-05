import pymongo
import pandas as pd
from tqdm import tqdm

client = pymongo.MongoClient("mongodb://user:pass@localhost:27017/")
mydb = client["mQTL"]

gsa_collection = mydb["GSA"]
gsa = pd.read_parquet("../mongo_db/data/genomic.parquet")
gsa = gsa.loc[~gsa.index.duplicated()]

for _id, row in tqdm(gsa.iterrows()):
    record = {"_id": _id, **dict(row)}
    gsa_collection.insert_one(record)

epic_collection = mydb["EPIC"]
epic = pd.read_parquet("../mongo_db/data/methylation.parquet")

for _id, row in tqdm(epic.iterrows()):
    record = {"_id": _id, **dict(row)}
    epic_collection.insert_one(record)

print(mydb.list_collection_names())
print("DONE")
