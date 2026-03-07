# my-first-crew

A demo project that uses the CrewAI library to power multi-agent AI workflows. This project includes multiple applications showcasing different crew configurations:

**Status**: Active development

## Overview

This project demonstrates CrewAI's capabilities with multiple multi-agent workflows:

1. **Technical Writing Crew** (`technical_writing_crew/`) — Research topics, create outlines, write and edit technical articles
2. **YouTube Crew** ([youtube_crew.py](my_first_crews/youtube_crew.py)) — Generate and filter YouTube video ideas
3. **Travel Planning Crew** ([simple_travel_planning_crew.py](my_first_crews/simple_travel_planning_crew.py)) — Research destinations and create travel itineraries

## Requirements

- Python 3.10+
- CrewAI library and dependencies
- LiteLLM (for provider fallback to Groq and other models)
- Network access for model APIs

## Quick Start

1. Activate the project's virtual environment (example):

```bash
source .venv/bin/activate
```

2. Install dependencies (including `litellm`):

```bash
pip install -r requirements.txt
```

3. Run a crew (target the active venv to avoid fallback warnings):

```bash
crewai run --active
```
	- Note: the Python package name is `litellm` (provides LiteLLM runtime)

## Using UV (optional)

This project uses `uv` for dependency management in some workflows. You can
use `uv` to add packages to the project environment from the `technical_writing_crew`
directory. Example:

```bash
# install uv if you don't have it
pip install uv

# add a dependency to the project environment
uv add <package-name>
```

Note: `uv add` modifies the project dependency metadata; you should still
activate your virtual environment before running crews to ensure packages are
available to the running Python process.

## Environment Variables

- `GROQ_API_KEY` — **Required** for using Groq LLM models (e.g., `groq/llama-3.3-70b-versatile`)
- `SERPER_API_KEY` — Required for using SerperDevTool (web search capability)
- `OPENAI_API_KEY` — Optional; if set, may cause network/connectivity issues if your network blocks api.openai.com
- `OTEL_SDK_DISABLED` — Set to "true" to disable OpenTelemetry

## Network Requirements

**Important**: Ensure your network allows outbound TLS connections to:
- `api.groq.com` (Groq API endpoint)
- `google.serper.dev` (SerperDevTool endpoint)

If your network blocks these endpoints (e.g., via Cisco Umbrella/OpenDNS), you may encounter connection errors. Contact your network administrator to whitelist these domains.

## Scripts

### 1. Technical Writing Crew (`technical_writing_crew/`)

**Purpose**: Research technical topics, create detailed outlines, write comprehensive articles, and edit for clarity and accuracy.

**Agents**:
- `technical_researcher` — Gathers comprehensive research from online sources using web search
- `article_strategist` — Creates logical outlines and structures for the article
- `technical_writer` — Writes clear, engaging technical content with code examples
- `technical_editor` — Reviews for technical accuracy, clarity, and quality

**Tasks** (Sequential):
- `research_task` — Research the technical topic and compile findings
- `outline_task` — Create a detailed article outline
- `writing_task` — Write the article draft
- `editing_task` — Review and refine the article
- `formatting_task` — Final formatting and output to Markdown file

**Key Configuration**:
- LLM: `groq/llama-3.3-70b-versatile` with temperature 0
- Process: Sequential
- Default topic: `"Introduction to GraphQL"`
- Output: `technical_article.md`

**Run**:
```bash
cd technical_writing_crew
crewai run
```

### 2. YouTube Crew ([youtube_crew.py](my_first_crews/youtube_crew.py))

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

**Run YouTube Crew**:

```bash
python my_first_crews/youtube_crew.py
```

### 3. Travel Planning Crew ([simple_travel_planning_crew.py](my_first_crews/simple_travel_planning_crew.py))

**Purpose**: Research travel destinations and create detailed itineraries.

**Agents**:
- `destination_research_agent` — Specializes in researching destinations, uncovering hidden gems, local attractions, and cultural experiences
- `itinerary_planner_agent` — Designs detailed day-by-day travel itineraries with activities, dining, and logistics

**Tools**:
- `SerperDevTool` (browse_tool) — Web search capability for destination research

**Key Configuration**:
- LLM: `groq/llama-3.3-70b-versatile` with temperature 0
- Tools: SerperDevTool (web search)
- Process: Sequential
- Default destination: `"CDMX"`

**Run Travel Planning Crew**:

```bash
python my_first_crews/simple_travel_planning_crew.py
```

Note: Requires valid `GROQ_API_KEY` and `SERPER_API_KEY` environment variables.

## Project Structure

```
my-first-crew/
├── README.md                           # This file
├── requirements.txt                    # Root dependencies
├── technical_writing_crew/             # Technical Writing crew (CrewAI scaffold)
│   ├── src/technical_writing_crew/
│   │   ├── crew.py                     # Crew and agent definitions
│   │   ├── main.py                     # Entry point
│   │   └── config/
│   │       ├── agents.yaml             # Agent configurations
│   │       └── tasks.yaml              # Task configurations
│   ├── pyproject.toml
│   └── .env                            # API keys (not in git)
├── my_first_crews/
│   ├── youtube_crew.py                 # YouTube idea generation
│   ├── simple_travel_planning_crew.py   # Travel planning
│   └── .venv/                          # Virtual environment (if created locally)
```

## Troubleshooting

### "ImportError: Fallback to LiteLLM is not available"
- **Cause**: LiteLLM package not installed
- **Solution**: Run `pip install litellm` or reinstall requirements
 - **Cause**: LiteLLM runtime (`litellm`) is not available in the Python
	 environment that is running the Crew. This commonly happens when `pip`
	 installs packages into a different Python/venv than the one used to run
	 the crew, or when the virtual environment is not activated.
 - **Solution**:
	 - Activate your project's virtual environment (example):

		 ```bash
		 source .venv/bin/activate
		 ```

	 - Install `litellm` into the active environment:

		 ```bash
		 pip install litellm
		 # or install all requirements
		 pip install -r requirements.txt
		 ```

	 - Verify the installation and that you're using the correct Python:

		 ```bash
		 python -c "import litellm, sys; print('litellm', getattr(litellm,'__version__','unknown'))"
		 python -c "from crewai import LLM; print('crewai.LLM import OK')"
		 ```

	 - When running `crewai run`, if you see a warning about the virtual
		 environment path not matching (for example: `VIRTUAL_ENV=... does not
		 match the project environment path .venv`), use the `--active` flag to
		 target the currently active environment:

		 ```bash
		 # from the technical_writing_crew directory
		 crewai run --active
		 ```

	 - If the error persists, confirm there are no multiple Python installs
		 shadowing each other and ensure `pip` installs to the same `python`
		 executable used to run the crew (use `which python` / `which pip`).

### "GROQ_API_KEY not set" or "SERPER_API_KEY not set"
- **Cause**: Environment variables not exported
- **Solution**: Set them before running (see Setup section above)

## Next Steps / Extending

- Add CLI arguments to customize topics/destinations at runtime
- Implement comprehensive error handling and retries
- Add test suite for workflows
- Create web UI for crew input/output
- Support additional LLM providers (Claude, Gemini, etc.)
- Add prompt versioning and A/B testing