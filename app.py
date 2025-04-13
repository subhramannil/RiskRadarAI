import streamlit as st
import os
from components.chat_interface import create_chat_interface
from components.dashboard import create_dashboard
from utils.pg_database import initialize_database, get_projects

# Set page config
st.set_page_config(
    page_title="AI Project Risk Management System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Initialize the database
initialize_database()
# Sidebar
st.sidebar.title("AI Project Risk Management")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/5726/5726532.png", width=100)
# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Chat Interface", "Project Details", "Settings"]
)
# Display selected page
if page == "Dashboard":
    st.title("Project Risk Dashboard")
    projects = get_projects()
    create_dashboard(projects)

elif page == "Chat Interface":
    st.title("Risk Management Assistant")
    create_chat_interface()

elif page == "Project Details":
    st.title("Project Details")
    projects = get_projects()

    if not projects:
        st.warning("No projects available in the database.")
    else:
        selected_project = st.selectbox(
            "Select a project",
            options=[project["name"] for project in projects],
            key="project_selector"
        )

        # Get selected project details
        selected_project_details = next((p for p in projects if p["name"] == selected_project), None)

        if selected_project_details:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Project Information")
                st.write(f"**ID:** {selected_project_details['id']}")
                st.write(f"**Name:** {selected_project_details['name']}")
                st.write(f"**Description:** {selected_project_details['description']}")
                st.write(f"**Status:** {selected_project_details['status']}")
                st.write(f"**Start Date:** {selected_project_details['start_date']}")
                st.write(f"**End Date:** {selected_project_details['end_date']}")
                st.write(f"**Budget:** ${selected_project_details['budget']:,}")

            with col2:
                st.subheader("Risk Metrics")
                # Risk indicators
                st.metric(
                    label="Overall Risk Score",
                    value=f"{selected_project_details.get('risk_score', 0)}/10",
                    delta=selected_project_details.get('risk_delta', 0)
                )

                # Risk categories
                risk_categories = {
                    "Schedule Risk": selected_project_details.get('schedule_risk', 0),
                    "Budget Risk": selected_project_details.get('budget_risk', 0),
                    "Resource Risk": selected_project_details.get('resource_risk', 0),
                    "Market Risk": selected_project_details.get('market_risk', 0),
                }

                for category, score in risk_categories.items():
                    st.write(f"**{category}:** {score}/10")

            # Risk history
            st.subheader("Risk History")
            if 'risk_history' in selected_project_details and selected_project_details['risk_history']:
                # Create risk history visualization
                import plotly.graph_objects as go
                import pandas as pd

                df = pd.DataFrame(selected_project_details['risk_history'])
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df['date'], y=df['risk_score'], mode='lines+markers', name='Risk Score'))
                fig.update_layout(
                    title='Risk Score Trend',
                    xaxis_title='Date',
                    yaxis_title='Risk Score',
                    yaxis=dict(range=[0, 10])
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No risk history available for this project.")

            # Risk factors
            st.subheader("Risk Factors")
            if 'risk_factors' in selected_project_details and selected_project_details['risk_factors']:
                for factor in selected_project_details['risk_factors']:
                    with st.expander(f"{factor['name']} - Impact: {factor['impact']}/10"):
                        st.write(f"**Description:** {factor['description']}")
                        st.write(f"**Mitigation Strategy:** {factor['mitigation']}")
            else:
                st.info("No risk factors identified for this project.")

elif page == "Settings":
    st.title("Settings")

    # General Settings
    st.subheader("General Settings")

    # Risk threshold settings
    risk_threshold = st.slider(
        "Risk Alert Threshold (0-10)",
        min_value=0,
        max_value=10,
        value=7,
        help="Send alerts when risk score exceeds this threshold"
    )

    # Notification settings
    st.subheader("Notification Settings")
    email_notifications = st.checkbox("Email Notifications", value=True)

    if email_notifications:
        notification_email = st.text_input("Notification Email", value="")

    # API Connections
    st.subheader("External Data Sources")

    col1, col2 = st.columns(2)
    with col1:
        market_data_source = st.selectbox(
            "Market Data Source",
            ["Alpha Vantage", "Yahoo Finance", "Bloomberg", "Custom API"]
        )

    with col2:
        update_frequency = st.selectbox(
            "Update Frequency",
            ["Hourly", "Daily", "Weekly"]
        )

    # Save settings
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2025 AI Project Risk Management")