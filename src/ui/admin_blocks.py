# TODO: create block for managing users
# def create_user():
# def delete_user():
# def update_user():

# imports
import streamlit as st
from src.backend.database import create_user, get_users, get_user, update_user, delete_user
from src.backend.schema import User

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
        "is_staff": st.checkbox("Staff", key="create_is_staff")
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
    st.write("**Delete User**")
    username = st.text_input("Username", key="delete_username")
    if username:
        user = get_user(username)
        if user:
            if st.button("Delete User"):
                delete_user(user)
                st.success("User deleted successfully")
        else:
            st.error("User does not exist")


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
            user = User(**user)
            form_data = {
                "is_admin": st.checkbox("Admin", key="update_is_admin", value=user.is_admin),
                "is_staff": st.checkbox("Staff", key="update_is_staff", value=user.is_staff)
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
                st.error("Please enter a username and password")
        else:
            st.error("User does not exist")
    return

# User management block
def user_management_block():
    block = st.container()
    with block:
        with st.expander("Create New User"):
            create_user_block()
        with st.expander("Delete User"):
            delete_user_block()
        with st.expander("Update User"):
            update_user_block()
    return