import os
from http import client
from typing import Dict

import streamlit as st
from deta import Deta
from dotenv import load_dotenv

from src.backend.schema import RECORD_ID, User

load_dotenv()


# Load the environment variables
DETA_KEY = os.getenv("DETA_KEY")

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
record_db = deta.Base("ehr_1")
user_db = deta.Base("ehr_2")
validation_db = deta.Base("validation_db")


def create_user(user: User) -> None:
    user_response = deta.Base("ehr_2").put(user.to_dict())
    return user_response


def update_user(user: User) -> None:
    user_response = deta.Base("ehr_2").put(user.to_dict())
    return user_response


def get_users() -> None:
    records = deta.Base("ehr_2").fetch({"model": "user"})
    return records.items


@st.cache_data()
def get_user(username) -> None:
    records = deta.Base("ehr_2").fetch({"username": username}, limit=1)
    return records.items[0] if records.items else None


def delete_user(user: User) -> None:
    deta.Base("ehr_2").delete(user["key"])
    return


def insert_record(record: Dict) -> None:
    """Insert a record into the database
    It will update an item if the key already exists.

    Args:
        record (Dict): The record object
    """
    record_response = deta.Base("ehr_1").put(record)
    return record_response


def insert_validation(record: Dict) -> None:
    """Insert a validation record into the database
    It will update an item if the key already exists.

    Args:
        record (Dict): The record object
    """
    validation_response = deta.Base("validation_db").put(record)
    return validation_response


def get_record(record_id: str) -> Dict:
    """Get a record from the database

    Args:
        record_id (str): The record id

    Returns:
        Record: The record object
    """
    return deta.Base("ehr_1").get(record_id)


def fetch_records(query: dict = None, limit: int = 1, last: str = None) -> list:
    """Retrieve a list of items matching the query

    Args:
        query (dict): A single query or a list of queries
        limit (int, optional): The limit of the number of items to retrieve. Defaults to 1.
        last (str, optional): The last key in a previous response, provide this in a subsequent call to fetch further items. Defaults to None.

    Returns:
        list: _description_
    """

    if dict is None:
        query = {}
    try:
        records = deta.Base("ehr_1").fetch(query, limit=limit, last=last)
        return records.items
    except (client.CannotSendRequest, client.ResponseNotReady) as e:
        print(e)
        return []


def get_record_ids() -> list:
    """Get a list of record ids

    Returns:
        list: A list of record ids
    """
    return deta.Base("ehr_1").get(RECORD_ID)


if __name__ == "__main__":
    pass
