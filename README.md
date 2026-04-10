# PRD Generator

A CLI tool that generates Product Requirements Documents in your voice and writing style, powered by Claude.

## Prerequisites

- Python 3.8+
- An Anthropic API key

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your API key:

```bash
export ANTHROPIC_API_KEY=your-key-here
```

## Usage

```bash
python generate_prd.py
```

The tool will walk you through a series of prompts:

| Prompt | Required | Description |
|--------|----------|-------------|
| Feature / product name | Yes | Name of the thing you're building |
| Problem statement | Yes | The pain you're solving and for whom |
| Target users | Yes | Who experiences this problem |
| Goals & success metrics | Yes | How you'll measure success |
| Scope notes | No | Known in/out of scope items |
| Additional context | No | Background, constraints, links |

After answering, the PRD streams to your terminal in real time and is saved as `prd-<feature-name>-<date>.md` in your current directory.

## Customizing Your Writing Style

Your voice and style preferences live in `style_guide.md`. Edit that file to adjust:

- **Tone** — add or remove writing principles
- **Structure** — reorder or rename sections
- **Length** — change the word count targets
- **Formatting** — adjust header levels, list styles, table formats

The contents of `style_guide.md` are injected as the system prompt for every PRD generation, so changes take effect immediately on the next run.
