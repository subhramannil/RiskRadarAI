import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime
from utils.pg_database import get_projects, get_risk_factors

def create_dashboard(projects):
    """Create the main risk dashboard display"""
    
    if not projects:
        st.warning("No projects found in the database.")
        return
    
    # Convert projects to dataframe for easier manipulation
    df = pd.DataFrame(projects)
    
    # Dashboard layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Project Risk Overview")
        
        # Create risk scatter plot
        fig = create_risk_scatter_plot(df)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Risk Alert Summary")
        
        # Show high risk projects
        high_risk_projects = df[df['risk_score'] >= 7].sort_values('risk_score', ascending=False)
        if not high_risk_projects.empty:
            for _, project in high_risk_projects.iterrows():
                with st.container(border=True):
                    st.markdown(f"**{project['name']}** 🔴")
                    st.markdown(f"Risk Score: **{project['risk_score']}/10**")
                    
                    # Show risk trend if available
                    if 'risk_delta' in project:
                        delta = project['risk_delta']
                        if delta > 0:
                            st.markdown(f"Trend: ⬆️ +{delta}")
                        elif delta < 0:
                            st.markdown(f"Trend: ⬇️ {delta}")
                        else:
                            st.markdown("Trend: ➡️ No change")
        else:
            st.info("No high-risk projects at this time.")
    
    # Risk metrics row
    st.subheader("Risk Metrics by Category")
    create_risk_category_charts(df)
    
    # Project details
    st.subheader("Project Details")
    create_project_table(df)
    
    # Risk factors section
    st.subheader("Top Risk Factors")
    create_risk_factors_section(projects)

def create_risk_scatter_plot(df):
    """Create a scatter plot of projects by risk score and budget"""
    
    # Add a size column for budget (handling missing values)
    df['budget_size'] = df['budget'].fillna(0) / 10000  # Adjust for visualization
    
    # Add hover text
    df['hover_text'] = df.apply(
        lambda row: f"Project: {row['name']}<br>" +
                    f"Risk Score: {row['risk_score']}/10<br>" +
                    f"Status: {row['status']}<br>" +
                    f"Budget: ${row.get('budget', 0):,.0f}<br>" +
                    f"Timeline: {row.get('start_date', 'N/A')} to {row.get('end_date', 'N/A')}",
        axis=1
    )
    
    # Create color mapping for status
    status_colors = {'At Risk': 'red', 'In Progress': 'orange', 'On Track': 'green', 'Planning': 'blue'}
    
    # Create the scatter plot
    fig = px.scatter(
        df,
        x='risk_score',
        y='budget',
        size='budget_size',
        color='status',
        color_discrete_map=status_colors,
        hover_name='name',
        hover_data={'budget_size': False, 'risk_score': True, 'budget': True, 'status': True},
        text='name',
        custom_data=['id', 'hover_text'],
        title='Project Risk Assessment'
    )
    
    # Update layout
    fig.update_traces(
        marker=dict(sizemin=10),
        mode='markers+text',
        textposition='top center',
        textfont=dict(size=10)
    )
    
    fig.update_layout(
        xaxis=dict(title='Risk Score (0-10)', range=[0, 10]),
        yaxis=dict(title='Budget ($)', tickformat='$,.0f'),
        hovermode='closest',
        showlegend=True
    )
    
    # Add a vertical line to indicate high risk threshold
    fig.add_vline(x=7, line_width=1, line_dash="dash", line_color="red")
    
    return fig

def create_risk_category_charts(df):
    """Create charts showing risk breakdown by category"""
    
    # Initialize the columns for all categories to ensure consistent data
    risk_categories = ['schedule_risk', 'budget_risk', 'resource_risk', 'market_risk']
    for category in risk_categories:
        if category not in df.columns:
            df[category] = 0
    
    # Calculate averages
    avg_risks = {
        'Schedule Risk': df['schedule_risk'].mean(),
        'Budget Risk': df['budget_risk'].mean(),
        'Resource Risk': df['resource_risk'].mean(),
        'Market Risk': df['market_risk'].mean()
    }
    
    # Create columns for charts
    cols = st.columns(len(risk_categories))
    
    for i, (category_name, risk_value) in enumerate(avg_risks.items()):
        with cols[i]:
            # Create gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_value,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': category_name},
                gauge={
                    'axis': {'range': [0, 10]},
                    'bar': {'color': "gray"},
                    'steps': [
                        {'range': [0, 3.9], 'color': "green"},
                        {'range': [4, 6.9], 'color': "orange"},
                        {'range': [7, 10], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 7
                    }
                }
            ))
            
            fig.update_layout(height=150, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig, use_container_width=True)

