import streamlit as st
import datetime
import json
from langchain_community.llms import HuggingFaceHub
from agents.crew_setup import RiskManagementCrew
from utils.pg_database import get_projects, get_project, search_similar_risks
from utils.vector_store import search_risks

llm = HuggingFaceHub(
    repo_id="google/flan-t5-base",
    model_kwargs={"temperature": 0.5, "max_length": 512}
)

def create_chat_interface():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI Project Risk Management Assistant. How can I help you today? You can ask me about project risks, request risk reports, or inquire about specific risk factors."}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about project risks..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = process_query(prompt)
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

def process_query(query):
    try:
        query_lower = query.lower()
        if "status" in query_lower and ("project" in query_lower or "projects" in query_lower):
            return handle_project_status_query(query)
        elif "report" in query_lower or "summary" in query_lower:
            return handle_risk_report_query(query)
        elif "mitigation" in query_lower or "strategies" in query_lower:
            return handle_mitigation_query(query)
        elif "trend" in query_lower or "increasing" in query_lower or "decreasing" in query_lower:
            return handle_risk_trend_query(query)
        else:
            return handle_general_query(query)
    except Exception as e:
        return f"I encountered an error while processing your query: {str(e)}. Could you please rephrase your question?"

def handle_project_status_query(query):
    projects = get_projects()
    project = projects[0] if projects else None
    if not project:
        return "No projects available to analyze."

    prompt = f"What is the current risk status of the project named {project['name']}?"
    return llm.invoke(prompt)

def handle_risk_report_query(query):
    projects = get_projects()
    summary = "Here is the current risk summary across all available projects:

"
    for p in projects:
        summary += f"- **{p['name']}**: Risk Score {p['risk_score']}/10, Status: {p['status']}
"
    return summary

def handle_mitigation_query(query):
    risks = search_similar_risks(query)
    if not risks:
        return "I could not find any matching risks. Please refine your query."
    top_risk = risks[0]
    prompt = f"What are mitigation strategies for the following risk: {top_risk['name']}?

Description: {top_risk['description']}"
    return llm.invoke(prompt)

def handle_risk_trend_query(query):
    projects = get_projects()
    trends = "Risk trend analysis:

"
    for p in projects:
        delta = p.get('risk_delta', 0)
        if delta > 0:
            trend = "⬆️ Increasing"
        elif delta < 0:
            trend = "⬇️ Decreasing"
        else:
            trend = "⏸ Stable"
        trends += f"- **{p['name']}**: {trend} (Δ{delta})
"
    return trends

def handle_general_query(query):
    memory = search_risks(query)
    prompt = f"Context: {memory}

Answer this user query about project risk management: {query}"
    return llm.invoke(prompt)