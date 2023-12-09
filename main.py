import streamlit as st

from src.backend.schema import User
from src.ui import admin_blocks
from src.ui.header import header
from src.ui.record_data_blocks import record_validation_form

header()
current_user = User(username="user", is_admin=True, is_staff=True)
if current_user.is_staff:
    records_tab, analysis_tab = st.tabs(["Records", "Analysis"])
    with records_tab:
        record_validation_form(current_user)
    with analysis_tab:
        st.write("**Records Analysis**")
        admin_blocks.analysis_block()
else:
    record_validation_form(current_user)
