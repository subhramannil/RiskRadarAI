import os
from crewai import Agent
from langchain_community.llms import HuggingFaceHub

class RiskScoringAgent:
    def __init__(self, llm):
        self.llm = llm
        
    def _create_tools(self):
        """Create the tools that the agent can use"""
        # In a real implementation, you might have custom tools for risk scoring
        return []
        
    def get_agent(self):
        """Create and return the Risk Scoring Agent"""
        agent = Agent(
            role='Risk Scoring Expert',
            goal='Calculate accurate risk scores for projects by evaluating multiple risk factors and their interrelationships',
            backstory="""You are a quantitative risk analyst with a background in mathematical modeling and
            statistical analysis. Your expertise lies in converting qualitative risk assessments into
            precise numerical scores that accurately reflect risk levels. Your models account for risk
            factor interdependencies, historical patterns, and predictive indicators to provide a holistic
            risk assessment.""",
            verbose=True,
            llm=self.llm,
            tools=self._create_tools()
        )
        return agent
        
    def score_project_risk(self, project_id, project_data=None):
        """Calculate risk score for a specific project"""
        # This is a simplified implementation that would be replaced with actual risk scoring algorithms
        
        if not project_data:
            # In a real implementation, you would retrieve project data from a database
            # and perform detailed analysis based on various risk factors
            project_data = {
                "schedule_risk_factors": [
                    {"name": "Timeline slippage", "impact": 7, "likelihood": 6},
                    {"name": "Resource availability", "impact": 8, "likelihood": 5}
                ],
                "budget_risk_factors": [
                    {"name": "Cost overruns", "impact": 6, "likelihood": 7},
                    {"name": "Vendor price increases", "impact": 5, "likelihood": 6}
                ],
                "technical_risk_factors": [
                    {"name": "Integration complexity", "impact": 8, "likelihood": 7},
                    {"name": "Technical debt", "impact": 6, "likelihood": 5}
                ],
                "market_risk_factors": [
                    {"name": "Competitive landscape", "impact": 7, "likelihood": 5},
                    {"name": "Regulatory changes", "impact": 8, "likelihood": 4}
                ]
            }
        
        # Calculate schedule risk
        schedule_risk = sum(f["impact"] * f["likelihood"] for f in project_data.get("schedule_risk_factors", [])) / 100 * 10
        if not project_data.get("schedule_risk_factors"):
            schedule_risk = 5.0  # Default value
            
        # Calculate budget risk
        budget_risk = sum(f["impact"] * f["likelihood"] for f in project_data.get("budget_risk_factors", [])) / 100 * 10
        if not project_data.get("budget_risk_factors"):
            budget_risk = 5.0  # Default value
            
        # Calculate technical risk
        technical_risk = sum(f["impact"] * f["likelihood"] for f in project_data.get("technical_risk_factors", [])) / 100 * 10
        if not project_data.get("technical_risk_factors"):
            technical_risk = 5.0  # Default value
            
        # Calculate market risk
        market_risk = sum(f["impact"] * f["likelihood"] for f in project_data.get("market_risk_factors", [])) / 100 * 10
        if not project_data.get("market_risk_factors"):
            market_risk = 5.0  # Default value
            
        # Calculate overall risk score (weighted average)
        weights = {"schedule": 0.25, "budget": 0.25, "technical": 0.3, "market": 0.2}
        overall_risk = (
            schedule_risk * weights["schedule"] +
            budget_risk * weights["budget"] +
            technical_risk * weights["technical"] +
            market_risk * weights["market"]
        )
        
        # Return formatted risk scores
        return {
            "overall_risk": round(overall_risk, 1),
            "schedule_risk": round(schedule_risk, 1),
            "budget_risk": round(budget_risk, 1),
            "technical_risk": round(technical_risk, 1),
            "market_risk": round(market_risk, 1),
        }