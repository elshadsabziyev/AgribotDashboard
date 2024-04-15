# Agribot365 - Dashboard

## Table of Contents

- [Agribot365 - Dashboard](#agribot365---dashboard)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Technologies](#technologies)
  - [Installation](#installation)
  - [Local Usage](#local-usage)
  - [Cloud Deployment](#cloud-deployment)
  - [Usage](#usage)
  - [Deployment (If you want to deploy it on your own server or Streamlit Sharing)](#deployment-if-you-want-to-deploy-it-on-your-own-server-or-streamlit-sharing)
  - [Architecture](#architecture)
      - [Codebase Structure:](#codebase-structure)
  - [Roadmap](#roadmap)
      - [Short-term goals:](#short-term-goals)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

**AgriBot365** is a cutting-edge smart farming and IoT project aimed at revolutionizing agricultural practices. This repository houses the frontend component, responsible for displaying real-time sensor data and providing an interactive dashboard for farmers to monitor and manage their operations. 

The backend component, implemented using **Arduino sensors**, **Raspberry Pi**, and **Firebase Realtime Database**, collects and stores essential environmental data from the farm. The frontend component, built with **Streamlit**, provides a user-friendly interface for farmers to access and analyze this data.

For the backend/hardware component, which includes the Arduino sensors, Raspberry Pi, and Firebase Realtime Database integration, please refer to the [**AgriBot365 Backend Repository**](example.com).

## Features

- **User Authentication:** Secure login and registration system powered by Firebase Authentication.
- **Real-time Sensor Data Visualization:** Interactive charts and tables displaying live data from temperature, humidity, moisture, and water level sensors.
- **Notifications and Alerts:** Smart notifications and alerts for critical conditions, such as low water levels or suboptimal environmental parameters.
- **Responsive Design:** Optimized for various devices and screen sizes.

## Technologies

AgriBot365 leverages the following technologies:

- **Python:** The primary programming language used for the frontend application.
- **Streamlit:** A powerful Python library for building interactive web applications.
- **Firebase Authentication:** Secure authentication and user management system.
- **Firebase Realtime Database:** Real-time, cloud-hosted database for storing and syncing sensor data.
- **Pandas:** Data manipulation and analysis library for Python.

## Installation

To set up and run AgriBot365 locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/elshadsabziyev/AgribotDashboard.git
    ```
2. **Navigate to the project directory:**
    ```bash
    cd Agribot365
    ```
3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
## Local Usage
1. **Get Firebase Config:**
    - Create a new Firebase project on the Firebase Console.
    - Enable the Firebase Authentication and Realtime Database services.
    - Go to Project Settings, go down to the "Your apps" section, and click on the "Web" app to get your Firebase configuration details.
    - Create a new file named `secret.toml` under the `.streamlit` directory and add your Firebase configuration details in the following format:
    ```toml
    [firebase_config]
    apiKey = "YOUR_API_KEY"
    authDomain = "YOUR_AUTH_DOMAIN"
    databaseURL = "YOUR_DATABASE_URL"
    projectId = "YOUR_PROJECT_ID"
    storageBucket = "YOUR_STORAGE_BUCKET"
    messagingSenderId = "YOUR_MESSAGING_SENDER_ID"
    appId = "YOUR_APP_ID"
    measurementId = "YOUR_MEASUREMENT_ID"
    ```

2. **Get Firebase Admin SDK Credentials:**
    - Go to Project Settings, Service Accounts, and click on "Generate new private key" to download the Firebase Admin SDK credentials JSON file.
    - Open the downloaded JSON file and copy its contents.
    - Go to [ConvertSimple](https://www.convertsimple.com/convert-json-to-toml/) and convert the JSON content to TOML format.
    - Open the `secret.toml` file and add the converted TOML content under the `[firebase_auth]` section:
    ```toml
    [firebase_auth]
    type = "service_account"
    project_id = "YOUR_PROJECT_ID"
    private_key_id = "YOUR_PRIVATE_KEY_ID"
    private_key = "YOUR_PRIVATE_KEY"
    client_email = "YOUR_CLIENT_EMAIL"
    client_id = "YOUR_CLIENT_ID"
    auth_uri = "YOUR_AUTH_URI"
    token_uri = "YOUR_TOKEN_URI"
    auth_provider_x509_cert_url = "YOUR_AUTH_PROVIDER"
    client_x509_cert_url = "YOUR_CLIENT_CERT_URL"
    universe_domain =  "YOUR_DOMAIN"
    ```
3. **Set up Firebase Realtime Database:**
    - Create a new Realtime Database on the Firebase Console.
    - Select the "Start in test mode" option to allow read and write access to all users.
    - Set up the necessary rules and permissions for reading and writing data.
    - Recommended rules for testing purposes on Local Deployment (If you select "Start in test mode" option, these rules will be automatically set):
    ```json
    {
      "rules": {
        ".read": true,
        ".write": true
      }
    }
    ```
4. **Set up Firebase Authentication:**
    - Go to the Firebase Console and from the left sidebar, click on "Authentication".
    - Click on the "Sign-in method" tab and enable the "Email/Password" sign-in provider.
    - Go to the "Templates" tab and set up the email verification template (optional).

5. **Configure OpenAI API key: (Optional)**
    - Sign up for an OpenAI API key on the OpenAI website.
    - Update the `secret.toml` file with your OpenAI API key:
    ```toml
    [openai]
    openai_api_key = "YOUR_OPENAI_API_KEY"
    ```
    > Note: The OpenAI API key is optional and can be used to access advanced AI-powered insights and summaries in the application. These features haven't been implemented yet, but the configuration is provided for future enhancements.
6. **Run the application:**
    ```bash
    streamlit run app.py
    ```
7. **Access the application:** Open your web browser and navigate to the provided URL (e.g., http://localhost:8501) to access the AgriBot365 dashboard.


## Cloud Deployment

> Steps from 1 to 5 are the same as Local Deployment. Skip to Step 6 if you have already completed these steps.


1. **Set up a GitHub repository:**
    - Go to [GitHub](https://github.com/) and create a new repository for your AgriBot365 project.
    - Push your local codebase to the GitHub repository (Or you can fork this repository and use it as your own).
    - Make sure your repository contains the necessary files, including `requirements.txt`, and the `.streamlit` directory with the `secret.toml` file.
    - Add a `.gitignore` file to exclude sensitive files and directories from version control.
    - Commit and push your changes to the repository.
2. **Deploy the application on Streamlit Sharing:**
    - Go to [share.streamlit.io](https://share.streamlit.io/) to deploy your Streamlit application.
    - Sign in with your GitHub account.
    - Click on the "New app" button to create a new deployment.
    - Connect your GitHub repository to Streamlit Sharing.
    - Select the branch containing your Streamlit application code.
    - Click on the "Deploy" button to start the deployment process.
    - Once the deployment is complete, you will receive a unique URL for your AgriBot365 dashboard.
    - In application settings, go to secrets, copy the content of `secret.toml` and paste it in the secrets section.
    - Click on the "Open app" button to access your deployed AgriBot365 dashboard.
    - You can share the URL with others to allow them to access the dashboard.

3. **Update the Firebase Realtime Database rules: (optional, but strongly recommended)**
    - Go to the Firebase Console and update the Realtime Database rules to restrict access to authorized users only.
    - Recommended rules for production deployment:
    ```json
    {
    "rules":{
        "users":{
            "$uid":{
                ".read":"auth != null && auth.uid === $uid",
                ".write":"auth != null && auth.uid === $uid"
                }
            }
        }
    }
    ```

## Usage

Once the application is running, you can access the AgriBot365 dashboard by navigating to the provided URL. Follow these steps to get started:

1. **Sign up or Log in:**
    - If you're a new user, click the "Register" button and follow the prompts to create a new account.
    - If you already have an account, click the "Login" button and enter your credentials.
2. **Explore the Dashboard:**
    - The main dashboard displays real-time sensor data from your farm in the form of interactive charts and tables.
    - Use the filtering and sorting options to focus on specific data ranges or variables of interest.
3. **Manage Notifications and Alerts:**
    - Configure custom thresholds and alert levels for critical parameters, such as water levels or temperature ranges.
    - Receive real-time notifications and alerts when these thresholds are breached.
4. **Analyze AI-Powered Insights: (Coming Soon)**
    - Access concise summaries and insights generated by OpenAI's language models, providing valuable intelligence about your farm's conditions.
> Note: Don't know if you noticed, but this is just a frontend part of the project. So, if you set everything up correctly, you will see warnings about missing data. To get the full experience, you need to set up the backend part of the project. You can find the backend part of the project [here](example.com). Also, you can just throw this dummy data into the Firebase Realtime Database to see how it works.
> Dummy Data:
```json
{
  "sensors": {
    "temperature": 25.5,
    "humidity": 60.0,
    "moisture": 40.0,
    "water_level": 70.0
  }
  "valve_status": "open",
}
```
For detailed instructions, troubleshooting tips, and advanced configuration options, please refer to the project's comprehensive documentation. LOL, just kidding, there is no documentation. But you can always reach out to me if you have any questions or need help with the project.

## Deployment (If you want to deploy it on your own server or Streamlit Sharing)

AgriBot365 can be deployed on various platforms, including cloud services and on-premises servers. Here are the general steps for deploying the application:

1. **Choose a deployment platform:**
    - Cloud platforms: AgriBot365 can be deployed on popular cloud platforms such as AWS, Google Cloud Platform (GCP), or Microsoft Azure.
    - On-premises servers: For self-hosted deployments, you can set up AgriBot365 on your own servers or private infrastructure.
2. **Set up the deployment environment:**
    - Install the required dependencies and configure the necessary services (e.g., web server, database, authentication provider) on the target deployment platform.
    - Configure the appropriate environment variables and secrets (e.g., Firebase credentials, OpenAI API key) for the deployment environment.
3. **Build and package the application:**
    - Use a suitable build tool (e.g., PyInstaller, Docker) to package the AgriBot365 codebase and its dependencies into a deployable artifact.
4. **Deploy the application:**
    - Follow the specific deployment instructions for your chosen platform (e.g., deploying to a cloud service, setting up a web server, configuring load balancing, etc.).
    - Monitor the application's logs and performance, and make necessary adjustments as needed.
> Note: The deployment process may vary depending on the target platform and deployment strategy. Consult the platform-specific documentation and resources for detailed instructions. Personally, I recommend using Streamlit Sharing for quick and easy deployment of Streamlit applications. 

## Architecture

AgriBot365 follows a client-server architecture, with the frontend interacting with the backend services through APIs. The key components include:

- **Python:** The primary programming language used for the frontend application.
- **Streamlit:** A powerful Python library for building interactive web applications.
- **Firebase Authentication:** Secure authentication and user management system.
- **Firebase Realtime Database:** Real-time, cloud-hosted database for storing and syncing sensor data.
- **Pandas:** Data manipulation and analysis library for Python.

#### Codebase Structure:

- **`app.py`:** The main application file containing the Streamlit code for the AgriBot365 dashboard.
- **`credential_loader.py`** A utility module for loading Firebase credentials from the `secret.toml` file.
- **`realtimedb.py`** A module for interacting with the Firebase Realtime Database.
- **`auth.py`** A module for handling user authentication and registration.

The codebase is organized into modules and functions to facilitate code readability, maintainability, and extensibility. Each module is responsible for a specific aspect of the application, such as data visualization, user authentication, or database interactions.

## Roadmap

AgriBot365 is an evolving project, and future enhancements and features are planned:

#### Short-term goals:
- **AI-Powered Insights:** Integration with OpenAI's language models to provide advanced data analysis and insights.
  > Note: Nowadays, everyone is talking about AI, so I thought it would be cool to add some AI-powered features to the dashboard. Probably is not going to be very useful, but it will look cool.
- **Enhanced User Interface:** Improvements to the dashboard layout, design, and user experience.
  > Note: The current version of the dashboard provides basic functionality and may benefit from additional styling and interactive elements. However, the core features are functional and provide a solid foundation for future enhancements. To be honest, I am not a front-end developer, so I would appreciate any help in this area. Considering limitations of Streamlit, I am planning to move to Flutte... haha, just kidding.

- **Refreshing Auth Tokens:** Implementing token refresh logic for Firebase Authentication.
  > Note: Currently, the application does not handle token refreshes, which may lead to authentication issues after the token expires.

- **Improved Data Visualization:** Enhancements to the data visualization components, including additional charts, graphs, and data analysis tools.
  > Note: The current version of the dashboard provides basic data visualization capabilities. Future enhancements may include more advanced chart types, interactive elements, and better real-time updates (Note: Streamlit does not support real-time updates out of the box, so this may require additional workarounds or integrations).
- **And more...**
  - Integration with additional data sources and sensor types.
  - Advanced data analysis and predictive modeling capabilities.
  - Mobile application development for on-the-go monitoring.
  - Improved scalability and performance optimizations.
  - Community contributions and feedback.
  - And more...

## Contributing

Contributions to AgriBot365 are welcome! If you'd like to contribute, please follow these steps:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and commit them with descriptive commit messages.
- Push your changes to your forked repository.
- Submit a pull request, detailing the changes you've made.

## License

AgriBot365 is released under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more details.