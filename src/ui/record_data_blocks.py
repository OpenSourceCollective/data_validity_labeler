import random
import time
from datetime import datetime
from typing import Optional

import streamlit as st

import src.backend.database as db
from src.backend.schema import (
    APP_INFO,
    QUERY_ID,
    RECORD_DISPLAY,
    VALIDITY_DISPLAY,
    User,
    Validation,
)


@st.cache_data()
def get_record_ids() -> int:
    return db.get_record_ids()["data"]


# @st.cache_data()
def get_record_data(
    limit: int = 1000, previous: Optional[list] = None
) -> tuple[str, list]:
    if previous is None:
        previous = []

    if "record_ids" not in st.session_state:
        st.session_state["record_ids"] = get_record_ids()

    got_data = False
    record_id = None
    record_is_not_validated = True
    while (
        not got_data and record_id not in previous and record_is_not_validated
    ):  # some samples dont have data
        record_id = random.choice(st.session_state["record_ids"])
        data = db.fetch_records({QUERY_ID: record_id}, limit=limit)
        if len(data) > 0:
            got_data = True
            if data[0].get("validated", None) is None:
                record_is_not_validated = False
        time.sleep(0.1)
    return record_id, data


def record_validation_form(user: User) -> None:
    st.write(f'Welcome, **{st.session_state["name"]}**')
    previous_validations = user.validations
    with st.form("entry_form", clear_on_submit=True):
        record_id, record_data = get_record_data(50, previous=previous_validations)
        st.write(f"#### Record ID: {record_id}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**{RECORD_DISPLAY.blocks[0].header}**")
        with col2:
            st.write(f"**{RECORD_DISPLAY.blocks[1].header}**")
        with col3:
            st.write(f"**{VALIDITY_DISPLAY.fields[0].name}**")

        updated_records = []
        validations = []
        for i, item in enumerate(record_data):
            record = item
            record[VALIDITY_DISPLAY.fields[0].id] = record.get(
                VALIDITY_DISPLAY.fields[0].id, []
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                for field in RECORD_DISPLAY.blocks[0].fields:
                    st.write(f"{record[field.id]}")
            with col2:
                for field in RECORD_DISPLAY.blocks[1].fields:
                    prefix = (
                        ""
                        if not field.prefix
                        else record[field.prefix.value]
                        if field.prefix.source == "record"
                        else field.prefix.value
                    )
                    suffix = (
                        ""
                        if not field.suffix
                        else record[field.suffix.value]
                        if field.suffix.source == "record"
                        else field.suffix.value
                    )
                    record_display = record[field.id]
                    if record_display != "":
                        st.write(f"{prefix}: {record_display}{suffix}")
            with col3:
                score = st.number_input(
                    f"{record['record_id']} Score",
                    value=0,
                    step=1,
                    max_value=5,
                    min_value=0,
                    label_visibility="hidden",
                )
                if score > 0:
                    record[VALIDITY_DISPLAY.fields[0].id] += [
                        {
                            "expert_id": user.key,
                            "score": score,
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    ]

                    # mark record as validated if max validations reached
                    if (
                        len(record[VALIDITY_DISPLAY.fields[0].id])
                        >= APP_INFO["max_validations"]
                    ):
                        record["validated"] = True
                    validations.append(
                        Validation(
                            user.key,
                            str(time.time()),
                            record["record_id"],
                            score,
                        )
                    )
            updated_records.append(record)
            st.markdown("---")

        submitted = st.form_submit_button(
            "Save Data",
        )
        if submitted:
            for record in updated_records:
                db.insert_record(record)
            for validation in validations:
                db.insert_validation(validation.to_dict())
                user.update_validations(validation.id)
            db.update_user(user)
