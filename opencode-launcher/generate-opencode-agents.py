#!/usr/bin/env python3
"""
Generate OpenCode Agents - Creates agent definitions from system prompts.

Reads all personas from system-prompts/ and generates OpenCode agent
markdown files in ~/.config/opencode/agents/

Usage:
    python3 generate-opencode-agents.py
    generate-opencode-agents    # if in PATH
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict


# ============================================================================
# Configuration
# ============================================================================

LAUNCHER_DIR = Path(__file__).parent.parent
SYSTEM_PROMPTS_DIR = LAUNCHER_DIR / "system-prompts"
GLOBAL_PROMPTS_DIR = Path.home() / ".claude" / "system-prompts"
OPENCODE_AGENTS_DIR = Path.home() / ".config" / "opencode" / "agents"


# ============================================================================
# Data Parsing (copied from claude-launcher.py)
# ============================================================================


def parse_frontmatter(file_path: Path) -> Dict[str, str]:
    """Parse YAML frontmatter from prompt file."""
    metadata = {}
    try:
        with open(file_path) as f:
            first_line = f.readline().strip()
            if first_line != "---":
                return metadata

            for line in f:
                line = line.strip()
                if line == "---":
                    break
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error parsing {file_path}: {e}", file=sys.stderr)

    return metadata


def build_enforcement_index(embedded_metadata: list) -> str:
    if not embedded_metadata:
        return ""

    lines = [
        "\n---\n",
        "\n## Skill Activation Protocol\n",
        f"You have {len(embedded_metadata)} embedded skills. They are ALL active for this session.",
        "IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT. THIS IS NOT NEGOTIABLE.",
        "If you catch yourself violating a skill, STOP IMMEDIATELY, re-read the skill, and correct course.",
        "Before EVERY action, check: does this violate any embedded skill? If yes, DO NOT PROCEED.\n",
        "### Embedded Skills\n",
    ]
    for meta in embedded_metadata:
        lines.append(f"- **{meta['name']}**: {meta['description']}")
    return "\n".join(lines) + "\n"


def process_imports(file_path: Path, persona_name: str) -> str:
    """Process @ references and build system prompt."""
    result = []
    imports = []
    embedded_metadata = []
    errors = []

    with open(file_path) as f:
        first_line = f.readline().strip()
        if first_line == "---":
            for line in f:
                if line.strip() == "---":
                    break
        else:
            result.append(first_line + "\n")

        for line in f:
            match = re.match(r"^\s*-?\s*@([^\s]+)\s*$", line)
            if match:
                import_path = match.group(1)
                import_path = import_path.replace("~", str(Path.home()))
                if not import_path.startswith("/"):
                    import_path = str(file_path.parent / import_path)

                import_path = Path(import_path)
                if import_path.exists():
                    skill_dir = (
                        import_path.parent.name
                        if import_path.name == "SKILL.md"
                        else import_path.stem
                    )
                    print(f"  ✓ Found: {skill_dir}", file=sys.stderr)
                    skill_meta = parse_frontmatter(import_path)
                    skill_id = f"development-skills:{skill_dir}"
                    display_name = skill_meta.get("name", skill_dir)
                    imports.append({"id": skill_id, "display_name": display_name})
                    if "description" in skill_meta:
                        embedded_metadata.append(
                            {
                                "name": skill_id,
                                "description": skill_meta["description"]
                                .strip('"')
                                .strip("'"),
                            }
                        )
                    with open(import_path) as skill_file:
                        result.append(skill_file.read())
                        result.append("\n\n")
                else:
                    print(
                        f"  ✗ ERROR: Import file not found: {import_path}",
                        file=sys.stderr,
                    )
                    errors.append(str(import_path))
            else:
                result.append(line)

    if errors:
        print(f"\nERROR: Failed to load {len(errors)} import(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    header = "---\n"

    if imports:
        print(f"\nLoaded {len(imports)} skill(s) successfully", file=sys.stderr)
        header += "\n# Loaded Skills\n\n"
        header += (
            "The following skills have been loaded and are active for this session:\n\n"
        )
        for imp in imports:
            header += f"- **{imp['display_name']}** ({imp['id']})\n"
        header += "\n---\n\n"

    header += """# System Instructions

## Precedence

This persona system prompt takes precedence over the default system prompt. When there is a conflict, follow this system prompt's guidance.

---

"""

    body = "".join(result)
    enforcement = build_enforcement_index(embedded_metadata)
    return header + body + enforcement


# ============================================================================
# Main
# ============================================================================


def main():
    # Find all persona files
    prompt_dirs = [SYSTEM_PROMPTS_DIR, GLOBAL_PROMPTS_DIR]

    personas = {}
    for prompt_dir in prompt_dirs:
        if not prompt_dir.exists():
            continue

        for file_path in sorted(prompt_dir.glob("*.md")):
            metadata = parse_frontmatter(file_path)

            if "shortcut" in metadata:
                shortcut = metadata["shortcut"]
                personas[shortcut] = file_path
            elif "name" in metadata:
                # Use lowercase name as shortcut fallback
                name = metadata["name"].lower().replace(" ", "-")
                personas[name] = file_path

    if not personas:
        print("No personas found", file=sys.stderr)
        sys.exit(1)

    # Create OpenCode agents directory
    OPENCODE_AGENTS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Generating OpenCode agents in {OPENCODE_AGENTS_DIR}")
    print(f"Found {len(personas)} personas\n")

    # Generate agent files
    for shortcut, file_path in sorted(personas.items()):
        metadata = parse_frontmatter(file_path)
        name = metadata.get("name") or file_path.stem

        # Create slugified filename from full name
        slug = (
            name.lower()
            .replace(" ", "-")
            .replace("/", "-")
            .replace(":", "")
            .replace("\\", "")
        )

        print(f"Processing: {shortcut} → {name}")

        # Build system prompt
        system_prompt = process_imports(file_path, name)

        # Create agent markdown file with full name
        agent_file = OPENCODE_AGENTS_DIR / f"{slug}.md"

        with open(agent_file, "w") as f:
            f.write("---\n")
            f.write(f"description: {name}\n")
            f.write("mode: primary\n")
            f.write("---\n")
            f.write(system_prompt)

        print(f"  → Created: {agent_file.name}")

    print(f"\n✓ Generated {len(personas)} agents")
    print(f"\nTo use:")
    print(f"  1. Run: opencode")
    print(f"  2. Press Tab or use @agent-name to switch personas")


if __name__ == "__main__":
    main()
