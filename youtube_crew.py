import os
from crewai import Agent, Task, Crew, Process, LLM

# 1. Environment Setup
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OTEL_SDK_DISABLED"] = "true"

# Initialize the native CrewAI LLM with the latest supported Groq model
free_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# 3. Agents
idea_generator_agent = Agent(
    role="A Youtube video ideas creative engine, responsible for brainstorming a wide variety of YouTube video concepts based on a given topic or channel niche",
    goal="Your goal is to produce a diverse and extensive list of potential video angles, formats (e.g., tutorials, vlogs, listicles, reviews, interviews), and concepts suitable for the YouTube platform, without initial judgment",
    backstory="""
        You are a free-thinking creative with an endless well of ideas, specifically tuned into the dynamics of YouTube. You thrive on exploring different perspectives and making connections between seemingly unrelated concepts, always thinking about visual potential and audience engagement on the platform. With a background in brainstorming techniques and an understanding of what makes a YouTube video compelling, you can quickly generate a high volume of video ideas, pushing the boundaries of conventional thinking within a niche. You are not concerned with practicality in the initial stage, focusing purely on generating possibilities that could work on YouTube
    """,    
    allow_delegation=False,
    llm=free_llm,
    verbose=True
)

idea_filter_agent = Agent(
    role="The analytical evaluator who sifts through the generated YouTube video ideas, assessing their relevance, feasibility, and potential impact specifically for a YouTube audience",
    goal="Select the most promising and actionable video ideas from the list you receive, based on predefined criteria relevant to YouTube (e.g., search potential, trending topics, audience appeal, visual feasibility, uniqueness, practicality for video production)",
    backstory="""
        You are a pragmatic strategist with a sharp eye for what works on YouTube. You have experience in content strategy and audience understanding, particularly within the online video space. You can quickly analyze a list of video ideas, identify patterns, and evaluate each idea against the project's goals and constraints for YouTube production. You are skilled at prioritizing and selecting the ideas that have the highest potential for success and engagement on the platform, ensuring the output is not just creative but also strategically viable for a YouTube channel.
    """,
    allow_delegation=False,
    llm=free_llm,
    verbose=True
)

# 4. Tasks (Simplified for brevity, keep your full descriptions if preferred)
idea_generation_task = Task(
    description="Brainstorm and produce a list of diverse YouTube video ideas related to {topic}. Think broadly about different YouTube-specific formats (e.g., tutorials, how-tos, reviews, unboxings, vlogs, challenges, listicles, interviews, deep dives) and angles that would appeal to viewers. The focus is on quantity and variety at this stage.",
    expected_output="A numbered or bulleted list of raw YouTube video concepts. Each idea should be a brief, engaging title or description of the video concept, indicating the potential format if applicable.",
    agent=idea_generator_agent    
)

idea_filtering_task = Task(
    description="Review the list of video ideas generated from the preceding task. You will evaluate each idea based on criteria relevant to YouTube success, such as potential search volume/discoverability, audience engagement potential (comments, likes, shares), originality within the niche, visual feasibility, and practicality for video production (required equipment, time commitment). You will then select the most promising ideas and provide a refined list. You should also provide a brief justification for why the selected ideas were chosen, specifically considering their YouTube viability",
    expected_output="""
        A refined list of the top 3-5 YouTube video ideas. For each selected idea, include the idea title/description and a brief explanation of why it was selected, emphasizing its potential effectiveness on YouTube (e.g., "High search potential as a 'how-to', strong visual demonstration opportunity," "Engaging personal format for audience connection," "Addresses a trending topic within the niche").""",
    agent=idea_filter_agent
)

# 5. Crew
idea_generation_crew = Crew(
    agents=[idea_generator_agent, idea_filter_agent],
    tasks=[idea_generation_task, idea_filtering_task],
    process=Process.sequential,
    verbose=True,
    # Use the same LLM for internal planning to avoid OpenAI 401 errors
    manager_llm=free_llm,
    planning_llm=free_llm,
    embedder={
        "provider": "huggingface",
        "config": {
            "model": "all-MiniLM-L6-v2"
        }
    }
)

# 6. Kickoff
result = idea_generation_crew.kickoff(inputs={
    "topic": "Como hacer gorditas de chicharron"
})

print("\n\n########################")
print("## FINAL RESULT ##")
print("########################\n")
print(result)