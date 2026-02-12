# my-first-crew

A demo project that uses the CrewAI library to power multi-agent AI workflows. This project includes two main applications: YouTube video idea generation and travel planning.

**Status**: Prototype / example

## Overview

This project demonstrates CrewAI's capabilities with two distinct multi-agent workflows:

1. **YouTube Crew** ([youtube_crew.py](youtube_crew.py)) — Generate and filter YouTube video ideas
2. **Travel Planning Crew** ([simple_travel_planning_crew.py](simple_travel_planning_crew.py)) — Research destinations and create travel itineraries

## Requirements

- Python 3.10+
- CrewAI library and dependencies
- Network access for model APIs and embeddings

## Environment Variables

- `GROQ_API_KEY` — Required for using Groq LLM models (e.g., `groq/llama-3.3-70b-versatile`)
- `OPENAI_API_KEY` — Set to "NA" by default (not used)
- `OTEL_SDK_DISABLED` — Set to "true" to disable OpenTelemetry
- `SERPER_API_KEY` — Required for using SerperDevTool

## Scripts

### 1. YouTube Crew ([youtube_crew.py](youtube_crew.py))

**Purpose**: Brainstorm and filter YouTube video ideas for a given topic.

**Agents**:
- `idea_generator_agent` — Generates diverse YouTube video concepts across formats (tutorials, vlogs, listicles, reviews, interviews, challenges, etc.)
- `idea_filter_agent` — Evaluates and prioritizes ideas based on YouTube viability (search potential, engagement, feasibility, uniqueness)

**Tasks**:
- `idea_generation_task` — Produces a broad list of raw video concepts
- `idea_filtering_task` — Refines the list to top 3-5 actionable ideas with justifications

**Key Configuration**:
- LLM: `groq/llama-3.3-70b-versatile` with temperature 0
- Embedder: HuggingFace `all-MiniLM-L6-v2`
- Process: Sequential
- Default topic: `"Como hacer gorditas de chicharron"`

**Output**: Refined list of the top YouTube video ideas with explanations of why each was selected.

### 2. Travel Planning Crew ([simple_travel_planning_crew.py](simple_travel_planning_crew.py))

**Purpose**: Research travel destinations and create detailed itineraries.

**Agents**:
- `destination_research_agent` — Specializes in researching destinations, uncovering hidden gems, local attractions, and cultural experiences
- `itinerary_planner_agent` — Designs detailed day-by-day travel itineraries with activities, dining, and logistics

**Tools**:
- `SerperDevTool` (browse_tool) — Web search capability for destination research

**Key Configuration**:
- LLM: `groq/llama-3.3-70b-versatile` with temperature 0
- Process: Not yet fully configured with tasks and crew
- Verbose mode: Enabled for both agents

## Usage

### Setup

Export your Groq API key:

```bash
export GROQ_API_KEY=your_groq_api_key_here
```

Export your Serper API key:

```bash
export SERPER_API_KEY=your_serper_api_key_here
```


### Run YouTube Crew

```bash
python youtube_crew.py
```

Customize the topic by editing the kickoff inputs at the bottom of the script:

```python
result = idea_generation_crew.kickoff(inputs={
    "topic": "Your desired topic here"
})
```

### Run Travel Planning Crew

```bash
python simple_travel_planning_crew.py
```

Note: This script currently initializes agents and demonstrates the SerperDevTool API response. Full Crew implementation with tasks is in progress.

## Project Structure

- `youtube_crew.py` — Complete YouTube idea generation workflow
- `simple_travel_planning_crew.py` — Travel planning agents and tools
- `requirements.txt` — Project dependencies
- `README.md` — This file

## Next Steps / Extending

- Complete travel planning Crew with tasks and process configuration
- Add CLI arguments to accept topics/destinations from command line
- Implement `.env` file support for secure credential management
- Add error handling and validation for agent outputs
- Create tests for agent workflows
- Add dry-run mode with stub LLM for testing