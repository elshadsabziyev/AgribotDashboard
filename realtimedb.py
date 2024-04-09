from credential_loader import Credentials
import firebase
import streamlit as st


class RealtimeDB(Credentials):
    """
    A class representing a Realtime Database.

    Inherits from the Credentials class.

    Attributes:
        app: The Firebase app instance.
        auth: The Firebase authentication instance.
        db: The Firebase database instance.
        user_info: Information about the user.
        id_token: The ID token of the user.

    Methods:
        push_sensor_data_for_user: Pushes new sensor data for the user.
        get_sensor_data_for_user: Gets all the sensor data for the user.
        update_valve_status_for_user: Updates the valve_status for the user.
        get_valve_status_for_user: Gets the valve_status for the user.
        delete_sensor_data_for_user: Deletes all the sensor data for the user.
    """

    def __init__(self) -> None:
        super().__init__()
        try:
            self.app = firebase.initialize_app(self.firebase_config)
        except Exception as e:
            st.error(
                f"""
                # There was an error initializing the Firebase app.
                - You may want to refresh the page.
                - If the problem persists, please contact the developer.
                """
            )
            st.stop()
        if st.session_state.get("user_info") is not None:
            self.db = self.app.database()
            self.user_info = st.session_state.user_info["fullUserInfo"]
            self.id_token = st.session_state.user_info["idToken"]

    def push_sensor_data_for_user(self, data: dict) -> None:
        """
        Sets the sensor data for the user.

        Args:
            data (dict): The sensor data to set.

        Returns:
            None
        """
        try:
            uid = self.user_info["users"][0]["localId"]
            self.db.child("users").child(uid).child("sensor_data").push(
                data=data, token=self.id_token
            )
        except Exception as e:
            st.error(
                f"""
                # There was an error pushing the sensor data.
                - You may want to refresh the page.
                - If the problem persists, please contact the developer.
                """
            )
            st.stop()

    def get_sensor_data_for_user(self) -> dict:
        """
        Gets the all the sensor data for the user (from the first to the last data).

        Returns:
            dict: The sensor data for the user.
        """
        try:
            uid = self.user_info["users"][0]["localId"]
            return (
                self.db.child("users")
                .child(uid)
                .child("sensor_data")
                .get(token=self.id_token)
                .val()
            )
        except Exception as e:
            st.error(
                f"""
                # There was an error getting the sensor data.
                - You may want to refresh the page.
                - If the problem persists, please contact the developer.
                """
            )
            st.stop()

    def update_valve_status_for_user(self, valve_status: str) -> None:
        """
        Updates the valve_status for the user.

        Args:
            valve_status (str): The new valve_status value.

        Returns:
            None
        """
        try:
            uid = self.user_info["users"][0]["localId"]

            # Update the valve_status field under the user's uid
            self.db.child("users").child(uid).child("valve_status").set(
                {"valve_status": valve_status}, token=self.id_token
            )
        except Exception as e:
            st.error(
                f"""
                # There was an error updating the valve status.
                - You may want to refresh the page.
                - If the problem persists, please contact the developer.
                """
            )
            st.stop()

    def get_valve_status_for_user(self) -> str:
        """
        Gets the valve_status for the user.

        Returns:
            str: The valve_status for the user.
        """
        try:
            uid = self.user_info["users"][0]["localId"]
            return (
                self.db.child("users")
                .child(uid)
                .child("valve_status")
                .get(token=self.id_token)
                .val()
            )
        except Exception as e:
            pass

    def delete_sensor_data_for_user(self) -> None:
        """
        Deletes all the sensor data for the user.
        Also deletes the valve_status field for the user.

        Returns:
            None
        """
        try:
            uid = self.user_info["users"][0]["localId"]
            self.db.child("users").child(uid).child("sensor_data").remove(
                token=self.id_token
            )
            self.db.child("users").child(uid).child("valve_status").remove(
                token=self.id_token
            )
        except Exception as e:
            st.error(
                f"""
                # There was an error deleting the sensor data.
                - You may want to refresh the page.
                - If the problem persists, please contact the developer.
                """
            )
            st.stop()
