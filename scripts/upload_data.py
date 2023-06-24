"""
This should be run only once to upload the data to the database
"""
import json
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import src.backend.database as db

orginal_data_path = "path/to/original/dataset.csv"
uploaded_data_path = "path/to/uploaded_records.json"  # this is to keep track of the uploaded records
raw_data = pd.read_csv(orginal_data_path).sample(frac=1)

print("Uploading data to the database...")
with open(uploaded_data_path, "r") as f:
    uploaded_data = json.load(f)

p_bar = tqdm(raw_data.iterrows())
for _, row in p_bar:
    row = {k: "" if v != v else v for k, v in row.to_dict().items()}
    row["key"] = str(row["record_id"])
    if row["key"] in uploaded_data:
        continue
    if db.get_record(row["key"]) is None:
        row["record_validation_updated"] = str(datetime.now())
        db.insert_record(row)
    uploaded_data[row["key"]] = row["key"]
    with open(uploaded_data_path, "w") as f:
        json.dump(uploaded_data, f)
    p_bar.set_description(f"Inserted record {row['record_id']}")
