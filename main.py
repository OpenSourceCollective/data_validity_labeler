import streamlit as st
import src.backend.database as db
from src.backend.schema import Record
import pandas as pd


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

st.title(f"{page_icon} {page_title}")
st.write(
    "This is a simple app to check and label the validity of electronic health records."
)
st.markdown("---")
st.subheader("Sample Data Fetching")


@st.cache_data()
def get_sample_data(limit: int = 5) -> pd.DataFrame:
    # TODO: replace with actual data
    return db.fetch_records({"patient_id": 25656}, limit=limit)


expert_name = st.text_input(
    "Name", placeholder="Name", label_visibility="hidden"
)

with st.form("entry_form", clear_on_submit=True):
    sample_data = get_sample_data(10)
    st.write("#### Patient ID: 25656")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Record Created**")
    with col2:
        st.write("**Recorded Vitals**")
    with col3:
        st.write("**Record Validity Score**")
    for i, item in enumerate(sample_data):
        record = Record(**item)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"{record.datetime_record_created}")
        with col2:
            st.write(f"{record.vitals}: {record.vitals_reading} {record.unit}")
        with col3:
            score = st.number_input(
                f"{record.record_id} Score",
                value=3,
                step=1,
                label_visibility="hidden",
            )

        "---"

    submitted = st.form_submit_button("Save Data")
