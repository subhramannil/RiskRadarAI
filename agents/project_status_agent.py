import os
from crewai import Agent
from langchain_community.llms import HuggingFaceHub

class ProjectStatusAgent:
    def __init__(self, llm):
        self.llm = llm
        
    def _create_tools(self):
        """Create the tools that the agent can use"""
        # In a real implementation, you might have custom tools for project analysis
        return []
        
    def get_agent(self):
        """Create and return the Project Status Agent"""
        agent = Agent(
            role='Project Status Analyst',
            goal='Analyze project parameters including resource allocation, schedule compliance, and internal factors to identify project-specific risks',
            backstory="""You are a seasoned project management professional with expertise in identifying
            project-specific risks. Your attention to detail and analytical skills allow you to
            detect subtle warning signs in project metrics, resource allocation, and timelines
            that others might miss. Project teams rely on your insights to address issues before they become critical.""",
            verbose=True,
            llm=self.llm,
            tools=self._create_tools()
        )
        return agent
        
    def analyze_project_status(self, project_id):
        """Analyze the current status of a specific project"""
        # This is a simplified implementation that would be replaced with actual project analysis
        
        # In a real implementation, you would retrieve project data from a database
        # and perform detailed analysis
        return {
            "status": "In Progress",
            "schedule_status": "2 weeks behind",
            "budget_status": "5% over budget",
            "resource_utilization": "85%",
            "major_issues": [
                "Key technical resource reassigned",
                "Requirements changing frequently",
                "Integration testing taking longer than expected"
            ],
            "risk_score": 6.8,
            "risk_change": +0.4
        }
        
    def check_specific_risk_area(self, project_id, risk_area):
        """Check a specific risk area for a project"""
        # This is a simplified implementation
        
        if risk_area.lower() == "schedule":
            return {
                "risk_score": 7.2,
                "trend": "Increasing",
                "key_factors": [
                    "Missed milestone: System Design Review",
                    "Testing phase extended by 2 weeks",
                    "Resource allocation delays"
                ],
                "recommendations": [
                    "Re-baseline project schedule",
                    "Add resources to critical path activities",
                    "Implement daily status checks for high-risk tasks"
                ]
            }
        elif risk_area.lower() == "budget":
            return {
                "risk_score": 5.8,
                "trend": "Stable",
                "key_factors": [
                    "Hardware costs higher than estimated",
                    "Additional contractor hours required",
                    "Foreign exchange rate impact on international vendors"
                ],
                "recommendations": [
                    "Review remaining budget allocations",
                    "Identify potential cost-saving opportunities",
                    "Implement stricter change control process"
                ]
            }
        else:
            return {
                "risk_score": 6.0,
                "trend": "Variable",
                "key_factors": [
                    "Multiple areas of concern identified",
                    "Insufficient data for detailed analysis",
                    "Recommend comprehensive risk assessment"
                ],
                "recommendations": [
                    "Conduct formal risk assessment workshop",
                    "Review project documentation and metrics",
                    "Interview key stakeholders"
                ]
            }