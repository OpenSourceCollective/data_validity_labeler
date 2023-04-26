# EHR Validator

This project is a web-based validator for EHR data.

## Set up

Create a Python environment and install the dependencies:

```bash
pip install -r requirements.txt
```

## The database

The database is a No-SQL database, based on [Deta](https://deta.space). It is a key-value storage, where the key is the Record ID, and the other values are the recorded data.

The original schema is as follows:

```json
{
  "key": "int", # same as record_id
  "record_id": "int",
  "patient_id": "int",
  "vitals": "str",
  "unit": "str",
  "loinc_code": "str",
  "vitals_reading": "float",
  "body_position": "str",
  "user_type": "str",
  "record_created_by": "str",
  "datetime_record_created": "datetime",
  "record_updated_by": "str",
  "datetime_record_deleted": "datetime",
  "record_validity": "int",
  "timestamp": "int",
  "vitals_type": "str"
}
```

We intend to update the database by adding an expert_validity field where multiple experts can submit a score for the validity of the record.

```json
{
  "expert_validity": [
    {
      "expert_id": "int",
      "score": "int",
      "created_at": "datetime"
    },
    ...
  ]
}
```

## Usage

- Provide a `.env` file where the environment variables are located.
- The `DETA_KEY` is the API key for the storage in [Deta space](https://deta.space). It is needed to access the cloud-based database. See the [src/backend/database.py](src/backend/database.py) file for more details on the simple interface to the database.
