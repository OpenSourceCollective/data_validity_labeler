import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.backend.database import (
    create_user,
    delete_user,
    fetch_records,
    get_record_ids,
    get_user,
    get_users,
    update_user,
)
from src.backend.schema import ANALYSIS_DISPLAY, User


# Create new users
def create_user_block():
    """
    Create a new user
    """
    # TODO: Add password confirmation and sanity checks
    # TODO: Check if user already exists
    form_data = {
        "username": st.text_input("Username", key="create_username"),
        "password": st.text_input("Password", key="create_password", type="password"),
        "is_admin": st.checkbox("Admin", key="create_is_admin"),
        "is_staff": st.checkbox("Staff", key="create_is_staff"),
    }
    if st.button("Create User"):
        if form_data["username"] and form_data["password"]:
            user = User(**form_data)
            create_user(user)
            st.success("User created successfully")
        else:
            st.error("Please enter a username and password")
    return


# Delete users
def delete_user_block():
    """
    Delete a user
    """
    username = st.text_input("Username", key="delete_username")
    if username:
        user = get_user(username)
        if user:
            if st.button("Delete User"):
                delete_user(user)
                st.success("User deleted successfully")
        else:
            st.error("User does not exist")


def list_users_block():
    """
    List all users
    """
    st.write("Registered Users")
    all_users = get_users()
    all_users = pd.DataFrame(all_users[1:])
    st.write(all_users[["username", "is_admin", "is_staff"]])
    return


# # Update users
def update_user_block():
    """
    Update a user
    """
    st.write("**Update User**")
    username = st.text_input("Username", key="get_username")
    # check if user exists
    if username:
        user = get_user(username)
        if user:
            user.pop("validations")
            user = User(**user)
            form_data = {
                "is_admin": st.checkbox(
                    "Admin", key="update_is_admin", value=user.is_admin
                ),
                "is_staff": st.checkbox(
                    "Staff", key="update_is_staff", value=user.is_staff
                ),
            }
            form_data["username"] = username
            if st.button("Update User"):
                if form_data["username"]:
                    user.username = form_data["username"]
                if form_data["is_admin"]:
                    user.is_admin = form_data["is_admin"]
                if form_data["is_staff"]:
                    user.is_staff = form_data["is_staff"]
                update_user(user)
                st.success("User updated successfully")
        else:
            st.error("User does not exist")
    return


# User management block
def user_management_block():
    block = st.container()
    with block:
        list_users_block()
        with st.expander("Create New User"):
            create_user_block()
        with st.expander("Delete User"):
            delete_user_block()
        with st.expander("Update User"):
            update_user_block()
    return


@st.cache_data()
def get_cache_record_ids() -> int:
    return get_record_ids()["data"]


@st.cache_data(show_spinner=False)
def get_all_data_df() -> pd.DataFrame:
    all_data = []
    last = None
    progress_value = 0
    while True:
        response = fetch_records(limit=1000, last=last)
        if len(response) == 0:
            break
        last = response[-1]["key"]
        all_data += response
        print("i: ", last)
    return pd.DataFrame(all_data)


# Analysis block
def analysis_block():
    with st.spinner(text="Loading data... Please wait."):
        all_data = get_all_data_df()
    data_size = len(all_data)
    if ANALYSIS_DISPLAY.progress.id in all_data.columns:
        progressed = all_data.dropna(subset=[ANALYSIS_DISPLAY.progress.id])
        progress_value = len(progressed) / data_size
    else:
        progressed = []
        progress_value = 0
    st.progress(
        progress_value,
        text=ANALYSIS_DISPLAY.progress.name
        + ": "
        + str(len(progressed))
        + "/"
        + str(data_size),
    )
    show_data = st.checkbox("Show Raw Data")
    if show_data:
        st.write(all_data)
    selected_case = st.selectbox(
        "Select a data to plot", ANALYSIS_DISPLAY.data_fields, index=0
    )
    plot_data = px.bar(all_data, x=selected_case)
    fig = go.Figure(data=plot_data)
    st.plotly_chart(fig)
