import os
import litellm
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# 1. Environment Setup
# Load environment variables from .env file
#load_dotenv()
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OTEL_SDK_DISABLED"] = "true"
# stop the library from attempting to load these standard logging objects
os.environ["LITELLM_MODE"] = "production"
os.environ["LITELLM_LOG"] = "INFO"
litellm.set_verbose = False
litellm.suppress_debug_info = True

@CrewBase
class TechnicalWritingCrew():
    """TechnicalWritingCrew crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def _get_llm(self, model_name="groq/llama-3.3-70b-versatile") -> LLM:
        return LLM(
            model=model_name,
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0,
            # Keep this around 2000-3000 to avoid hitting limits 
            # when the agent receives large search results
            max_tokens=2000
        )    

    # Agents: All Agents are defined on this section. You can add as many Agents as you want, and they will be available to the Crew.
    @agent
    def technical_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_researcher'],
            tools=[SerperDevTool(n_results=3)],
            # Switch to 8b to stay under rate limits during heavy searching
            llm=self._get_llm("groq/llama-3.1-8b-instant"), 
            verbose=True,
            # Slower cadence to avoid Groq's 429 error
            max_rpm=1, 
            # Limits the agent from getting stuck in long loops
            max_iter=3
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