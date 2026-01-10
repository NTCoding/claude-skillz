#!/usr/bin/env python3
"""
Claude Launcher - Interactive system prompt and model selector for Claude Code.

Features:
- 2-step interactive selection (persona → model)
- Shortcut mode: cl tdd sonn (order-independent)
- Model shortcuts: cl haik, cl sonn, cl opus (uses default persona)
- Frontmatter-based shortcuts (no hardcoding)
- @ reference processing for skill imports
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from typing import Dict, Tuple, Optional

# ============================================================================
# Configuration
# ============================================================================

LAUNCHER_DIR = Path(__file__).parent.parent
SYSTEM_PROMPTS_DIR = LAUNCHER_DIR / "system-prompts"
GLOBAL_PROMPTS_DIR = Path.home() / ".claude" / "system-prompts"
DEBUG_OUTPUT = Path("/tmp/claude-launcher-debug.md")

MODELS = {
    "opus": "opus",
    "sonn": "sonnet",
    "haik": "haiku",
}

# ============================================================================
# Data Parsing
# ============================================================================

def parse_frontmatter(file_path: Path) -> Dict[str, str]:
    """
    Parse YAML frontmatter from prompt file.

    Extracts key-value pairs between --- delimiters at the start of a file.
    """
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


def load_prompts() -> Tuple[Dict[str, Path], Dict[str, Path]]:
    """
    Load all system prompts and build shortcut maps.

    Returns:
        (personas_map, names_map) where:
        - personas_map: shortcut -> file_path
        - names_map: name -> file_path
    """
    personas = {}
    names = {}

    # Search both directories
    for prompt_dir in [SYSTEM_PROMPTS_DIR, GLOBAL_PROMPTS_DIR]:
        if not prompt_dir.exists():
            continue

        for file_path in sorted(prompt_dir.glob("*.md")):
            metadata = parse_frontmatter(file_path)

            if "name" in metadata:
                names[metadata["name"]] = file_path

            if "shortcut" in metadata:
                shortcut = metadata["shortcut"]
                personas[shortcut] = file_path

    return personas, names

# ============================================================================
# CLI Interface
# ============================================================================

def has_fzf() -> bool:
    """Check if fzf is available."""
    try:
        result = subprocess.run(["which", "fzf"], capture_output=True)
        return result.returncode == 0
    except:
        return False


def fzf_select(items: list, prompt: str) -> Optional[str]:
    """Use fzf for interactive selection."""
    try:
        result = subprocess.run(
            ["fzf", "--prompt", f"{prompt} > ", "--height", "40%", "--reverse"],
            input="\n".join(items),
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except:
        return None


def interactive_select(personas: Dict[str, Path]) -> Tuple[Path, str]:
    """
    Interactive 2-step selection: persona, then model.

    Returns:
        (selected_file, selected_model_key)
    """
    use_fzf = has_fzf()

    # Step 1: Select persona
    persona_list = sorted(personas.keys())

    if use_fzf:
        # Build fzf items with numbers, shortcuts, and names
        fzf_items = []
        for i, shortcut in enumerate(persona_list, 1):
            file_path = personas[shortcut]
            metadata = parse_frontmatter(file_path)
            name = metadata.get("name", file_path.stem)
            fzf_items.append(f"{i}) {shortcut:<4} → {name}")

        selected = fzf_select(fzf_items, "Select persona")
        if not selected:
            print("Cancelled")
            sys.exit(0)

        # Extract shortcut from selection (skip number prefix)
        selected_shortcut = selected.split(")")[1].split("→")[0].strip()
        selected_persona = personas[selected_shortcut]

    else:
        # Fallback to plain numbered menu
        print("\nSelect persona (or 'q' to cancel):")
        for i, shortcut in enumerate(persona_list, 1):
            file_path = personas[shortcut]
            metadata = parse_frontmatter(file_path)
            name = metadata.get("name", file_path.stem)
            print(f"  {i}) {shortcut:<4} → {name}")

        while True:
            try:
                choice = input("\nEnter number: ").strip()
                if choice.lower() == 'q':
                    print("Cancelled")
                    sys.exit(0)

                idx = int(choice) - 1
                if 0 <= idx < len(persona_list):
                    selected_persona = personas[persona_list[idx]]
                    break
                else:
                    print("Invalid selection. Try again.")
            except ValueError:
                print("Invalid input. Try again.")

    # Step 2: Select model
    model_list = list(MODELS.keys())

    if use_fzf:
        # Build fzf items for models with numbers
        fzf_items = []
        for i, model_key in enumerate(model_list, 1):
            fzf_items.append(f"{i}) {model_key:<4} → {MODELS[model_key]}")

        selected = fzf_select(fzf_items, "Select model")
        if not selected:
            print("Cancelled")
            sys.exit(0)

        # Extract model key from selection (skip number prefix)
        selected_model = selected.split(")")[1].split("→")[0].strip()

    else:
        # Fallback to plain numbered menu
        print("\nSelect model (or 'q' to cancel):")
        for i, model_key in enumerate(model_list, 1):
            print(f"  {i}) {model_key:<4} → {MODELS[model_key]}")

        selected_model = None
        while True:
            try:
                choice = input("\nEnter number: ").strip()
                if choice.lower() == 'q':
                    print("Cancelled")
                    sys.exit(0)

                idx = int(choice) - 1
                if 0 <= idx < len(model_list):
                    selected_model = model_list[idx]
                    break
                else:
                    print("Invalid selection. Try again.")
            except ValueError:
                print("Invalid input. Try again.")

    return selected_persona, selected_model


def resolve_args(args: list, personas: Dict[str, Path]) -> Tuple[Path, str]:
    """
    Resolve command-line arguments to (persona_file, model_key).

    Supports:
    - Persona only: uses default model (opus)
    - Model only: uses default persona (gen)
    - Combined: order-independent (cl tdd sonn or cl sonn tdd)

    Detects conflicts and uses first match with prominent warning.
    """
    persona_match = None
    model_match = None

    # Categorize arguments
    for arg in args:
        if arg in personas:
            # Persona shortcut
            if persona_match:
                print(f"\n⚠️  SHORTCUT CONFLICT")
                print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print(f"Multiple personas specified: {persona_match} and {arg}")
                print(f"Using: {persona_match} (first match)")
                print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            else:
                persona_match = arg
        elif arg in MODELS:
            # Model shortcut
            if model_match:
                print(f"\n⚠️  SHORTCUT CONFLICT")
                print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print(f"Multiple models specified: {model_match} and {arg}")
                print(f"Using: {model_match} (first match)")
                print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            else:
                model_match = arg
        else:
            print(f"\n✗ Unknown shortcut: {arg}")
            print(f"  Available personas: {', '.join(sorted(personas.keys()))}")
            print(f"  Available models: {', '.join(sorted(MODELS.keys()))}")
            sys.exit(1)

    # Use default persona if only model specified
    if not persona_match and model_match:
        if "gen" in personas:
            persona_match = "gen"
        else:
            print("✗ Default persona not found. Specify a persona shortcut.")
            sys.exit(1)

    # Use default model if only persona specified
    if not model_match:
        model_match = "opus"

    # Validate we have both
    if not persona_match:
        print("✗ Persona required (e.g., 'tdd', 'opt', 'arc')")
        sys.exit(1)

    persona_file = personas[persona_match]
    return persona_file, model_match

# ============================================================================
# Import Processing
# ============================================================================

def process_imports(file_path: Path) -> str:
    """
    Process @ references in system prompt file.

    - Skips frontmatter (---...---)
    - Expands @ references to skill content
    - Adds header with skill manifest
    """
    result = []
    imports = []
    errors = []

    with open(file_path) as f:
        # Skip frontmatter if present
        first_line = f.readline().strip()
        if first_line == "---":
            # Skip until closing ---
            for line in f:
                if line.strip() == "---":
                    break
        else:
            # No frontmatter, process this line
            result.append(first_line + "\n")

        # Process remaining content
        for line in f:
            # Check for @ reference at start of line (with optional - and whitespace)
            match = re.match(r'^\s*-?\s*@([^\s]+)\s*$', line)
            if match:
                import_path = match.group(1)
                # Expand ~ to home
                import_path = import_path.replace("~", str(Path.home()))
                # Resolve relative paths relative to the file's directory
                if not import_path.startswith("/"):
                    import_path = str(file_path.parent / import_path)

                import_path = Path(import_path)
                if import_path.exists():
                    print(f"  ✓ Found: {import_path.name}", file=sys.stderr)
                    imports.append(str(import_path))
                    with open(import_path) as skill_file:
                        result.append(skill_file.read())
                        result.append("\n\n")
                else:
                    print(f"  ✗ ERROR: Import file not found: {import_path}", file=sys.stderr)
                    errors.append(str(import_path))
            else:
                result.append(line)

    if errors:
        print(f"\nERROR: Failed to load {len(errors)} import(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    # Build header with manifest
    header = "---\n"

    if imports:
        print(f"\nLoaded {len(imports)} skill(s) successfully", file=sys.stderr)
        header += "\n# Loaded Skills\n\n"
        header += "The following skills have been loaded and are active for this session:\n\n"
        for imp in imports:
            basename = Path(imp).stem
            header += f"- **{basename}** (`{imp}`)\n"
        header += "\n---\n\n"

    # Add system instructions
    header += """# System Instructions