def create_project_table(df):
    """Create an interactive table of projects with risk information"""
    
    # Ensure necessary columns exist and create the display dataframe
    display_columns = ['name', 'status', 'risk_score', 'schedule_risk', 
                       'budget_risk', 'resource_risk', 'market_risk', 'start_date', 'end_date']
    
    # Create a copy to avoid modifying the original
    display_df = df.copy()
    
    # Ensure all columns exist by adding missing ones with N/A
    for col in display_columns:
        if col not in display_df.columns:
            display_df[col] = 'N/A'
    
    # Select and rename columns for display
    display_df = display_df[display_columns].rename(columns={
        'name': 'Project Name',
        'status': 'Status',
        'risk_score': 'Overall Risk',
        'schedule_risk': 'Schedule Risk',
        'budget_risk': 'Budget Risk', 
        'resource_risk': 'Resource Risk',
        'market_risk': 'Market Risk',
        'start_date': 'Start Date',
        'end_date': 'End Date'
    })
    
    # Style the dataframe
    def highlight_risk(val):
        """Highlight risk scores based on severity"""
        try:
            val = float(val)
            if val >= 7:
                return 'background-color: #ffcccc'
            elif val >= 4:
                return 'background-color: #ffe0b3'
            else:
                return 'background-color: #d6f5d6'
        except:
            return ''
    
    # Apply styling and display
    styled_df = display_df.style.map(
        highlight_risk, 
        subset=['Overall Risk', 'Schedule Risk', 'Budget Risk', 'Resource Risk', 'Market Risk']
    )
    
    st.dataframe(styled_df, use_container_width=True)

def create_risk_factors_section(projects):
    """Create a section showing top risk factors across projects"""
    
    # Extract risk factors from all projects
    all_risk_factors = []
    
    for project in projects:
        if 'risk_factors' in project and project['risk_factors']:
            for factor in project['risk_factors']:
                factor_copy = factor.copy()
                factor_copy['project_name'] = project['name']
                factor_copy['project_id'] = project['id']
                # Calculate a score for sorting
                factor_copy['risk_score'] = (factor.get('impact', 5) * factor.get('likelihood', 5)) / 10
                all_risk_factors.append(factor_copy)
    
    if not all_risk_factors:
        st.info("No risk factors found for any projects.")
        return
    
    # Sort by combined impact and likelihood
    sorted_factors = sorted(all_risk_factors, key=lambda x: x.get('risk_score', 0), reverse=True)
    
    # Display top factors
    top_factors = sorted_factors[:5]  # Show top 5 factors
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Create a bar chart of top risk factors
        factor_df = pd.DataFrame(top_factors)
        
        fig = px.bar(
            factor_df, 
            x='risk_score', 
            y='name',
            orientation='h',
            color='risk_score',
            color_continuous_scale='Reds',
            labels={
                'risk_score': 'Risk Score',
                'name': 'Risk Factor'
            },
            title='Top Risk Factors'
        )
        
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Display detailed information about top factors
        for i, factor in enumerate(top_factors):
            with st.expander(f"{i+1}. {factor['name']} (Score: {factor['risk_score']:.1f})"):
                st.write(f"**Project:** {factor['project_name']}")
                st.write(f"**Category:** {factor.get('category', 'Uncategorized').replace('_', ' ').title()}")
                st.write(f"**Description:** {factor['description']}")
                st.write(f"**Impact:** {factor.get('impact', 'N/A')}/10 | **Likelihood:** {factor.get('likelihood', 'N/A')}/10")
                st.write(f"**Mitigation Strategy:** {factor.get('mitigation', 'No mitigation strategy provided.')}")