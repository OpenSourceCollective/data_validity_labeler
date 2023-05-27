import random
from datetime import datetime

import pandas as pd
import streamlit as st

import src.backend.database as db
from src.backend.schema import RECORD_DISPLAY, VALIDITY_DISPLAY, Record, User


@st.cache_data()
def get_patient_ids() -> int:
    # TODO: replace with a deterministic fetcher
    patient_ids = db.get_patient_ids()["data"]
    return patient_ids


@st.cache_data()
def get_patient_data(limit: int = 5) -> pd.DataFrame:
    # TODO: replace with actual data
    got_data = False
    while not got_data:  # some samples dont have data
        patient_id = random.choice(get_patient_ids())
        data = db.fetch_records({"patient_id": patient_id}, limit=1000)
        if len(data) > 0:
            got_data = True
    return patient_id, data


# TODO: Deprecate this
def patient_data_validation_form() -> None:
    st.write(f'Welcome, **{st.session_state["name"]}**')
    with st.form("entry_form", clear_on_submit=True):
        patient_id, patient_data = get_patient_data(50)
        st.write(f"#### Patient ID: {patient_id}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**Record Created**")
        with col2:
            st.write("**Recorded Vitals**")
        with col3:
            st.write("**Record Validity Score**")
        for i, item in enumerate(patient_data):
            record = Record(**item)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"{record.datetime_record_created}")
            with col2:
                st.write(
                    f"{record.vitals}: {record.vitals_reading} {record.unit}"
                )
                if record.body_position:
                    st.write(f"Body Position: {record.body_position}")
                if record.vitals_type:
                    st.write(f"Vitals Type: {record.vitals_type}")
            with col3:
                score = st.number_input(
                    f"{record.record_id} Score",
                    value=0,
                    step=1,
                    max_value=5,
                    min_value=0,
                    label_visibility="hidden",
                )
                if score > 0:
                    item["expert_validity"] += [
                        {
                            "expert_id": 1234,  # TODO: assign unique ids to experts
                            "score": score,
                            "created_at": datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                        }
                    ]
            st.markdown("---")

        submitted = st.form_submit_button(
            "Save Data",
        )
        if submitted:
            # print("item: ", item)
            # TODO: submit data to database
            st.cache_data.clear()
            st.experimental_rerun()


def record_validation_form(user: User) -> None:
    st.write(f'Welcome, **{st.session_state["name"]}**')
    with st.form("entry_form", clear_on_submit=True):
        patient_id, patient_data = get_patient_data(50)
        st.write(f"#### Patient ID: {patient_id}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**{RECORD_DISPLAY.blocks[0].header}**")
        with col2:
            st.write(f"**{RECORD_DISPLAY.blocks[1].header}**")
        with col3:
            st.write(f"**{VALIDITY_DISPLAY.fields[0].name}**")
        for i, item in enumerate(patient_data):
            record = item
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
                    item["expert_validity"] += [
                        {
                            "expert_id": user.key,
                            "score": score,
                            "created_at": datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                        }
                    ]
            st.markdown("---")

        submitted = st.form_submit_button(
            "Save Data",
        )
        if submitted:
            # print("item: ", item)
            # TODO: submit data to database
            st.cache_data.clear()
            st.experimental_rerun()
