import os
from crewai import Agent, LLM
from crewai_tools import SerperDevTool

browse_tool = SerperDevTool()

print("########################")   
print(browse_tool.run(search_query="AI Agents for travel planning"))
print("########################\n")

# 1. Environment Setup
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OTEL_SDK_DISABLED"] = "true"

# Initialize the native CrewAI LLM with the latest supported Groq model
free_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

destination_research_agent = Agent(
    role="An explorer who specializes in researching travel destinations, uncovering hidden gems, local attractions, and cultural experiences.",
    goal="Identify and compile a list of must-visit places, activities, and experiences for a given travel destination (e.g. 'historical', 'foodie spots').",
    backstory="A seasoned traveler with a passion for discovering unique locations and experiences. You have extensive knowledge of various destinations around the world and are skilled at finding off-the-beaten-path attractions that provide authentic cultural experiences.",
    tools=[browse_tool],
    llm=free_llm,
    verbose=True
)

itinerary_planner_agent = Agent(
    role="A meticulous planner who designs detailed travel itineraries based on researched destinations and user preferences.",
    goal="Create a day-by-day travel itinerary that includes activities, dining options, and logistical details for a specified destination.",
    backstory="An organized travel enthusiast with experience in crafting personalized itineraries. You excel at balancing sightseeing, relaxation, and local experiences to ensure travelers have a memorable and well-rounded trip.",
    llm=free_llm,
    verbose=True
)