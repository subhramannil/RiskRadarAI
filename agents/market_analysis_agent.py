import os
from crewai import Agent
from langchain_community.llms import HuggingFaceHub

class MarketAnalysisAgent:
    def __init__(self, llm):
        self.llm = llm
        
    def _create_tools(self):
        """Create the tools that the agent can use"""
        # In a real implementation, you might have custom tools for market analysis
        return []
        
    def get_agent(self):
        """Create and return the Market Analysis Agent"""
        agent = Agent(
            role='Market Analysis Specialist',
            goal='Continuously analyze market conditions and economic indicators to identify external risk factors that may impact projects',
            backstory="""You are an expert in market analysis and economic forecasting with decades of experience.
            Your deep understanding of market trends, financial indicators, and global economic patterns
            allows you to spot potential risks before they materialize. Your analysis is highly valued
            by project managers and executives.""",
            verbose=True,
            llm=self.llm,
            tools=self._create_tools()
        )
        return agent
    
    def analyze_market_risks(self, project_domain=None):
        """Analyze market risks potentially affecting a specific project domain"""
        # This is a simplified implementation that would be replaced with actual market analysis
        
        # Sample market risk analysis for different domains
        if project_domain and project_domain.lower() == "healthcare":
            return {
                "industry_volatility": "Medium",
                "regulatory_changes": "High",
                "competitive_landscape": "Moderate",
                "technology_disruption": "Medium",
                "market_growth": "Positive",
                "top_risks": [
                    {
                        "name": "Regulatory Approval Delays",
                        "likelihood": 7,
                        "impact": 8,
                        "description": "Increasing scrutiny from regulatory bodies may delay product approvals"
                    },
                    {
                        "name": "Technology Obsolescence",
                        "likelihood": 6,
                        "impact": 7,
                        "description": "Rapid technological advances may render current solutions outdated"
                    }
                ]
            }
        else:
            # Generic market risks
            return {
                "industry_volatility": "Variable",
                "regulatory_changes": "Moderate",
                "competitive_landscape": "Dynamic",
                "technology_disruption": "High",
                "market_growth": "Uncertain",
                "top_risks": [
                    {
                        "name": "Supply Chain Disruption",
                        "likelihood": 7,
                        "impact": 8,
                        "description": "Global supply chain instability poses significant risks to projects"
                    },
                    {
                        "name": "Market Demand Shifts",
                        "likelihood": 6,
                        "impact": 7,
                        "description": "Changing consumer preferences may impact product/service demand"
                    }
                ]
            }