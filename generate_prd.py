#!/usr/bin/env python3
"""
PRD Generator — Uses Claude to write a PRD in your voice and style.
Run: python generate_prd.py
"""

import re
import sys
from datetime import date
from pathlib import Path

import anthropic


STYLE_GUIDE_PATH = Path(__file__).parent / "style_guide.md"
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096


def load_style_guide() -> str:
    if not STYLE_GUIDE_PATH.exists():
        print(f"Error: style_guide.md not found at {STYLE_GUIDE_PATH}")
        sys.exit(1)
    return STYLE_GUIDE_PATH.read_text(encoding="utf-8")


def prompt(label: str, required: bool = True) -> str:
    """Single-line input. Re-prompts if required and empty."""
    suffix = " (optional, press Enter to skip): " if not required else ": "
    while True:
        value = input(f"\n{label}{suffix}").strip()
        if value or not required:
            return value
        print("  This field is required. Please enter a value.")


def multiline_prompt(label: str, required: bool = False) -> str:
    """Multi-line input. User enters a blank line to finish."""
    suffix = " (optional)" if not required else ""
    print(f"\n{label}{suffix}:")
    print("  (Press Enter on a blank line when done)")
    lines = []
    while True:
        line = input()
        if line == "":
            if lines or not required:
                break
            print("  This field is required. Please enter a value.")
            continue
        lines.append(line)
    return "\n".join(lines)


def collect_inputs() -> dict:
    print("\n" + "=" * 60)
    print("  PRD Generator")
    print("=" * 60)
    print("Answer the prompts below. Required fields are marked.")
    print("Press Ctrl+C at any time to cancel.\n")

    return {
        "feature_name": prompt("Feature / product name [required]"),
        "author":        prompt("Author name", required=False),
        "reviewers":     prompt("Reviewers / stakeholders", required=False),
        "problem":       prompt("Problem statement — what pain are we solving? [required]"),
        "why_now":       prompt("Why now — what makes this the right time to build this?", required=False),
        "users":         prompt("Target users — who experiences this problem? [required]"),
        "personas":      multiline_prompt("User personas — name, role, context, key frustration (1–3 personas)"),
        "jtbd":          multiline_prompt("User stories (JTBD) — 'When I... I want to... So I can...' (one per line)"),
        "goals":         prompt("Goals & success metrics — how do we know it worked? [required]"),
        "acceptance":    multiline_prompt("Acceptance criteria — when is this feature shippable? (one condition per line)"),
        "scope":         prompt("Scope notes — any known in/out of scope items", required=False),
        "assumptions":   multiline_prompt("Assumptions — things you're treating as true but haven't verified"),
        "risks":         multiline_prompt("Risks & dependencies — what could block or break this?"),
        "context":       prompt("Additional context — background, constraints, links", required=False),
    }


def build_user_message(inputs: dict) -> str:
    today = date.today().isoformat()
    lines = [
        "Write a PRD for the following feature brief.\n",
        f"**Feature name:** {inputs['feature_name']}",
        f"**Date:** {today}",
    ]
    if inputs["author"]:
        lines.append(f"**Author:** {inputs['author']}")
    if inputs["reviewers"]:
        lines.append(f"**Reviewers:** {inputs['reviewers']}")

    lines.append(f"\n**Problem statement:**\n{inputs['problem']}")

    if inputs["why_now"]:
        lines.append(f"\n**Why now:**\n{inputs['why_now']}")

    lines.append(f"\n**Target users:**\n{inputs['users']}")

    if inputs["personas"]:
        lines.append(f"\n**User personas:**\n{inputs['personas']}")
    if inputs["jtbd"]:
        lines.append(f"\n**User stories (JTBD):**\n{inputs['jtbd']}")

    lines.append(f"\n**Goals & success metrics:**\n{inputs['goals']}")

    if inputs["acceptance"]:
        lines.append(f"\n**Acceptance criteria:**\n{inputs['acceptance']}")
    if inputs["scope"]:
        lines.append(f"\n**Scope notes:**\n{inputs['scope']}")
    if inputs["assumptions"]:
        lines.append(f"\n**Assumptions:**\n{inputs['assumptions']}")
    if inputs["risks"]:
        lines.append(f"\n**Risks & dependencies:**\n{inputs['risks']}")
    if inputs["context"]:
        lines.append(f"\n**Additional context:**\n{inputs['context']}")

    return "\n".join(lines)


def sanitize_filename(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    return name[:60]


def generate_prd(style_guide: str, user_message: str) -> str:
    client = anthropic.Anthropic()
    print("\n" + "-" * 60)
    print("Generating your PRD...\n")

    output_chunks = []
    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=style_guide,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            output_chunks.append(text)

    print("\n" + "-" * 60)
    return "".join(output_chunks)


def save_prd(content: str, feature_name: str) -> Path:
    slug = sanitize_filename(feature_name)
    today = date.today().isoformat()
    filename = f"prd-{slug}-{today}.md"
    output_path = Path.cwd() / filename
    output_path.write_text(content, encoding="utf-8")
    return output_path


def main():
    try:
        style_guide = load_style_guide()
        inputs = collect_inputs()
        user_message = build_user_message(inputs)
        prd_content = generate_prd(style_guide, user_message)
        output_path = save_prd(prd_content, inputs["feature_name"])
        print(f"\nPRD saved to: {output_path}\n")
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(0)
    except anthropic.AuthenticationError:
        print("\nError: ANTHROPIC_API_KEY is missing or invalid.")
        print("Set it with: export ANTHROPIC_API_KEY=your-key-here")
        sys.exit(1)
    except anthropic.APIError as e:
        print(f"\nAPI error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
