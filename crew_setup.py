import os
from crewai import Crew, Agent, Task
from langchain_community.llms import HuggingFaceHub
from agents.market_analysis_agent import MarketAnalysisAgent
from agents.risk_scoring_agent import RiskScoringAgent
from agents.project_status_agent import ProjectStatusAgent
from agents.reporting_agent import ReportingAgent
# The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# Do not change this unless explicitly requested by the user

llm = HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature": 0.5, "max_length": 512})
class RiskManagementCrew:
    def __init__(self):
        self.market_analysis_agent = MarketAnalysisAgent(llm).get_agent()
        self.risk_scoring_agent = RiskScoringAgent(llm).get_agent()
        self.project_status_agent = ProjectStatusAgent(llm).get_agent()
        self.reporting_agent = ReportingAgent(llm).get_agent()
        
    def create_crew(self):
        """Create and return a crew with all the agents"""
        crew = Crew(
            agents=[
                self.market_analysis_agent,
                self.risk_scoring_agent,
                self.project_status_agent,
                self.reporting_agent
            ],
            tasks=self._get_tasks(),
            verbose=True
        )
        return crew
    
    def _get_tasks(self):
        """Define the tasks for the crew"""
        market_analysis_task = Task(
            description="Analyze current market conditions, financial trends, and economic indicators to identify external risk factors that could impact ongoing projects.",
            expected_output="A comprehensive report of market-related risk factors with their potential impact on projects, along with confidence levels.",
            agent=self.market_analysis_agent
        )
        
        project_status_task = Task(
            description="Analyze project parameters like resource availability, payment schedules, timeline progress, and internal factors to identify project-specific risks.",
            expected_output="A detailed analysis of each project's status, highlighting internal risk factors with severity ratings.",
            agent=self.project_status_agent
        )
        
        risk_scoring_task = Task(
            description="Evaluate both market and project-specific risks to calculate comprehensive risk scores for each project and identify the most critical risk factors.",
            expected_output="Risk scores for each project along with ranked risk factors, including likelihood and impact assessments.",
            agent=self.risk_scoring_agent,
            context=[market_analysis_task, project_status_task]
        )
        
        reporting_task = Task(
            description="Generate comprehensive risk reports with visualizations, mitigation strategies, and alerts for critical risks that exceed thresholds.",
            expected_output="Complete risk reports with actionable mitigation strategies and alerts for stakeholders.",
            agent=self.reporting_agent,
            context=[risk_scoring_task]
        )
        
        return [market_analysis_task, project_status_task, risk_scoring_task, reporting_task]
    
    def run_risk_assessment(self, project_id=None):
        """Run the risk assessment process, optionally for a specific project"""
        crew = self.create_crew()
        result = crew.kickoff()
        return result
    
    def get_risk_report(self, project_id):
        """Get a risk report for a specific project"""
        # This is a simplified implementation - in a real system, we'd retrieve stored reports
        crew = self.create_crew()
        result = crew.kickoff(inputs={"project_id": project_id})
        return result
    
    def get_mitigation_strategies(self, risk_factor):
        """Get mitigation strategies for a specific risk factor"""
        # For simplicity, we'll use the reporting agent directly
        result = self.reporting_agent.run(f"Provide detailed mitigation strategies for the following risk factor: {risk_factor}")
        return result