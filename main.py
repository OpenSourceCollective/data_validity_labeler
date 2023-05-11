import streamlit as st
import streamlit_authenticator as stauth

from src.ui.blocks import patient_data_validation_form
from src.backend.database import get_users
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
    patient_data_validation_form()
    authenticator.logout("Logout", "main")

elif st.session_state["authentication_status"] == False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] == None:
    st.warning("Please enter your username and password")
