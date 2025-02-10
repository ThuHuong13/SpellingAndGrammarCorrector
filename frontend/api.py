import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"  # Replace with your actual API base URL


def check_spell(content: str):
    """
    Check spelling of the content via the API.
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/checker/spell",
            json={"content": content},                                                  
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if response.status_code == 200:
            return True, response.json()["data"]

        return False, response.json().get("message", "Failed to check spell.")
    except Exception as e:
        return False, str(e)


def check_grammar(content: str):
    """
    Check grammar of the content via the API.
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/checker/grammar",
            json={"content": content},
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if response.status_code == 200:
            return True, response.json()["data"]

        return False, response.json().get("message", "Failed to check grammar.")
    except Exception as e:
        return False, str(e)


def create_document(content: str, errors: dict):
    """
    Create a new document via the API.
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/documents",
            json={"content": content, "errors": errors},
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if response.status_code == 201:
            return True, response.json()["data"]

        return False, response.json().get("message", "Failed to create document.")
    except Exception as e:
        return False, str(e)


def create_correction(original_text, suggested_text, document_id):
    """
    Create a new correction via the API.
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/corrections",
            json={
                "original_text": original_text,
                "suggested_text": suggested_text,
                "document_id": document_id,
            },
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if response.status_code == 201:
            return True, response.json()["data"]

        return False, response.json().get("message", "Failed to create corrections.")
    except Exception as e:
        return False, str(e)


def apply_correction(correction: str, errors: dict):
    _, document = create_document(st.session_state.suggested_text, errors)
    document_id = document["document_id"]
    create_correction(st.session_state.suggested_text, correction, document_id)
    st.session_state.suggested_text = correction


def get_documents():
    """
    Create a new document via the API.
    """
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/documents",
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if response.status_code == 200:
            return True, response.json().get("data")

        return False, response.json().get("message", "Failed to get document.")
    except Exception as e:
        return False, str(e)


def get_corrections():
    """
    Create a new document via the API.
    """
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/corrections",
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if response.status_code == 200:
            return True, response.json()["data"]

        return False, response.json().get("message", "Failed to get corrections.")
    except Exception as e:
        return False, str(e)
