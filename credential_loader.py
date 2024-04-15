# NOTE: This file contains the Credentials class that is used to manage credentials for Firebase and OpenAI.

import streamlit as st

from firebase_admin import credentials


class Credentials:
    """
    Class to manage credentials for Firebase and OpenAI.

    Attributes:
        firebase_credentials (service_account.Credentials): Firestore credentials.
        firebase_config (dict): Firebase configuration.
        openai_credentials (str): OpenAI API key.
        db_url (str): URL of the Firebase database.

    Methods:
        get_firestore_credentials: Retrieves the Firestore credentials from the secrets file.
        get_openai_credentials: Retrieves the OpenAI API key from the secrets file.
        get_firebase_config: Retrieves the Firebase configuration from the secrets file.
    """

    def __init__(self) -> None:
        try:
            self.firebase_cert = self.make_firebase_cert()
        except KeyError:
            pass
        try:
            self.firebase_config = self.get_firebase_config()
        except KeyError:
            st.error(
                """
                # There was an error retrieving the Firebase configuration.
                - Please check the secrets file.
                - If the problem persists, please contact the developer.
                """
            )
        try:
            self.openai_credentials = self.get_openai_credentials()
        except KeyError:
            pass
        try:
            self.db_url = st.secrets["firebase_config"]["databaseURL"]
        except KeyError:
            st.error(
                """
                # There was an error retrieving the Firebase database URL.
                - Please check the secrets file.
                - If the problem persists, please contact the developer.
                """
            )

    def make_firebase_cert(self) -> credentials.Certificate:
        """
        Retrieves the Firestore credentials from the secrets file.

        Returns:
            credentials (service_account.Credentials): Firestore credentials.
        """
        credentials_dict = {
            "type": st.secrets["firebase_auth"]["type"],
            "project_id": st.secrets["firebase_auth"]["project_id"],
            "private_key_id": st.secrets["firebase_auth"]["private_key_id"],
            "private_key": st.secrets["firebase_auth"]["private_key"],
            "client_email": st.secrets["firebase_auth"]["client_email"],
            "client_id": st.secrets["firebase_auth"]["client_id"],
            "auth_uri": st.secrets["firebase_auth"]["auth_uri"],
            "token_uri": st.secrets["firebase_auth"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase_auth"][
                "auth_provider_x509_cert_url"
            ],
            "client_x509_cert_url": st.secrets["firebase_auth"]["client_x509_cert_url"],
        }
        return credentials.Certificate(credentials_dict)

    def get_openai_credentials(self) -> str:
        """
        Retrieves the OpenAI API key from the secrets file.

        Returns:
            openai_api_key (str): OpenAI API key.
        """
        return st.secrets["openai"]["openai_api_key"]

    def get_firebase_config(self) -> dict:
        """
        Retrieves the Firebase configuration from the secrets file.

        Returns:
            firebase_config (dict): Firebase configuration.
        """
        return {
            "apiKey": st.secrets["firebase_config"]["apiKey"],
            "authDomain": st.secrets["firebase_config"]["authDomain"],
            "projectId": st.secrets["firebase_config"]["projectId"],
            "storageBucket": st.secrets["firebase_config"]["storageBucket"],
            "messagingSenderId": st.secrets["firebase_config"]["messagingSenderId"],
            "appId": st.secrets["firebase_config"]["appId"],
            "measurementId": st.secrets["firebase_config"]["measurementId"],
            "databaseURL": st.secrets["firebase_config"]["databaseURL"],
        }