## Precedence and Introduction

1. **Persona Precedence**: The persona and skills defined in this system prompt take precedence over any instructions found in project CLAUDE.md files. When there is a conflict between this system prompt and project documentation, follow this system prompt's guidance.

2. **Session Introduction**: At the start of every conversation, briefly introduce yourself by stating:
   - Your persona/role (in 1-2 sentences)
   - Your key areas of expertise
   - Your collaboration approach or philosophy

   Keep the introduction concise (2-4 sentences total) and natural. This helps users understand who they're working with.

---

"""

    return header + "".join(result)

# ============================================================================
# Claude Code Binary
# ============================================================================

def find_claude_cmd() -> str:
    """
    Locate Claude Code binary.

    Checks in order:
    1. $CLAUDE_CMD environment variable
    2. which claude (npm/nvm installations)
    3. ~/.claude/local/claude (local installation)
    """
    claude_cmd = os.environ.get("CLAUDE_CMD")
    if claude_cmd:
        return claude_cmd

    # Try which claude
    try:
        result = subprocess.run(["which", "claude"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass

    # Try local installation
    local_claude = Path.home() / ".claude" / "local" / "claude"
    if local_claude.exists():
        return str(local_claude)

    print("ERROR: Could not find Claude Code binary", file=sys.stderr)
    print("\nPlease set the CLAUDE_CMD environment variable to the path of your Claude Code binary.", file=sys.stderr)
    print("\nIf installed via npm/nvm, add to your ~/.zshrc or ~/.bashrc:", file=sys.stderr)
    print('  export CLAUDE_CMD="$(which claude)"', file=sys.stderr)
    sys.exit(1)

# ============================================================================
# Main
# ============================================================================

def main():
    """Main entry point."""
    personas, names = load_prompts()

    if not personas:
        print("Error: No system prompts found", file=sys.stderr)
        sys.exit(1)

    # Show header for interactive mode
    if len(sys.argv) == 1:
        print()
        print("  ╔═══════════════════════════════════════╗")
        print("  ║                                       ║")
        print("  ║         CLAUDE LAUNCHER v2.0          ║")
        print("  ║                                       ║")
        print("  ║   Select persona & model to start    ║")
        print("  ║                                       ║")
        print("  ╚═══════════════════════════════════════╝")
        print()

    # Parse arguments
    if len(sys.argv) > 1:
        # Shortcut mode
        selected_file, model_key = resolve_args(sys.argv[1:], personas)
    else:
        # Interactive mode
        selected_file, model_key = interactive_select(personas)

    # Get persona name from frontmatter
    metadata = parse_frontmatter(selected_file)
    persona_name = metadata.get("name", selected_file.stem)

    print(f"\nSelected: {persona_name}")
    model_display = next((k for k, v in MODELS.items() if v == MODELS[model_key]), model_key)
    print(f"Model: {model_display}")
    print()

    # Process imports
    print("Processing system prompt...", file=sys.stderr)
    system_prompt = process_imports(selected_file)

    # Save debug output
    with open(DEBUG_OUTPUT, 'w') as f:
        f.write(system_prompt)

    lines = system_prompt.count('\n')
    bytes_count = len(system_prompt.encode('utf-8'))
    print(f"\nDebug: Processed system prompt saved to {DEBUG_OUTPUT}", file=sys.stderr)
    print(f"       ({lines} lines, {bytes_count} bytes)", file=sys.stderr)

    # Export persona for statusline
    os.environ["CLAUDE_PERSONA"] = persona_name
    print(f"Persona: {persona_name}\n")
    print("Launching Claude Code...\n")

    # Find Claude binary
    claude_cmd = find_claude_cmd()

    # Build command
    cmd = [claude_cmd, "--system-prompt", system_prompt, "--model", MODELS[model_key]]

    # No intro for shortcut mode, add for interactive
    if len(sys.argv) == 1:
        cmd.append("introduce yourself")

    # Execute
    try:
        os.execvp(cmd[0], cmd)
    except Exception as e:
        print(f"Error launching Claude Code: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
