import streamlit as st
from src.ui.blocks import authenticated_form
from src.ui.header import header
from src.ui.authenticator import auth_logout

# st.write(st.session_state)

header()
authenticated_form()
auth_logout()
