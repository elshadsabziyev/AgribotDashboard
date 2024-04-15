# NOTE: This file contains the FirebaseAuthenticator class that is used to manage user authentication using Firebase.

import json
import requests
from credential_loader import Credentials
import streamlit as st
import re


class FirebaseAuthenticator(Credentials):
    """
    Class to manage user authentication using Firebase.

    Attributes:
        firebase_config (str): Firebase configuration.

    Methods:
        sign_in_with_email_and_password: Signs in a user with the provided email and password.
        get_account_info: Retrieves the account information associated with the given ID token.
        send_email_verification: Sends an email verification request to the user with the provided ID token.
        send_password_reset_email: Sends a password reset email to the specified email address.
        create_user_with_email_and_password: Creates a new user with the provided email and password.
        delete_user_account: Deletes a user account using the provided ID token.
        raise_detailed_error: Raises a detailed error if the HTTP request returns an error status code.
        sign_in: Signs in a user with the provided email and password.
        create_account: Creates a new user account with the provided email and password.
        reset_password: Resets the password for the given email.
        sign_out: Clears the session state and displays a success message for signing out.
        delete_account: Deletes the user account associated with the provided password.
    """

    def __init__(self) -> None:
        super().__init__()
        self.firebase_config = self.get_firebase_config().get("apiKey")

    def sign_in_with_email_and_password(self, email: str, password: str) -> dict:
        """
        Signs in a user with the provided email and password.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            dict: A dictionary containing the response data from the API.

        Raises:
            DetailedError: If there is an error during the API request.
        """
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(
            self.firebase_config
        )
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps(
            {"email": email, "password": password, "returnSecureToken": True}
        )
        request_object = requests.post(request_ref, headers=headers, data=data)
        self.raise_detailed_error(request_object)
        return request_object.json()

    def get_account_info(self, id_token: str) -> dict:
        """
        Retrieves the account information associated with the given ID token.

        Args:
            id_token (str): The ID token to authenticate the request.

        Returns:
            dict: The account information as a dictionary.

        Raises:
            DetailedError: If there is an error in the request.
        """
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={0}".format(
            self.firebase_config
        )
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"idToken": id_token})
        request_object = requests.post(request_ref, headers=headers, data=data)
        self.raise_detailed_error(request_object)
        return request_object.json()

    def send_email_verification(self, id_token: str) -> dict:
        """
        Sends an email verification request to the user with the provided ID token.

        Args:
            id_token (str): The ID token of the user.

        Returns:
            dict: The response JSON object containing the result of the request.
        """
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(
            self.firebase_config
        )
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"requestType": "VERIFY_EMAIL", "idToken": id_token})
        request_object = requests.post(request_ref, headers=headers, data=data)
        self.raise_detailed_error(request_object)
        return request_object.json()

    def send_password_reset_email(self, email: str) -> dict:
        """
        Sends a password reset email to the specified email address.

        Args:
            email (str): The email address to send the password reset email to.

        Returns:
            dict: A dictionary containing the response from the API call.

        Raises:
            DetailedError: If there is an error in the API call.
        """
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(
            self.firebase_config
        )
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"requestType": "PASSWORD_RESET", "email": email})
        request_object = requests.post(request_ref, headers=headers, data=data)
        self.raise_detailed_error(request_object)
        return request_object.json()

    def create_user_with_email_and_password(self, email: str, password: str) -> dict:
        """
        Creates a new user with the provided email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.

        Returns:
            dict: A dictionary containing the response from the API call.

        Raises:
            DetailedError: If there is an error in the API call.
        """
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={0}".format(
            self.firebase_config
        )
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps(
            {"email": email, "password": password, "returnSecureToken": True}
        )
        request_object = requests.post(request_ref, headers=headers, data=data)
        self.raise_detailed_error(request_object)
        return request_object.json()

    def delete_user_account(self, id_token: str) -> dict:
        """
        Deletes a user account using the provided ID token.

        Args:
            id_token (str): The ID token of the user.

        Returns:
            dict: The response from the delete account request.

        Raises:
            DetailedError: If there is an error in the delete account request.
        """
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/deleteAccount?key={0}".format(
            self.firebase_config
        )
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"idToken": id_token})
        request_object = requests.post(request_ref, headers=headers, data=data)
        self.raise_detailed_error(request_object)
        return request_object.json()

    def raise_detailed_error(self, request_object: requests.models.Response) -> None:
        """
        Raises a detailed error if the HTTP request returns an error status code.

        Args:
            request_object (requests.models.Response): The response object from the HTTP request.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returns an error status code.

        """
        try:
            request_object.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise requests.exceptions.HTTPError(error, request_object.text)

    def sign_in(self, email: str, password: str) -> None:
        """
        Signs in a user with the provided email and password.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Raises:
            requests.exceptions.HTTPError: If there is an HTTP error during the sign-in process.
            Exception: If there is an error during the sign-in process.

        Returns:
            None
        """
        try:
            id_token = self.sign_in_with_email_and_password(email, password)["idToken"]
            # user_info = self.get_account_info(id_token)["users"][0]
            account_info = self.get_account_info(id_token)
            user_info = account_info["users"][0]
            if not user_info["emailVerified"]:
                self.send_email_verification(id_token)
                st.session_state.auth_warning = """
                ##### Email not verified.
                - Check your inbox to verify your email.
                - Please check your spam folder if you don't see it in your inbox.
                """
            else:
                user_info["idToken"] = id_token
                user_info["fullUserInfo"] = account_info
                st.session_state.user_info = user_info
                st.rerun()
        except requests.exceptions.HTTPError as error:
            error_message = json.loads(error.args[1])["error"]["message"]
            if error_message in {
                "INVALID_EMAIL",
                "EMAIL_NOT_FOUND",
                "INVALID_PASSWORD",
                "MISSING_PASSWORD",
                "INVALID_LOGIN_CREDENTIALS",
            }:
                st.session_state.auth_warning = """
                ##### Error: Invalid login credentials.
                - Please check your email and password.
                - Forgot your password?
                - Click the 'Forgot Password' button to reset it.
                """
            elif any(
                re.search(pattern, error_message, re.IGNORECASE)
                for pattern in {
                    "TOO_MANY_ATTEMPTS_TRY_LATER",
                    "USER_DISABLED",
                    "OPERATION_NOT_ALLOWED",
                    "USER_NOT_FOUND",
                    "TOO_MANY_ATTEMPTS_TRY_LATER : Too many unsuccessful login attempts. Please try again later.",
                }
            ):
                st.session_state.auth_warning = """
                ##### Error: Too many attempts.
                - Please try again later.
                - You are temporarily blocked from signing in.
                - Be sure to verify your email.
                - Get access instantly by resetting your password.
                - Or, wait for a while and try again.
                """
            else:
                st.session_state.auth_warning = f"Error: {error_message}"
        except Exception as error:
            st.session_state.auth_warning = f"Error: {error}"

    def create_account(self, email: str, password: str) -> None:
        """
        Creates a new user account with the provided email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user account.

        Raises:
            requests.exceptions.HTTPError: If there is an HTTP error during the account creation process.
            Exception: If there is an unexpected error during the account creation process.
        """
        try:
            id_token = self.create_user_with_email_and_password(email, password)[
                "idToken"
            ]
            self.send_email_verification(id_token)
            st.session_state.auth_success = f"""
            ##### Account created successfully.
            - Email sent to {email} to verify your email.
            - Check your inbox to verify your email.
            - Please check your spam folder if you don't see it in your inbox.
            """
        except requests.exceptions.HTTPError as error:
            error_message = json.loads(error.args[1])["error"]["message"]
            if error_message == "EMAIL_EXISTS":
                st.session_state.auth_warning = """
                    ##### Error: Email already exists.
                    - Use a different email.
                    - If you already have an account, sign in.
                    - Forgot your password?
                    - Click the 'Forgot Password' button to reset it.
                    """
            elif error_message in {
                "INVALID_EMAIL",
                "MISSING_EMAIL",
            }:
                st.session_state.auth_warning = "Error: Use a valid email address"
            elif error_message in {
                "MISSING_PASSWORD",
                "WEAK_PASSWORD : Password should be at least 6 characters",
            }:
                st.session_state.auth_warning = """
                ##### Error: Weak password.
                - Password should be at least 6 characters.
                - Use a strong password.
                - Include numbers, symbols, and uppercase letters.
                """
            else:
                st.session_state.auth_warning = f"Error: {error_message}"
        except Exception as error:
            st.session_state.auth_warning = f"Error: {error}"

    def reset_password(self, email: str) -> None:
        """
        Resets the password for the given email.

        Args:
            email (str): The email address for which the password needs to be reset.

        Returns:
            None

        Raises:
            requests.exceptions.HTTPError: If there is an HTTP error while sending the password reset email.
            Exception: If there is any other error while sending the password reset email.
        """
        try:
            self.send_password_reset_email(email)
            st.session_state.auth_success = f"""
            ##### Password reset email sent.
            - Email sent to {email} to reset your password.
            - Check your inbox to reset your password.
            - Please check your spam folder if you don't see it in your inbox.
            """
        except requests.exceptions.HTTPError as error:
            error_message = json.loads(error.args[1])["error"]["message"]
            if error_message in {"MISSING_EMAIL", "INVALID_EMAIL", "EMAIL_NOT_FOUND"}:
                st.session_state.auth_warning = """
                ##### Error: Invalid email.
                - Please check your email address.  
                - Use the email address you used to create your account.
                """
            else:
                st.session_state.auth_warning = f"Error: {error_message}"
        except Exception as error:
            st.session_state.auth_warning = f"Error: {error}"

    def sign_out(self) -> None:
        """
        Clears the session state and displays a success message for signing out.

        This function clears the session state, including any authenticated user information,
        and sets the `auth_success` variable in the session state to a success message.

        Returns:
            None
        """
        st.session_state.clear()
        st.session_state.auth_success = (
            "user signed out successfully."  # Not displayed in the app
        )

    def delete_account(self, password: str) -> None:
        """
        Deletes the user account associated with the provided password.

        Args:
            password (str): The password of the user account.

        Returns:
            None

        Raises:
            requests.exceptions.HTTPError: If there is an HTTP error during the account deletion.
            Exception: If there is any other error during the account deletion.
        """
        try:
            id_token = self.sign_in_with_email_and_password(
                st.session_state.user_info["email"], password
            )["idToken"]
            self.delete_user_account(id_token)
            st.session_state.clear()
            st.session_state.auth_success = """
            ##### Account deleted successfully.
            - Your account has been deleted.
            - You have been signed out.
            - Sign up to create a new account.
            """
        except requests.exceptions.HTTPError as error:
            error_message = json.loads(error.args[1])["error"]["message"]
            if error_message in {
                "INVALID_EMAIL",
                "EMAIL_NOT_FOUND",
                "INVALID_PASSWORD",
                "MISSING_PASSWORD",
                "INVALID_LOGIN_CREDENTIALS",
            }:
                st.session_state.auth_warning = f"""
                ##### Error: Invalid login credentials.
                - You have to enter your password again to delete your account.
                - Please check your password.
                - Use the password you used to sign in.
                - Forgot your password?
                - Click the 'Forgot Password' button to reset it.
                """
            elif any(
                re.search(pattern, error_message, re.IGNORECASE)
                for pattern in {
                    "TOO_MANY_ATTEMPTS_TRY_LATER",
                    "USER_DISABLED",
                    "OPERATION_NOT_ALLOWED",
                    "USER_NOT_FOUND",
                    "TOO_MANY_ATTEMPTS_TRY_LATER : Too many unsuccessful login attempts. Please try again later.",
                }
            ):
                st.session_state.auth_warning = """
                ##### Error: Too many attempts.
                - Please try again later.
                - You are temporarily blocked from signing in.
                - Be sure to verify your email.
                - Get access instantly by resetting your password.
                - Or, wait for a while and try again.
                """
            else:
                st.session_state.auth_warning = f"Error: {error_message}"
        except Exception as error:
            st.session_state.auth_warning = f"Error: {error}"

    def verify_password(self, password: str) -> bool:
        """
        Verifies the password against the user's password.

        Args:
            password (str): The password to verify.

        Returns:
            bool: True if the password matches the user's password, False otherwise.
        """
        try:
            id_token = st.session_state.user_info["idToken"]
            self.sign_in_with_email_and_password(
                st.session_state.user_info["email"], password
            )
            return True
        except requests.exceptions.HTTPError as error:
            error_message = json.loads(error.args[1])["error"]["message"]
            if error_message in {
                "INVALID_EMAIL",
                "EMAIL_NOT_FOUND",
                "INVALID_PASSWORD",
                "MISSING_PASSWORD",
                "INVALID_LOGIN_CREDENTIALS",
            }:
                return False
            elif any(
                re.search(pattern, error_message, re.IGNORECASE)
                for pattern in {
                    "TOO_MANY_ATTEMPTS_TRY_LATER",
                    "USER_DISABLED",
                    "OPERATION_NOT_ALLOWED",
                    "USER_NOT_FOUND",
                    "TOO_MANY_ATTEMPTS_TRY_LATER : Too many unsuccessful login attempts. Please try again later.",
                }
            ):
                return False
            else:
                return False
        except Exception as error:
            return False