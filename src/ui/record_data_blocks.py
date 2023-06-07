import random
from datetime import datetime

import pandas as pd
import streamlit as st

import src.backend.database as db
from src.backend.schema import (
    QUERY_ID,
    RECORD_DISPLAY,
    VALIDITY_DISPLAY,
    User,
)


@st.cache_data()
def get_record_ids() -> int:
    # TODO: replace with a deterministic fetcher
    return db.get_record_ids()["data"]


@st.cache_data()
def get_record_data(limit: int = 5) -> pd.DataFrame:
    # TODO: replace with actual data
    got_data = False
    while not got_data:  # some samples dont have data
        record_id = random.choice(get_record_ids())
        data = db.fetch_records({QUERY_ID: record_id}, limit=1000)
        if len(data) > 0:
            got_data = True
    return record_id, data


def record_validation_form(user: User) -> None:
    st.write(f'Welcome, **{st.session_state["name"]}**')
    with st.form("entry_form", clear_on_submit=True):
        record_id, record_data = get_record_data(50)
        st.write(f"#### Record ID: {record_id}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**{RECORD_DISPLAY.blocks[0].header}**")
        with col2:
            st.write(f"**{RECORD_DISPLAY.blocks[1].header}**")
        with col3:
            st.write(f"**{VALIDITY_DISPLAY.fields[0].name}**")

        updated_records = []
        # expert_validities = []
        for i, item in enumerate(record_data):
            record = item
            record["expert_validity"] = record.get("expert_validity", [])
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
                    record["expert_validity"] += [
                        {
                            "expert_id": user.key,
                            "score": score,
                            "created_at": datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                        }
                    ]
            updated_records.append(record)
            st.markdown("---")

        submitted = st.form_submit_button(
            "Save Data",
        )
        if submitted:
            # TODO: submit data to database
            for record in updated_records:
                db.insert_record(record)
            st.cache_data.clear()
            st.experimental_rerun()
