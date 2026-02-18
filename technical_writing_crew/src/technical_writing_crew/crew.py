import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# 1. Environment Setup
# Load environment variables from .env file
load_dotenv()
os.environ["OTEL_SDK_DISABLED"] = "true"


@CrewBase
class TechnicalWritingCrew():
    """TechnicalWritingCrew crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def _get_llm(self) -> LLM:
        """Initialize the native CrewAI LLM with the latest supported Groq model."""
        return LLM(
            model="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY"),
            # model="groq/llama-3.3-70b-versatile",
            # api_key=os.getenv("GROQ_API_KEY"),
            temperature=0
        )

    # Agents: All Agents are defined on this section. You can add as many Agents as you want, and they will be available to the Crew.
    @agent
    def technical_researcher(self) -> Agent:
        web_search_tool = SerperDevTool()

        return Agent(
            config=self.agents_config['technical_researcher'],
            tools=[web_search_tool],
            allow_delegation=False,
            llm=self._get_llm(),
            verbose=True
        )

    @agent
    def article_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['article_strategist'],
            llm=self._get_llm(),
            verbose=True,
            allow_delegation=False
        )
    
    @agent
    def technical_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_writer'],
            llm=self._get_llm(),
            verbose=True,
            allow_delegation=False
        )
    
    @agent
    def technical_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_editor'],
            llm=self._get_llm(),
            verbose=True,
            allow_delegation=False
        )

    # Tasks: All Tasks are defined on this section. You can add as many Tasks as you want, and they will be available to the Crew.
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task']
        )
    
    @task
    def outline_task(self) -> Task:
        return Task(
            config=self.tasks_config['outline_task']
        )
    
    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task']
        )
    
    @task
    def editing_task(self) -> Task:
        return Task(
            config=self.tasks_config['editing_task']
        )

    # We will need to define an output file for the formatting task, as it will be the last task of the process and we want to save the final article in a markdown file.
    @task
    def formatting_task(self) -> Task:
        return Task(
            config=self.tasks_config['formatting_task'],
            output_file="technical_article.md"
        )

    # Crew: The Crew is defined on this section. 
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process= Process.sequential,
            verbose=True
        )