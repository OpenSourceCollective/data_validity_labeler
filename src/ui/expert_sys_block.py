import time
from typing import List
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.backend.database import (
    create_user,
    delete_user,
    fetch_records,
    get_user,
    get_users,
    update_user,
)
from src.backend.database import get_all_data_df

from src.backend.schema import ANALYSIS_DISPLAY, User

#ES block
def es_block_1():
    data = get_all_data_df()
    patient_ids = data['patient_id'].dropna().unique().astype(int)
    with st.form("es_block_1_form", clear_on_submit=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            field_check = st.checkbox("Field check")
            patient_check = st.checkbox("Patient check")
        with col2:  #make col2 - col4 appear only on field check = true
            sel_fields = st.selectbox(
                'Select field(s) to check',
                ('Height', 'Weight', 'Temperature', 'Pulse', 'Systolic', 'Diastolic', 'Resp rate'))
            sel_patient = st.selectbox(
                'Select patient(s) to check', patient_ids)
        with col3:
                low_lim = st.number_input("Type Low limit", value=None, placeholder="")
                st.write('Low limit is', low_lim)
        with col4:
                high_lim = st.number_input("Type High limit", value=None, placeholder="")
                st.write('High limit is', high_lim)

        es_submit = st.form_submit_button("Find suspect records")

    if es_submit:
        # insert form inputs into db
        # get results
        
        # display spinner until computation is done
        es_block_2(data, [low_lim, high_lim], [sel_fields], field_check, patient_check)
        

def es_block_2(sus_data, limits: List[float], vitals: List[str], field_check: bool = False, patient_check:bool = False): #specify arg list from backend
    """Displays the result of expert system run"""
    # TODO:
    # needs the number of relevant records
    # needs the number of suspect records

    rel_recs = 100 #placeholder variable for no. relevant records arg
    sus_recs = 10 #placeholder variable for no. of suspect records arg
    # sus_data = data #placeholder variable for suspect records arg. A subset of the dataset
    # limits = [low_lim, high_lim] #placeholder variable for limits list arg. extractable from sus_data?
    # vitals = [vital1, vital2] #placeholder variable for vitals list arg. extractable from sus_data?

    st.metric(label="Releveant records", value=rel_recs)
    st.metric(label="Suspect records", value=sus_recs)

    show_data = st.checkbox("Show Suspect Records", key="show_data")
    
    # if show_data:
    st.write(sus_data)

    if field_check:
        #if field check, show count vs limit, low and high
        plot_data = px.bar(sus_data, x=limits)
        fig = go.Figure(data=plot_data)
        st.plotly_chart(fig)

    if patient_check:
        #if patient check, show count vs vitals
        plot_data = px.bar(sus_data, x=vitals[0])
        fig = go.Figure(data=plot_data)
        st.plotly_chart(fig)

    # define/catch if (field_check and patient_check)
    