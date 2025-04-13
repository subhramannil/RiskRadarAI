import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.pg_database import get_project, get_projects

def create_risk_trend_chart(project):
    """Create a line chart showing risk score trends over time for a project"""
    
    if 'risk_history' not in project or not project['risk_history']:
        st.info("No risk history data available for this project.")
        return None
    
    # Create dataframe from risk history
    df = pd.DataFrame(project['risk_history'])
    
    # Create the line chart
    fig = go.Figure()
    
    # Add the main risk score line
    fig.add_trace(
        go.Scatter(
            x=df['date'], 
            y=df['risk_score'], 
            mode='lines+markers', 
            name='Risk Score',
            line=dict(color='#FF5757', width=3),
            marker=dict(size=8)
        )
    )
    
    # Add threshold line for high risk
    fig.add_hline(
        y=7, 
        line_width=2, 
        line_dash="dash", 
        line_color="red",
        annotation_text="High Risk Threshold",
        annotation_position="top right"
    )
    
    # Add threshold line for medium risk
    fig.add_hline(
        y=4, 
        line_width=2, 
        line_dash="dash", 
        line_color="orange",
        annotation_text="Medium Risk Threshold",
        annotation_position="top right"
    )
    
    # Update layout
    fig.update_layout(
        title=f"Risk Score Trend: {project['name']}",
        xaxis_title="Date",
        yaxis_title="Risk Score",
        yaxis=dict(range=[0, 10]),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_risk_matrix(project):
    """Create a risk matrix visualization (impact vs. likelihood)"""
    
    if 'risk_factors' not in project or not project['risk_factors']:
        st.info("No risk factors available to create a risk matrix.")
        return None
    
    # Create dataframe from risk factors
    risk_factors = []
    for factor in project['risk_factors']:
        if 'impact' in factor and 'likelihood' in factor:
            risk_factors.append({
                'name': factor['name'],
                'impact': factor['impact'],
                'likelihood': factor['likelihood'],
                'category': factor.get('category', 'Uncategorized'),
                'description': factor['description']
            })
    
    if not risk_factors:
        st.info("Risk factors do not contain impact and likelihood data.")
        return None
    
    df = pd.DataFrame(risk_factors)
    
    # Create a bubble size based on impact * likelihood
    df['risk_score'] = df['impact'] * df['likelihood'] / 10
    
    # Create text for hover labels
    df['hover_text'] = df.apply(
        lambda row: f"Risk: {row['name']}<br>" +
                    f"Impact: {row['impact']}/10<br>" +
                    f"Likelihood: {row['likelihood']}/10<br>" +
                    f"Score: {row['risk_score']:.1f}/10<br>" +
                    f"Category: {row['category'].replace('_', ' ').title()}<br>" +
                    f"Description: {row['description']}",
        axis=1
    )
    
    # Create color mapping for categories
    category_colors = {
        'schedule_risk': '#FF9E3D',
        'budget_risk': '#5DA5DA', 
        'resource_risk': '#FAA43A',
        'market_risk': '#60BD68',
        'technical_risk': '#F15854',
        'Uncategorized': '#B276B2'
    }
    
    # Normalize category names for display
    df['category_display'] = df['category'].apply(
        lambda x: x.replace('_', ' ').title() if isinstance(x, str) else 'Uncategorized'
    )
    
    # Create the risk matrix
    fig = px.scatter(
        df,
        x='likelihood',
        y='impact',
        size='risk_score',
        color='category_display',
        hover_name='name',
        text='name',
        custom_data=['hover_text'],
        labels={
            'likelihood': 'Likelihood (1-10)',
            'impact': 'Impact (1-10)',
            'category_display': 'Risk Category'
        },
        title=f'Risk Matrix: {project["name"]}',
        size_max=30
    )
    
    # Define the background areas (Low, Medium, High risk)
    # Create coordinates for risk regions
    low_risk_x = [0, 0, 4, 7, 4, 0]
    low_risk_y = [0, 4, 4, 0, 0, 0]
    
    medium_risk_x = [0, 0, 7, 10, 7, 4, 0]
    medium_risk_y = [4, 7, 7, 0, 0, 4, 4]
    
    high_risk_x = [0, 0, 10, 10, 7, 7, 4, 0]
    high_risk_y = [7, 10, 10, 0, 0, 7, 7, 7]
    
    # Add colored background regions
    fig.add_trace(
        go.Scatter(
            x=low_risk_x, y=low_risk_y,
            fill="toself",
            fillcolor="rgba(144, 238, 144, 0.3)",
            line=dict(color="rgba(144, 238, 144, 0)"),
            name="Low Risk",
            hoverinfo="skip"
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=medium_risk_x, y=medium_risk_y,
            fill="toself",
            fillcolor="rgba(255, 165, 0, 0.3)",
            line=dict(color="rgba(255, 165, 0, 0)"),
            name="Medium Risk",
            hoverinfo="skip"
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=high_risk_x, y=high_risk_y,
            fill="toself",
            fillcolor="rgba(255, 0, 0, 0.3)",
            line=dict(color="rgba(255, 0, 0, 0)"),
            name="High Risk",
            hoverinfo="skip"
        )
    )
    
    # Update layout and traces
    fig.update_traces(
        marker=dict(sizemin=7, sizeref=0.1),
        mode='markers+text',
        textposition='top center',
        textfont=dict(size=9)
    )
    
    fig.update_layout(
        xaxis=dict(title='Likelihood (1-10)', range=[0, 10], dtick=1),
        yaxis=dict(title='Impact (1-10)', range=[0, 10], dtick=1),
        hovermode='closest',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_risk_radar_chart(project):
    """Create a radar chart showing risk by category"""
    
    # Risk categories to display
    risk_categories = [
        'schedule_risk', 
        'budget_risk', 
        'resource_risk', 
        'market_risk', 
        'technical_risk'
    ]
    
    # Get values for each category
    values = []
    for category in risk_categories:
        values.append(project.get(category, 0))
    
    # Format category names for display
    categories = [cat.replace('_', ' ').title() for cat in risk_categories]
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line=dict(color='#FF5757'),
        fillcolor='rgba(255, 87, 87, 0.3)',
        name='Risk Level'
    ))
    
    # Add threshold for high risk
    fig.add_trace(go.Scatterpolar(
        r=[7, 7, 7, 7, 7],
        theta=categories,
        line=dict(color='red', dash='dash'),
        fill=None,
        name='High Risk Threshold'
    ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        title=f"Risk Categories: {project['name']}",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def visualize_project_risks(project, container=None):
    """Create and display a comprehensive set of risk visualizations for a project"""
    target = container if container else st
    
    target.header(f"Risk Visualizations: {project['name']}")
    
    # Risk score trend chart
    target.subheader("Risk Score Trend")
    trend_chart = create_risk_trend_chart(project)
    if trend_chart:
        target.plotly_chart(trend_chart, use_container_width=True)
    
    # Risk matrix
    col1, col2 = target.columns(2)
    
    with col1:
        st.subheader("Risk Matrix (Impact vs. Likelihood)")
        matrix = create_risk_matrix(project)
        if matrix:
            st.plotly_chart(matrix, use_container_width=True)
    
    with col2:
        st.subheader("Risk Categories")
        radar = create_risk_radar_chart(project)
        st.plotly_chart(radar, use_container_width=True)
    
    # Display detailed risk factors
    if 'risk_factors' in project and project['risk_factors']:
        target.subheader("Risk Factors")
        
        # Sort risk factors by impact * likelihood
        sorted_factors = sorted(
            project['risk_factors'],
            key=lambda x: x.get('impact', 0) * x.get('likelihood', 0),
            reverse=True
        )
        
        for i, factor in enumerate(sorted_factors):
            with target.expander(f"{i+1}. {factor['name']} (Impact: {factor.get('impact', 'N/A')}/10, Likelihood: {factor.get('likelihood', 'N/A')}/10)"):
                st.write(f"**Description:** {factor['description']}")
                st.write(f"**Category:** {factor.get('category', 'Uncategorized').replace('_', ' ').title()}")
                st.write(f"**Mitigation Strategy:** {factor.get('mitigation', 'No mitigation strategy provided')}")

def visualize_portfolio_risks(projects, container=None):
    """Create and display portfolio-level risk visualizations"""
    target = container if container else st
    
    target.header("Portfolio Risk Visualization")
    
    # Create dataframe for all projects
    df = pd.DataFrame([
        {
            'name': p['name'],
            'id': p['id'],
            'risk_score': p['risk_score'],
            'schedule_risk': p.get('schedule_risk', 0),
            'budget_risk': p.get('budget_risk', 0),
            'resource_risk': p.get('resource_risk', 0),
            'market_risk': p.get('market_risk', 0),
            'technical_risk': p.get('technical_risk', 0),
            'budget': p.get('budget', 0),
            'status': p['status']
        }
        for p in projects
    ])
    
    # Risk scatter plot
    target.subheader("Project Risk Assessment")
    fig = create_risk_bubble_chart(df)
    target.plotly_chart(fig, use_container_width=True)
    
    # Risk category comparison
    target.subheader("Risk Category Comparison")
    category_fig = create_risk_category_comparison(df)
    target.plotly_chart(category_fig, use_container_width=True)

def create_risk_bubble_chart(df):
    """Create a bubble chart visualization of project risks"""
    
    # Add hover text
    df['hover_text'] = df.apply(
        lambda row: f"Project: {row['name']}<br>" +
                    f"Risk Score: {row['risk_score']:.1f}/10<br>" +
                    f"Schedule Risk: {row['schedule_risk']:.1f}/10<br>" +
                    f"Budget Risk: {row['budget_risk']:.1f}/10<br>" +
                    f"Resource Risk: {row['resource_risk']:.1f}/10<br>" +
                    f"Market Risk: {row['market_risk']:.1f}/10",
        axis=1
    )
    
    # Create size values proportional to budget
    max_budget = df['budget'].max()
    df['size'] = df['budget'] / max_budget * 50 + 20 if max_budget > 0 else 30
    
    # Create the figure
    fig = go.Figure()
    
    # Add a trace for each status category
    for status in df['status'].unique():
        subset = df[df['status'] == status]
        
        color = 'red' if status == 'At Risk' else 'orange' if status == 'In Progress' else 'green' if status == 'On Track' else 'blue'
        
        fig.add_trace(go.Scatter(
            x=subset['market_risk'],
            y=subset['technical_risk'],
            mode='markers+text',
            marker=dict(
                size=subset['size'],
                color=color,
                opacity=0.7,
                line=dict(color='white', width=1)
            ),
            text=subset['name'],
            textposition='top center',
            name=status,
            customdata=subset['hover_text'],
            hovertemplate='%{customdata}<extra></extra>'
        ))
    
    # Update layout
    fig.update_layout(
        xaxis=dict(title='Market Risk', range=[0, 10]),
        yaxis=dict(title='Technical Risk', range=[0, 10]),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Add quadrant lines
    fig.add_hline(y=7, line_dash="dash", line_color="red")
    fig.add_vline(x=7, line_dash="dash", line_color="red")
    
    return fig

def create_risk_category_comparison(df):
    """Create a comparison of risk categories across all projects"""
    
    # Melt the dataframe to get risk categories in one column
    risk_categories = ['schedule_risk', 'budget_risk', 'resource_risk', 'market_risk', 'technical_risk']
    
    # Ensure all categories exist
    for cat in risk_categories:
        if cat not in df.columns:
            df[cat] = 0
    
    melted_df = pd.melt(
        df,
        id_vars=['name', 'risk_score'],
        value_vars=risk_categories,
        var_name='risk_category',
        value_name='category_score'
    )
    
    # Format category names for display
    melted_df['risk_category'] = melted_df['risk_category'].apply(lambda x: x.replace('_', ' ').title())
    
    # Create the group bar chart
    fig = px.bar(
        melted_df,
        x='name',
        y='category_score',
        color='risk_category',
        barmode='group',
        labels={
            'name': 'Project',
            'category_score': 'Risk Score (0-10)',
            'risk_category': 'Risk Category'
        },
        title='Risk Category Comparison Across Projects'
    )
    
    # Add a horizontal line for high risk threshold
    fig.add_hline(
        y=7,
        line_dash="dash",
        line_color="red",
        annotation_text="High Risk Threshold",
        annotation_position="top right"
    )
    
    # Update layout
    fig.update_layout(
        xaxis_tickangle=-45,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig