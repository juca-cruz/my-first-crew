# my-first-crew

A small demo project that uses the CrewAI library to generate and filter YouTube video ideas. The core script, [youtube_crew.py](youtube_crew.py), defines a pair of agents (idea generator and idea evaluator) and runs them as a Crew to produce and refine video concepts for a provided topic.

**Status**: Prototype / example

**Key features**
- Brainstorm YouTube video ideas across formats (tutorials, vlogs, listicles, reviews, interviews, etc.)
- Filter and prioritize the most promising ideas with simple evaluation criteria
- Uses a local LLM wrapper and an embedder for in-memory planning

**Requirements**
- Python 3.10+
- The project imports `crewai` and uses a Groq LLM; install the runtime packages required by your environment (for example, a `crewai` package if available).
- Network access for model APIs and Hugging Face embeddings (if used).

Environment variables
- `GROQ_API_KEY` — required by the `LLM` initialization in `youtube_crew.py` when using Groq models.
- `OPENAI_API_KEY` — shown in the example script but set to "NA" (not used) by default.

Usage

1. Export your model API key (example):

```bash
export GROQ_API_KEY=your_groq_api_key_here
```

2. Run the example script:

```bash
python youtube_crew.py
```

3. By default the script runs with the topic `"Como hacer gorditas de chicharron"`. To change it, edit the kickoff inputs at the bottom of [youtube_crew.py](youtube_crew.py) or modify the script to accept a CLI argument.

What to expect
- The script initializes two agents and runs a sequential Crew process.
- Output will be printed to the console and include a final refined list of top video ideas.

Extending this project
- Add CLI flags to pass `topic` from the command line.
- Replace the placeholder API key handling with secure config or `.env` support.
- Add tests for agent outputs or a dry-run mode that uses a deterministic stub LLM.
- Add a `requirements.txt` or `pyproject.toml` to pin dependencies.