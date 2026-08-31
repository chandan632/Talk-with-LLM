# Talk with LLM

A small Python project for interacting with Groq-hosted large language models from the terminal.

## Features

- Sends prompts to Groq models through the official Groq Python SDK
- Reads the API key from a local `.env` file
- Includes a simple example for chat completion
- Lists available models from the Groq API

## Project structure

- `hello-llm.py` — sample chat request to a model
- `models.py` — lists available Groq models
- `src/talk_with_llm/` — package entry point

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   If you are using the project environment managed by `uv`, you can also run:

   ```bash
   uv sync
   ```

3. Create a `.env` file in the project root with your Groq API key:

   ```env
   GROQ_API_KEY=your_api_key_here
   ```

## Usage

Run the chat example:

```bash
python hello-llm.py
```

List the models available on Groq:

```bash
python models.py
```

## Example output

```text
Who is the Chief Minister of Delhi, India?
Model used: openai/gpt-oss-120b
Usage: {...}
Finish reason: stop
```

## Notes

- The project expects a valid `GROQ_API_KEY` environment variable.
- The example uses the `openai/gpt-oss-120b` model.
- This is intended as a minimal starter project for experimenting with LLM APIs in Python.
