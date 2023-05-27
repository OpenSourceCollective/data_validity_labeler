import streamlit as st
import streamlit_authenticator as stauth

from src.ui.patient_data_blocks import (
    patient_data_validation_form,
    record_validation_form,
)
from src.backend.database import get_users, get_user
from src.backend.schema import User
from src.ui.header import header

users = get_users()
usernames = {item["username"]: item for item in users}

authenticator = stauth.Authenticate(
    {"usernames": usernames},
    "ehr_records_validity_labeler",
    "ehr_rvl_05_2023",
    cookie_expiry_days=14,
)

name, authentication_status, username = authenticator.login("Login", "main")

if st.session_state["authentication_status"]:
    header()
    current_user = get_user(username)
    current_user.pop("password")
    current_user = User(**current_user)
    show_records = True
    # TODO: Fill admin tab with user management
    if current_user.is_admin:
        records_tab, admin_tab = st.tabs(
            [
                "Records",
                "Admin",
            ]
        )
        with admin_tab:
            st.write("**Manage Users**")
    if show_records:
        record_validation_form(current_user)
    authenticator.logout("Logout", "main")

elif st.session_state["authentication_status"] == False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] == None:
    st.warning("Please enter your username and password")
