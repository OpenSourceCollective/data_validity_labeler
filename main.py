import random

import pandas as pd
import streamlit as st
from datetime import datetime

import src.backend.database as db
from src.backend.schema import Record

# -------------- SETTINGS --------------
page_title = "Health Record Validity Labeler"
page_icon = (
    ":health_worker:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
)
layout = "centered"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

# --- HIDE STREAMLIT STYLE ---: uncomment in production
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)

st.title(f"{page_icon} {page_title}er")
st.write(
    "This is a simple app to check and label the validity of electronic health records."
)
st.markdown("---")
st.subheader("Patient Vitals Validation")
st.write("*[Insert instructions here]*")


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
        data = db.fetch_records({"patient_id": patient_id}, limit=limit)
        if len(data) > 0:
            got_data = True
    return patient_id, data


expert_name = st.text_input(
    "Name", placeholder="Please enter your name", label_visibility="hidden"
)

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
            st.write(f"{record.vitals}: {record.vitals_reading} {record.unit}")
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
        # disabled=(expert_name == "")
    )
    if submitted:
        print("item: ", item)
        # TODO: submit data to database
        st.cache_data.clear()
        st.experimental_rerun()
