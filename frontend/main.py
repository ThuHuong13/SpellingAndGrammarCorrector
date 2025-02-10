import streamlit as st
import pandas as pd
from auth import login_callback, logout_callback, signup_callback
from api import (
    check_spell,
    check_grammar,
    apply_correction,
    get_documents,
    get_corrections,
)


st.set_page_config(
    page_title="Spelling and Grammar Checker",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)


# State management for user authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.access_token = ""
if "username" not in st.session_state:
    st.session_state.username = ""
if "suggested_text" not in st.session_state:
    st.session_state.suggested_text = ""

if not st.session_state.authenticated:
    # Main app
    st.title("Welcome to the Spelling and Grammar checker App")
    st.markdown("***")
    st.image("./static/dataset-cover.png")

    st.sidebar.subheader("Login or Sign Up")

    with st.sidebar:
        tabs = st.tabs(["Login", "Sign Up"])

        # Login Tab
        with tabs[0]:
            st.subheader("Login")
            st.text_input("Username", key="login_username")
            st.text_input("Password", type="password", key="login_password")
            st.button(
                "Login",
                on_click=login_callback,
                type="primary",
                use_container_width=True,
            )

            # Show login message
            if "info_message" in st.session_state:
                st.error(st.session_state.info_message)

        # Sign Up Tab
        with tabs[1]:
            st.subheader("Sign Up")
            st.text_input("Email", key="signup_email")
            st.text_input("Username", key="signup_username")
            st.text_input("Password", type="password", key="signup_password")
            st.button(
                "Sign Up",
                on_click=signup_callback,
                type="primary",
                use_container_width=True,
            )
            # Show sign-up message
            if "signup_message" in st.session_state:
                if "successful" in st.session_state.signup_message:
                    st.success(st.session_state.signup_message)
                else:
                    st.error(st.session_state.signup_message)
else:
    # Authenticated state
    st.sidebar.subheader(f"Welcome, {st.session_state.username}")
    st.sidebar.button("Log Out", on_click=logout_callback)

    st.subheader("📝 Spelling and Grammar Checker")

    st.markdown(
        """
        ***
        """
    )

    tab1, tab2, tab3 = st.tabs(["💻 Input Content", "📄 Documents", "✅ Corrections"])
    with tab1:
        # Character counter under input field
        char_count = 0
        user_input = st.text_area(
            "Write or paste your content here",
            value=st.session_state.suggested_text,
            max_chars=3000,
            key="input_text",
        )
        st.session_state.suggested_text = user_input
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Spell check"):
                if not user_input:
                    st.warning("Please enter some text to check.")
                else:
                    success, result = check_spell(user_input)

                    correction = result.get("correction")
                    correction_highlighted = result.get("correction_highlighted")
                    correction_edits = result.get("correction_edits")
                    if success:
                        if correction_edits == []:
                            st.success("No spelling errors found.")
                        else:
                            st.markdown(
                                f"Spell checked result: {correction_highlighted}",
                                unsafe_allow_html=True,
                            )
                            st.markdown(
                                f"Suggessted correction: {correction}",
                                unsafe_allow_html=True,
                            )
                            st.button(
                                "Apply spell correction",
                                on_click=lambda: apply_correction(
                                    correction=correction,
                                    errors={"errors": correction_edits},
                                ),
                                type="primary",
                            )
                    else:
                        st.error(result)
        with col2:
            if st.button("Grammar check"):
                if not user_input:
                    st.warning("Please enter some text to check.")
                else:
                    success, result = check_grammar(user_input)

                    correction = result.get("correction")
                    correction_highlighted = result.get("correction_highlighted")
                    correction_edits = result.get("correction_edits")
                    if success:
                        if correction_edits == []:
                            st.success("No grammar errors found.")
                        else:
                            st.markdown(
                                f"Grammar checked result: {correction_highlighted}",
                                unsafe_allow_html=True,
                            )
                            st.markdown(
                                f"Suggessted correction: {correction}",
                                unsafe_allow_html=True,
                            )
                            st.button(
                                "Apply Grammar correction",
                                on_click=lambda: apply_correction(
                                    correction=correction,
                                    errors={"errors": correction_edits},
                                ),
                                type="primary",
                            )
                    else:
                        st.error(result)
    with tab2:
        _, documents = get_documents()
        documents_df = pd.DataFrame(documents)

        # Display the DataFrame in Streamlit as a table
        st.dataframe(documents_df)

    with tab3:
        _, corrections = get_corrections()
        # Convert the list of dictionaries to a pandas DataFrame
        corrections_df = pd.DataFrame(corrections)

        # Display the DataFrame in Streamlit as a table
        st.dataframe(corrections_df)

    st.markdown(
        """
        ***
        """
    )
