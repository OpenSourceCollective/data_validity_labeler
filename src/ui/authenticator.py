import streamlit as st
import streamlit_authenticator as stauth
from src.backend.database import get_users

users = get_users()
usernames = {item["username"]: item for item in users}

authenticator = stauth.Authenticate(
    {"usernames": usernames},
    "ehr_records_validity_labeler",
    "ehr_rvl_05_2023",
    cookie_expiry_days=14,
)


def auth_logout():
    authenticator.logout("Logout", key="force_logout")
