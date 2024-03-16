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

#ES block 1: for receiving user inputs
def es_block_1():
    data = get_all_data_df()
    patient_ids = data['patient_id'].dropna().unique().astype(int)
    limits = []
    vitals = []
    field_check = []
    patient_check = []

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
                low_lim = st.number_input("Type Low limit", value=0)
                st.write('Low limit is', low_lim)
                limits.append(low_lim)
        with col4:
                high_lim = st.number_input("Type High limit", value=1)
                st.write('High limit is', high_lim)
                limits.append(high_lim)

        es_submit = st.form_submit_button("Find suspect records")

        show_data = st.checkbox("Show Suspect Records", key="show_data")

    if es_submit:
        # insert form inputs into db
        # get results
        
        # display spinner until computation is done
        es_block_2(data, limits, [sel_fields], field_check, patient_check, show_data)
        

#ES block 2: For displaying results and such
def es_block_2(data, limits: List[float], vitals: List[str], field_check, patient_check, show_data): 
    """Displays the result of expert system run"""

    limits = [4, 20]

    #perform expert system check


    if patient_check == false
        rel_data = data[data.vitals==vitals[0]] #array is used for vitals for future check on simulataneous vitals like in patient check
    else:
        rel_data = data[data.]


    rel_recs = len(rel_data.index)

    sus_data = []
    low_lim = limits[0]
    high_lim = limits[1]

    
    #field check
    for i, item in rel_data.iterrows():
        if low_lim >= item['vitals_reading'] or item['vitals_reading'] >= high_lim:
            sus_data.append(item)
    sus_data_df = pd.DataFrame(sus_data)
    sus_recs = len(sus_data_df.index)

    #patient check
 

    st.metric(label="Releveant records", value=rel_recs)
    st.metric(label="Suspect records", value=sus_recs)
    
    if show_data:
        st.write(sus_data_df)

    if field_check:
        #if field check, show histogram of suspected records
        if sus_data_df.empty:
            st.write("No suspect records")
        else: 
            reading_col = sus_data_df['vitals_reading']
            plot_data = go.Histogram(x=reading_col)
            layout = go.Layout(
                title='Histogram of suspect records',
                title_x=0.3, #centralize title
                xaxis=dict(title='Vitals_reading'),
                yaxis=dict(title='Frequency')
            )
            fig = go.Figure(data=[plot_data],layout=layout)
            st.plotly_chart(fig)

    if patient_check:
        #if patient check, show count vs vitals
        plot_data = px.bar(sus_data_df, 'patient_id') #TO DO: make this count of (patient_ID_records) vs patient_ID
        fig = go.Figure(data=plot_data)
        st.plotly_chart(fig)



    # st.write(sus_data_df)
    # st.write(working[working.vitals_reading])

    # define/catch if (field_check and patient_check)
    