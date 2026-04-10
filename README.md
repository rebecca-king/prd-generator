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

The tool walks you through a series of prompts, then streams the PRD to your terminal and saves it as `prd-<feature-name>-<date>.md` in your current directory.

### Prompts

| Prompt | Required | Description |
|--------|----------|-------------|
| Feature / product name | Yes | Name of the thing you're building |
| Author name | No | Your name, for the document header |
| Reviewers / stakeholders | No | Who needs to sign off |
| Problem statement | Yes | The pain you're solving and for whom |
| Why now | No | What makes this the right time to build this |
| Target users | Yes | Who experiences this problem |
| User personas | No | 1–3 personas: name, role, context, key frustration |
| User stories (JTBD) | No | "When I... I want to... So I can..." — one per line |
| Goals & success metrics | Yes | How you'll measure success |
| Acceptance criteria | No | Conditions that make the feature shippable |
| Scope notes | No | Known in/out of scope items |
| Assumptions | No | Things being treated as true but not yet verified |
| Risks & dependencies | No | What could block or break delivery |
| Additional context | No | Background, constraints, links |

Multi-line fields (personas, user stories, acceptance criteria, assumptions, risks) accept multiple lines — press Enter on a blank line to move to the next prompt.

Optional sections that are left blank are omitted from the output entirely. No placeholders, no empty headers.

### Output structure

Generated PRDs follow this section order:

1. Document Header *(title, date, status, author, reviewers)*
2. Executive Summary
3. Why Now / Strategic Context *(if provided)*
4. Problem Statement
5. Target Users
6. User Personas *(if provided)*
7. User Stories (JTBD) *(if provided)*
8. Goals & Success Metrics
9. Solution Overview
10. Acceptance Criteria *(if provided)*
11. Scope
12. Assumptions *(if provided)*
13. Risks & Dependencies *(if provided)*
14. Open Questions

## Customizing Your Writing Style

Your voice and style preferences live in `style_guide.md`. Edit that file to adjust:

- **Tone** — add or remove writing principles
- **Structure** — reorder or rename sections
- **Length** — change the word count targets per section
- **Formatting** — adjust header levels, list styles, table formats

The contents of `style_guide.md` are injected as the system prompt on every run, so changes take effect immediately.
