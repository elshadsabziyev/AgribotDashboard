import time
import streamlit as st
from auth import FirebaseAuthenticator
from realtimedb import RealtimeDB
import pandas as pd
import datetime
from datetime import timedelta as tdlt
from datetime import datetime as dt


class App(FirebaseAuthenticator, RealtimeDB):
    def __init__(self):
        super().__init__()
        self.set_page_config()
        if "notifications" not in st.session_state:
            st.session_state.notifications = []
        self.last_notification_time = dt.now()

    def add_notification(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.notifications.append((timestamp, message))
    
    def show_notifications(self, sensor_data):
        if sensor_data:
            latest_timestamp = max(sensor_data.keys())
            latest_data = sensor_data[latest_timestamp]

            time_deadband = tdlt(seconds=1)

            if dt.now() - self.last_notification_time >= time_deadband:
                self.last_notification_time = dt.now()
                if latest_data["water_level"] <= 40:
                    message = f"**{dt.fromtimestamp(latest_data['timestamp']/1000).strftime('%Y-%m-%d %H:%M:%S')}**: *Water level is low*."
                    if (
                        not st.session_state.notifications
                        or st.session_state.notifications[-1][1] != message
                    ):
                        st.toast(message, icon="🚰")
                        self.add_notification(message)
                elif (
                    st.session_state.notifications
                    and "Water level is low" in st.session_state.notifications[-1][1]
                ):
                    message = f"**{dt.fromtimestamp(latest_data['timestamp']/1000).strftime('%Y-%m-%d %H:%M:%S')}**: *Water level is back to normal*."
                    st.toast(message, icon="🚰")
                    self.add_notification(message)

                if latest_data["water_level"] <= 10:
                    message = f"**{dt.fromtimestamp(latest_data['timestamp']/1000).strftime('%Y-%m-%d %H:%M:%S')}**: *Water level is critically low*."
                    if (
                        not st.session_state.notifications
                        or st.session_state.notifications[-1][1] != message
                    ):
                        st.toast(message, icon="🚱")
                        self.add_notification(message)
                elif (
                    st.session_state.notifications
                    and "Water level is critically low"
                    in st.session_state.notifications[-1][1]
                ):
                    message = f"**{dt.fromtimestamp(latest_data['timestamp']/1000).strftime('%Y-%m-%d %H:%M:%S')}**: *Water level is back to normal*."
                    st.toast(message, icon="🚰")
                    self.add_notification(message)

                if (
                    0 <= latest_data["humidity"] <= 50
                    and 0 <= latest_data["temperature"] <= 30
                ):
                    message = f"**{dt.fromtimestamp(latest_data['timestamp']/1000).strftime('%Y-%m-%d %H:%M:%S')}**: *Suboptimal conditions for greenhouse. Humidity ({latest_data['humidity']}%) and temperature ({latest_data['temperature']}°C) are not in the optimal range for plant growth*."
                    if (
                        not st.session_state.notifications
                        or st.session_state.notifications[-1][1] != message
                    ):
                        st.toast(message, icon="⏰")
                        self.add_notification(message)
                elif (
                    st.session_state.notifications
                    and "Suboptimal conditions" in st.session_state.notifications[-1][1]
                ):
                    message = f"**{dt.fromtimestamp(latest_data['timestamp']/1000).strftime('%Y-%m-%d %H:%M:%S')}**: *Conditions are back to optimal. Humidity ({latest_data['humidity']}%) and temperature ({latest_data['temperature']}°C) are now in the optimal range for plant growth*."

    def set_page_config(self):
        st.set_page_config(
            page_title="Farm Dashboard",
            page_icon=":seedling:",
            layout="centered",
            initial_sidebar_state="auto",
        )

    def auth_page(self):
        if "user_info" not in st.session_state:
            col1, col2, col3 = st.columns([2, 5, 2])
            login_register = col2.toggle(
                label="**Login/Register**", key="login_register"
            )
            if login_register:
                do_you_have_an_account = "No"
            else:
                do_you_have_an_account = "Yes"
            auth_form = col2.form(key="Authentication form", clear_on_submit=False)
            email = auth_form.text_input(
                label="**Email**",
                type="default",
                placeholder="Enter your email",
                autocomplete="email",
            )
            password = (
                auth_form.text_input(
                    label="**Password**",
                    type="password",
                    placeholder="Enter your password",
                    autocomplete="current-password",
                )
                if do_you_have_an_account in {"Yes", "No"}
                else auth_form.empty()
            )
            auth_notification = col2.empty()

            if do_you_have_an_account == "Yes":
                if auth_form.form_submit_button(
                    label="Sign In", use_container_width=True, type="primary"
                ):
                    with auth_notification, st.spinner("Signing in"):
                        self.sign_in(email, password)

                if auth_form.form_submit_button(
                    label="Forgot Password", use_container_width=True, type="secondary"
                ):
                    with auth_notification, st.spinner("Sending password reset link"):
                        self.reset_password(email)

            elif do_you_have_an_account == "No" and auth_form.form_submit_button(
                label="Create Account", use_container_width=True, type="primary"
            ):
                with auth_notification, st.spinner("Creating account"):
                    self.create_account(email, password)

            if "auth_success" in st.session_state:
                auth_notification.success(st.session_state.auth_success)
                del st.session_state.auth_success
            elif "auth_warning" in st.session_state:
                auth_notification.error(st.session_state.auth_warning)
                del st.session_state.auth_warning
        else:
            self.home_page()

    def home_page(self):
        self.sidebar()
        try:
            st.title(
                f"**Welcome, _{st.session_state.user_info['fullUserInfo']['users'][0]['email'].split('@')[0]}_!**"
            )
        except:
            st.title("**Welcome!**")
        st.info(
            """
            # Dashboard
            - This dashboard displays the sensor data from your farm.
            - You can view the sensor data in real-time and get notifications.
            - Click on the expander below to view the dashboard controls.
            """
        )
        with st.expander("**Click for Dashboard Controls**"):
            st.info(
                """- When continuous mode is on, only the chart will be displayed."""
            )
            is_live = st.toggle("**Continuos Mode**", False)

        # Create a placeholder for the chart
        chart_placeholder = st.empty()

        sensor_data = self.get_sensor_data_for_user()
        self.show_notifications(sensor_data)
        # Update the placeholder with the new chart
        chart_placeholder = self.visualize_sensor_data_chart(sensor_data, is_live)

        # Create a placeholder for the elements below the chart
        below_chart_placeholder = st.empty()

        if not is_live:
            with below_chart_placeholder.container():
                with st.expander("**Click for Table View**"):
                    self.visualize_sensor_data_table(sensor_data)

                with st.expander("**Click for Notifications**"):
                    for timestamp, message in reversed(st.session_state.notifications):
                        st.write(f"{timestamp}: {message}")
                    if st.button("Clear Notifications"):
                        st.session_state.notifications = []

        if is_live:
            time.sleep(0.1)
            st.rerun()

    def sidebar(self):
        st.sidebar.write("# Your Account")
        st.sidebar.write(
            f"**Email:** {st.session_state.user_info['fullUserInfo']['users'][0]['email']}"
        )
        if st.sidebar.button("**Sign Out**"):
            session_state_variables = [
                "user_info",
                "valve_state",
                "sensor_data",
                "selected_variables",
                "delete_account_warning_shown",
                "delete_account_clicked",
                "auth_success",
                "auth_warning",
                "auth_error",
                "notifications",
            ]

            for var in session_state_variables:
                try:
                    del st.session_state[var]
                except KeyError:
                    continue
            st.sidebar.success(
                """
                    ##### Signed out successfully.
                    - You have been signed out.
                    - Sign in to access your account.
                    """
            )
            time.sleep(2)
            st.rerun()
        with st.sidebar.expander("**Click for Account Settings**"):
            self.account_settings()
        st.sidebar.info(
            """
            # About
            - Team: [**_Elshad Sabziyev_**](https://github.com/elshadsabziyev), [**_Elvin Mammadov_**](#), and [**_Arif Najafov_**](#).
            - The source code for Dashboard is available on [**_GitHub_**](https://github.com/elshadsabziyev/AgribotDashboard).
            """
        )

    def visualize_sensor_data_table(self, sensor_data):
        col1, col2, col3 = st.columns([5, 30, 5], gap="large")
        if sensor_data:
            # Convert the OrderedDict to a list of dictionaries
            sensor_data_list = list(sensor_data.values())

            sensor_data_df = pd.DataFrame(sensor_data_list)
            sensor_data_df["timestamp"] = pd.to_datetime(
                sensor_data_df["timestamp"], unit="ms"
            )
            with col2:
                st.write(sensor_data_df)
        else:
            st.write("No sensor data available")

    def visualize_sensor_data_chart(self, sensor_data, live=False):
        if live:
            window_size = 100
        else:
            window_size = 1000
        # Check if the session state is already initialized
        if "session_state" not in st.session_state:
            st.session_state["session_state"] = {}

        if not sensor_data:
            st.error("**No sensor data available**")
            return

        # Convert the OrderedDict to a list of dictionaries
        sensor_data_list = list(sensor_data.values())

        if not sensor_data_list:
            st.error("**No sensor data available**")
            return

        sensor_data_df = pd.DataFrame(sensor_data_list)
        sensor_data_df["timestamp"] = pd.to_datetime(
            sensor_data_df["timestamp"], unit="ms"
        )

        # Set the timestamp column as the index
        sensor_data_df.set_index("timestamp", inplace=True)
        if live:
            sensor_data_df = sensor_data_df.tail(window_size)

        filtered_df = sensor_data_df.copy()

        with st.expander("**Click for Filtering Options**"):
            # Add date and time input to select the timeframe
            start_date = st.date_input(
                "**Select start date**", sensor_data_df.index.min().date()
            )
            start_time = st.time_input("**Select start time**", datetime.time(0, 0))

            end_date = st.date_input(
                "**Select end date**", sensor_data_df.index.max().date()
            )
            end_time = st.time_input("**Select end time**", datetime.time(23, 59))

            # Combine date and time inputs to create datetime range
            start_datetime = pd.to_datetime(f"{start_date} {start_time}")
            end_datetime = pd.to_datetime(f"{end_date} {end_time}")

            # Filter dataframe based on selected datetime range
            filtered_df = sensor_data_df.loc[start_datetime:end_datetime]
            # Add checkboxes to select which variables to display
            variable_labels = {
                "water_level": "Water Level",
                "temperature": "Temperature",
                "humidity": "Humidity",
                "moisture": "Moisture",
                # Add more mappings here if necessary
            }
            selected_variables = st.multiselect(
                "**Select Variables**",
                options=[
                    variable_labels.get(option, option)
                    for option in filtered_df.columns.tolist()
                ],
                default=[
                    variable_labels.get(option, option)
                    for option in filtered_df.columns.tolist()
                ],
            )

            # Update the session state with the current state of the multiselect
            st.session_state["session_state"]["selected_variables"] = selected_variables

            # Filter the DataFrame based on the selected variables
            filtered_df = filtered_df.loc[
                :,
                [
                    key
                    for key, value in variable_labels.items()
                    if value in selected_variables
                ],
            ]

            # Add a slider to set the resampling time
            resample_time = st.slider(
                "**Set resampling time (seconds)**",
                min_value=1,
                max_value=50,
                value=25,
            )

        # Check if selected_variables is empty
        if not selected_variables:
            st.info(
                "###### **No variables selected. Please select at least one variable.**"
            )
            return

        # Check if sensor_data_df is empty
        if sensor_data_df.empty:
            st.info("**No data fetched from the server.**")
            return

        # Check if the actual time range is less than the minimum time range required
        if filtered_df.empty or filtered_df.size < 50:
            st.markdown("**Insufficient data for selected range.**")
            st.info(
                f"Available range is from **{sensor_data_df.index.min().strftime('%Y-%m-%d %H:%M')}** to **{(sensor_data_df.index.max() + pd.Timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M')}**"
            )
            return

        # Resample the DataFrame to the selected interval and interpolate missing values
        filtered_df = filtered_df.resample(f"{resample_time}s").mean()

        # Format the index
        filtered_df.index = filtered_df.index.strftime("%d %B, %H:%M:%S")

        # Filter the DataFrame based on the selected variables
        filtered_df = filtered_df.loc[
            :,
            [
                key
                for key, value in variable_labels.items()
                if value in selected_variables
            ],
        ]

        # Check if any toggles are on
        if any(selected_variables):
            st.line_chart(filtered_df)
        else:
            st.empty()

    def account_settings(self):
        with st.form(key="delete_account_form", clear_on_submit=True):
            st.subheader("Delete Account:")
            password = st.text_input("**Enter your password**", type="password")
            submit_button = st.form_submit_button(label="**Confirm Delete Account**")
            if submit_button:
                if st.session_state.get("delete_account_warning_shown", False):
                    with st.spinner("Deleting account"):
                        self.delete_account(password)
                    if "auth_success" in st.session_state:
                        st.success(st.session_state.auth_success)
                        del st.session_state.auth_success
                        time.sleep(2)
                        st.rerun()
                    elif "auth_warning" in st.session_state:
                        st.error(st.session_state.auth_warning)
                        del st.session_state.auth_warning
                    st.session_state.delete_account_clicked = False
                    st.session_state.delete_account_warning_shown = False
                else:
                    st.warning(
                        "Are you sure you want to delete your account? This action cannot be undone!"
                    )
                    st.session_state.delete_account_warning_shown = True
        with st.form(key="Reset", clear_on_submit=True):
            st.subheader("Reset Password:")
            st.info(
                "After clicking the button below, a password reset link will be sent to your email address."
            )
            submit_button = st.form_submit_button(label="**Reset Password**")
            if submit_button:
                with st.spinner("Resetting password"):
                    self.reset_password(
                        st.session_state.user_info["fullUserInfo"]["users"][0]["email"]
                    )
                if "auth_success" in st.session_state:
                    st.success(st.session_state.auth_success)
                    del st.session_state.auth_success
                elif "auth_warning" in st.session_state:
                    st.error(st.session_state.auth_warning)
                    del st.session_state.auth_warning


if __name__ == "__main__":
    app = App()
    app.auth_page()
