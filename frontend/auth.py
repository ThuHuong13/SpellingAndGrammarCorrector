import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"  # Replace with your actual API base URL


def login_callback():
    """
    Callback function for login.
    Authenticates user via the API and updates session state.
    """
    username = st.session_state.login_username
    password = st.session_state.login_password
    success, message = login(username, password)
    if success:
        st.session_state.authenticated = True
        st.session_state.access_token = message["access_token"]
        st.session_state.username = username
    else:
        st.session_state.info_message = message


def logout_callback():
    """
    Callback function for logout.
    Resets authentication state.
    """
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.access_token = ""
    st.session_state.suggested_text = ""
    st.session_state.login_message = "Logged out successfully."


def signup_callback():
    """
    Callback function for sign-up.
    Registers a new user and shows the response message.
    """
    email = st.session_state.signup_email
    username = st.session_state.signup_username
    password = st.session_state.signup_password
    _, message = signup(email, username, password)
    st.session_state.signup_message = message


def login(username, password):
    """
    Authenticate user via the login API.
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/login",
            json={"username": username, "password": password},
        )                   
        if response.status_code == 200:
            return (
                True,
                response.json(),
            )  # Assuming the API returns user data on success
        return False, response.json().get("message", "Invalid username or password.")
    except Exception as e:
        return False, str(e)


def signup(email, username, password):
    """
    Register a new user via the signup API.
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/register",
            json={"email": email, "username": username, "password": password},
        )
        if response.status_code == 201:
            return (
                True,
                response.json(),
            )
        return False, response.json().get("message", "Sign-up failed.")
    except Exception as e:
        return False, str(e)
