import os

from deta import Deta  # pip install deta
from src.backend.schema import Record

from dotenv import load_dotenv
load_dotenv()


# Load the environment variables
DETA_KEY = os.getenv("DETA_KEY")

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("ehr_1")


def insert_record(record: Record) -> None:
    """Insert a record into the database
    It will update an item if the key already exists.

    Args:
        record (Record): The record object
    """
    record_id = db.put(record.to_dict())
    return record_id


def get_record(record_id: str) -> Record:
    """Get a record from the database

    Args:
        record_id (str): The record id

    Returns:
        Record: The record object
    """
    record = db.get(record_id)
    return Record(**record)


def fetch_records(query: dict={}, limit: int = 1, last: str = None) -> list:
    """Retrieve a list of items matching the query

    Args:
        query (dict): A single query or a list of queries
        limit (int, optional): The limit of the number of items to retrieve. Defaults to 1.
        last (str, optional): The last key in a previous response, provide this in a subsequent call to fetch further items. Defaults to None.

    Returns:
        list: _description_
    """
    records = db.fetch(query, limit=limit, last=last)
    return records.items


if __name__ == "__main__":
    pass

    print(fetch_records({"record_id": 760}))
