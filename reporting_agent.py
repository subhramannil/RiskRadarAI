import os
from crewai import Agent
from langchain_community.llms import HuggingFaceHub

class ReportingAgent:
    def __init__(self, llm):
        self.llm = llm
        
    def _create_tools(self):
        """Create the tools that the agent can use"""
        # In a real implementation, you might have custom tools for report generation
        return []
        
    def get_agent(self):
        """Create and return the Reporting Agent"""
        agent = Agent(
            role='Risk Reporting Specialist',
            goal='Generate comprehensive risk reports with visualizations, mitigation strategies, and actionable insights',
            backstory="""You are a skilled risk communication and reporting expert with experience translating
            complex risk data into clear, actionable reports. Your ability to present information in a 
            compelling and understandable way ensures that stakeholders at all levels can comprehend
            risk status and make informed decisions. You excel at creating visualizations that highlight
            key risk patterns and trends.""",
            verbose=True,
            llm=self.llm,
            tools=self._create_tools()
        )
        return agent
        
    def generate_report(self, project_id, risk_data=None):
        """Generate a detailed risk report for a specific project"""
        # This is a simplified implementation
        
        if not risk_data:
            # In a real implementation, you would retrieve risk data from a database
            risk_data = {
                "project_name": "Sample Project",
                "overall_risk_score": 6.8,
                "risk_trend": "Increasing",
                "risk_categories": {
                    "schedule_risk": 7.2,
                    "budget_risk": 5.8,
                    "resource_risk": 6.5,
                    "technical_risk": 7.4
                },
                "top_risk_factors": [
                    {
                        "name": "Technical Complexity",
                        "score": 7.4,
                        "description": "Integration challenges with legacy systems",
                        "mitigation": "Conduct additional integration testing and allocate expert resources"
                    },
                    {
                        "name": "Resource Availability",
                        "score": 6.9,
                        "description": "Key technical specialists overallocated",
                        "mitigation": "Cross-train team members and consider contracting specialists"
                    }
                ]
            }
        
        # Generate a report based on the risk data
        # In a real implementation, this would create a structured report with visualizations
        return f"""
        # Risk Report: {risk_data.get('project_name', 'Project')}
        
        ## Executive Summary
        
        The project currently has an overall risk score of **{risk_data.get('overall_risk_score', 'N/A')}/10**
        with a **{risk_data.get('risk_trend', 'stable')}** trend. Immediate attention is required for 
        the following high-risk areas:
        
        1. {risk_data.get('top_risk_factors', [{}])[0].get('name', 'No major risks identified')}
        2. {risk_data.get('top_risk_factors', [{}, {}])[1].get('name', 'No additional major risks') if len(risk_data.get('top_risk_factors', [])) > 1 else 'No additional major risks'}
        
        ## Detailed Risk Analysis
        
        [Detailed risk metrics and visualization would be included here]
        
        ## Recommended Mitigation Strategies
        
        {risk_data.get('top_risk_factors', [{}])[0].get('mitigation', 'No mitigation strategies available')}
        
        ## Risk Trend Analysis
        
        [Risk trend visualization would be included here]
        
        """
        
    def suggest_mitigation_strategy(self, risk_factor):
        """Suggest mitigation strategies for a specific risk factor"""
        # This is a simplified implementation
        
        risk_type = risk_factor.get('category', 'unknown').lower() if isinstance(risk_factor, dict) else 'unknown'
        
        if risk_type == 'schedule_risk':
            return """
            # Mitigation Strategy for Schedule Risk
            
            ## Recommended Actions:
            
            1. **Buffer Management**: Add buffer periods to critical path activities
            2. **Resource Optimization**: Allocate additional resources to high-risk activities
            3. **Dependency Review**: Re-evaluate and potentially restructure task dependencies
            4. **Milestone Tracking**: Implement more frequent milestone reviews
            5. **Scope Control**: Consider reducing non-essential scope elements
            
            ## Implementation Timeline:
            
            - **Immediate**: Review critical path and identify potential schedule compression opportunities
            - **Short-term**: Allocate additional resources to at-risk activities
            - **Ongoing**: Weekly schedule risk assessment and adjustment
            
            ## Success Metrics:
            
            - Schedule Performance Index (SPI) improved to >0.95
            - All critical milestones met within 3 business days of baseline
            - No further schedule deterioration in monthly assessments
            """
        elif risk_type == 'budget_risk':
            return """
            # Mitigation Strategy for Budget Risk
            
            ## Recommended Actions:
            
            1. **Cost Control**: Implement enhanced cost tracking and approval processes
            2. **Vendor Management**: Renegotiate terms with key suppliers
            3. **Scope Management**: Review requirements for potential descoping opportunities
            4. **Resource Optimization**: Evaluate resource utilization and adjust allocation
            5. **Contingency Planning**: Review and potentially increase contingency reserves
            
            ## Implementation Timeline:
            
            - **Immediate**: Conduct cost variance analysis and identify saving opportunities
            - **Short-term**: Implement revised approval processes for all expenditures
            - **Ongoing**: Bi-weekly budget reviews with stakeholders
            
            ## Success Metrics:
            
            - Cost Performance Index (CPI) improved to >0.95
            - Monthly expenditure within 5% of revised budget
            - Identified cost savings of at least 10% in non-critical areas
            """
        else:
            return """
            # Mitigation Strategy
            
            ## Recommended Actions:
            
            1. **Risk Assessment**: Conduct detailed analysis of the risk factor
            2. **Stakeholder Engagement**: Engage relevant stakeholders to develop mitigation plan
            3. **Monitoring Plan**: Establish clear metrics for tracking the risk
            4. **Contingency Planning**: Develop contingency plans for worst-case scenarios
            5. **Regular Review**: Schedule periodic reviews of risk status and mitigation effectiveness
            
            ## Implementation Timeline:
            
            - **Immediate**: Assign risk owner and begin detailed assessment
            - **Short-term**: Develop and begin implementing mitigation plan
            - **Ongoing**: Regular monitoring and adjustment of mitigation strategies
            
            ## Success Metrics:
            
            - Risk score reduction of at least 20% within one month
            - No major impacts to project objectives from this risk factor
            - Stakeholder confidence in risk management approach
            """