import streamlit as st
import streamlit_authenticator as stauth

from src.backend.database import get_user, get_users
from src.backend.schema import User
from src.ui import admin_blocks
from src.ui.header import header
from src.ui.record_data_blocks import record_validation_form

users = get_users()
# DEBUG
# print("Users: ", users)
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
    current_user = get_user(name)
    current_user.pop("password")
    validations = current_user.pop("validations")
    current_user = User(**current_user)
    current_user.validations = validations
    if current_user.is_admin:
        records_tab, admin_tab, analysis_tab = st.tabs(["Records", "Admin", "Analysis"])
        with records_tab:
            record_validation_form(current_user)
        with admin_tab:
            st.write("**Manage Users**")
            admin_blocks.user_management_block()
        with analysis_tab:
            st.write("**Records Analysis**")
            admin_blocks.analysis_block()
    elif current_user.is_staff:
        records_tab, analysis_tab = st.tabs(["Records", "Analysis"])
        with records_tab:
            record_validation_form(current_user)
        with analysis_tab:
            st.write("**Records Analysis**")
            admin_blocks.analysis_block()
    else:
        record_validation_form(current_user)

    authenticator.logout("Logout", "main")

elif st.session_state["authentication_status"] == False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] == None:
    st.warning("Please enter your username and password")
