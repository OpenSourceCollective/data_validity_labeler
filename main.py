import streamlit as st

from src.backend.schema import User
from src.ui import admin_blocks
from src.ui.header import header
from src.ui.record_data_blocks import record_validation_form
from src.ui.expert_sys_block import es_block_1

header()
current_user = User(username="user", is_admin=True, is_staff=True)
if current_user.is_staff:
    records_tab, analysis_tab, es_tab = st.tabs(["Records", "Analysis", "Expert System"])
    with records_tab:
        record_validation_form(current_user)
    with analysis_tab:
        st.write("**Records Analysis**")
        admin_blocks.analysis_block()
    with es_tab:
        st.write("**Expert System**")
        es_block_1()
else:
    record_validation_form(current_user)
