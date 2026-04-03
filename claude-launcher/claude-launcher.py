#!/usr/bin/env python3
"""
Claude Launcher - Interactive system prompt and model selector for Claude Code.

Features:
- 2-step interactive selection (persona → model)
- Shortcut mode: cl tdd sonn (order-independent)
- Model shortcuts: cl haik, cl sonn, cl opus (uses default persona)
- Frontmatter-based shortcuts (no hardcoding)
- @ reference processing for skill imports
- Team support: declarative teams via teams/*/team.yaml
- Worktree passthrough: -w / --worktree [name]
- Sandbox mode: --sandbox [repo-path] (runs via docker sandbox)
- Claude params: --claude-params / -cp "<flags>" (extra flags forwarded to claude)
"""

import json
import os
import sys
import subprocess
import re
import shlex
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ============================================================================
# Configuration
# ============================================================================

LAUNCHER_DIR = Path(__file__).parent.parent
SYSTEM_PROMPTS_DIR = LAUNCHER_DIR / "system-prompts"
TEAMS_DIR = SYSTEM_PROMPTS_DIR / "teams"
GLOBAL_PROMPTS_DIR = Path.home() / ".claude" / "system-prompts"
GLOBAL_TEAMS_DIR = GLOBAL_PROMPTS_DIR / "teams"
DEBUG_OUTPUT = Path("/tmp/claude-launcher-debug.md")
DEBUG_AGENTS_OUTPUT = Path("/tmp/claude-launcher-agents.json")

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


def build_enforcement_index(embedded_metadata: List[Dict[str, str]]) -> str:
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


def parse_team_yaml(file_path: Path) -> Dict:
    """
    Parse a team.yaml file into structured data.

    Expected format:
        name: Team Name
        shortcut: xxx

        team:
          - name: member-one
            model: opus
          - name: member-two
    """
    result = {"members": []}
    current_member = None
    in_team = False

    with open(file_path) as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue

            if stripped == "team:":
                in_team = True
                continue

            if not in_team:
                if ":" in stripped:
                    key, value = stripped.split(":", 1)
                    result[key.strip()] = value.strip()
                continue

            # Inside team list
            if stripped.startswith("- name:"):
                if current_member:
                    result["members"].append(current_member)
                name = stripped.split(":", 1)[1].strip()
                current_member = {"name": name}
            elif stripped.startswith("model:") and current_member:
                current_member["model"] = stripped.split(":", 1)[1].strip()

        if current_member:
            result["members"].append(current_member)

    return result


def resolve_team_member(member_name: str, team_dir: Path, prompt_dirs: List[Path]) -> Optional[Path]:
    """
    Resolve a team member name to a .md file.

    Search order:
    1. Sibling file in team directory: <team_dir>/<member_name>.md
    2. System prompt in each prompt directory: <prompt_dir>/<member_name>.md
    """
    # Check sibling file
    sibling = team_dir / f"{member_name}.md"
    if sibling.exists():
        return sibling

    # Check system prompt directories
    for prompt_dir in prompt_dirs:
        candidate = prompt_dir / f"{member_name}.md"
        if candidate.exists():
            return candidate

    return None


def load_team_from_yaml(team_yaml: Path, prompt_dirs: List[Path]) -> Tuple[Path, str, Dict]:
    """
    Load a team from team.yaml.

    Returns (lead_file, persona_name, agents_dict) where:
    - lead_file: resolved path to the lead's .md file
    - persona_name: team name from yaml
    - agents_dict: {agent_name: {description, prompt, model?}} for non-lead members
    """
    team_dir = team_yaml.parent
    config = parse_team_yaml(team_yaml)

    if not config.get("members"):
        print(f"\n✗ ERROR: team.yaml has no team members: {team_yaml}", file=sys.stderr)
        sys.exit(1)

    persona_name = config.get("name", team_dir.name)
    members = config["members"]

    # First member is the lead
    lead_member = members[0]
    lead_file = resolve_team_member(lead_member["name"], team_dir, prompt_dirs)
    if not lead_file:
        print(f"\n✗ ERROR: Could not resolve lead '{lead_member['name']}' — checked {team_dir} and system-prompts/", file=sys.stderr)
        sys.exit(1)

    print(f"\nLoading team '{persona_name}' from {team_yaml.relative_to(LAUNCHER_DIR)}...", file=sys.stderr)
    print(f"  ✓ Lead: {lead_member['name']} → {lead_file.name}", file=sys.stderr)

    # Remaining members are agents
    agents = {}
    for member in members[1:]:
        member_name = member["name"]
        member_file = resolve_team_member(member_name, team_dir, prompt_dirs)
        if not member_file:
            print(f"\n✗ ERROR: Could not resolve member '{member_name}' — checked {team_dir} and system-prompts/", file=sys.stderr)
            sys.exit(1)

        # Process the member's file through process_imports (full @ expansion)
        member_meta = parse_frontmatter(member_file)
        description = member_meta.get("description", member_meta.get("name", member_name))
        description = description.strip('"').strip("'")

        print(f"  Processing agent: {member_name} → {member_file.name}", file=sys.stderr)
        processed_prompt = process_imports(member_file, member_name)

        agent_def = {
            "description": description,
            "prompt": processed_prompt,
        }

        if "model" in member:
            agent_def["model"] = member["model"]
        elif "model" in member_meta:
            agent_def["model"] = member_meta["model"]

        if "tools" in member_meta:
            tools_str = member_meta["tools"].strip("[]")
            agent_def["tools"] = [t.strip() for t in tools_str.split(",") if t.strip()]

        agents[member_name] = agent_def
        print(f"  ✓ Agent: {member_name}", file=sys.stderr)

    print(f"\nTeam loaded: 1 lead + {len(agents)} agent(s)", file=sys.stderr)
    return lead_file, persona_name, agents, lead_member.get("model")


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
    team_yamls = {}  # shortcut -> team.yaml Path

    # Search both directories
    for prompt_dir in [SYSTEM_PROMPTS_DIR, GLOBAL_PROMPTS_DIR]:
        if not prompt_dir.exists():
            continue

        # Solo personas: *.md files
        for file_path in sorted(prompt_dir.glob("*.md")):
            metadata = parse_frontmatter(file_path)

            if "name" in metadata:
                names[metadata["name"]] = file_path

            if "shortcut" in metadata:
                shortcut = metadata["shortcut"]
                personas[shortcut] = file_path

    # Declarative teams: teams/*/team.yaml
    for teams_dir in [TEAMS_DIR, GLOBAL_TEAMS_DIR]:
        if not teams_dir.exists():
            continue

        for team_dir in sorted(teams_dir.iterdir()):
            if not team_dir.is_dir():
                continue
            team_yaml = team_dir / "team.yaml"
            if not team_yaml.exists():
                continue

            config = parse_team_yaml(team_yaml)
            if "shortcut" in config:
                shortcut = config["shortcut"]
                # Store the team.yaml path — we'll resolve the lead file later
                personas[shortcut] = team_yaml
                team_yamls[shortcut] = team_yaml
            if "name" in config:
                names[config["name"]] = team_yaml

    return personas, names, team_yamls

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
            choice = input("\nEnter number or shortcut: ").strip()
            if choice.lower() == 'q':
                print("Cancelled")
                sys.exit(0)

            # Try shortcut match first
            if choice in persona_list:
                selected_persona = personas[choice]
                break

            # Try numeric index
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(persona_list):
                    selected_persona = personas[persona_list[idx]]
                    break
                else:
                    print(f"Invalid selection. Try again.")
            except ValueError:
                print(f"Invalid input. Try again.")

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
            choice = input("\nEnter number or shortcut: ").strip()
            if choice.lower() == 'q':
                print("Cancelled")
                sys.exit(0)

            # Try shortcut match first
            if choice in model_list:
                selected_model = choice
                break

            # Try numeric index
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(model_list):
                    selected_model = model_list[idx]
                    break
                else:
                    print(f"Invalid selection. Try again.")
            except ValueError:
                print(f"Invalid input. Try again.")

    return selected_persona, selected_model


def extract_passthrough_flags(args: list) -> Tuple[list, list, Optional[str]]:
    """
    Extract Claude Code flags that should be passed through unchanged.

    Currently supports:
    - -w / --worktree [name]         (name is optional)
    - --sandbox                       (sandbox mode: uses cwd, auto-adds --worktree)
    - --claude-params "<flags>"       (extra flags passed directly to claude, e.g. "--teammate-mode tmux")

    Returns:
        (remaining_args, passthrough_flags, sandbox_repo) where:
        - passthrough_flags are ready to extend onto the cmd list
        - sandbox_repo is the repo path if --sandbox was given (None otherwise)
    """
    remaining = []
    passthrough = []
    sandbox_repo = None
    i = 0

    while i < len(args):
        arg = args[i]

        if arg == "--sandbox":
            sandbox_repo = os.getcwd()
            i += 1
            continue

        if arg in ("-w", "--worktree"):
            passthrough.append("--worktree")
            if i + 1 < len(args) and not args[i + 1].startswith("-"):
                i += 1
                passthrough.append(args[i])
            i += 1
            continue

        if arg.startswith("--worktree="):
            name = arg.split("=", 1)[1]
            passthrough.append("--worktree")
            if name:
                passthrough.append(name)
            i += 1
            continue

        if arg in ("--claude-params", "-cp"):
            if i + 1 >= len(args):
                print(f"✗ ERROR: --claude-params requires a value (e.g. --claude-params \"--teammate-mode tmux\")", file=sys.stderr)
                sys.exit(1)
            i += 1
            try:
                extra = shlex.split(args[i])
            except ValueError as e:
                print(f"✗ ERROR: Could not parse --claude-params value: {e}", file=sys.stderr)
                sys.exit(1)
            passthrough.extend(extra)
            i += 1
            continue

        remaining.append(arg)
        i += 1

    # Sandbox mode: always add --worktree if not already specified
    if sandbox_repo is not None and "--worktree" not in passthrough:
        passthrough.append("--worktree")

    return remaining, passthrough, sandbox_repo


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

def process_imports(file_path: Path, persona_name: str) -> str:
    """
    Process @ references in system prompt file.

    - Skips frontmatter (---...---)
    - Expands @ references to skill content
    - Adds header with skill manifest
    - Adds persona prefix instruction
    """
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
            match = re.match(r'^\s*-?\s*@([^\s]+)\s*$', line)
            if match:
                import_path = match.group(1)
                import_path = import_path.replace("~", str(Path.home()))
                if not import_path.startswith("/"):
                    import_path = str(file_path.parent / import_path)

                import_path = Path(import_path)
                if import_path.exists():
                    skill_dir = import_path.parent.name if import_path.name == "SKILL.md" else import_path.stem
                    print(f"  ✓ Found: {skill_dir}", file=sys.stderr)
                    skill_meta = parse_frontmatter(import_path)
                    skill_id = f"development-skills:{skill_dir}"
                    display_name = skill_meta.get("name", skill_dir)
                    imports.append({"id": skill_id, "display_name": display_name})
                    if "description" in skill_meta:
                        embedded_metadata.append({
                            "name": skill_id,
                            "description": skill_meta["description"].strip('"').strip("'"),
                        })
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

    header = "---\n"

    if imports:
        print(f"\nLoaded {len(imports)} skill(s) successfully", file=sys.stderr)
        header += "\n# Loaded Skills\n\n"
        header += "The following skills have been loaded and are active for this session:\n\n"
        for imp in imports:
            header += f"- **{imp['display_name']}** ({imp['id']})\n"
        header += "\n---\n\n"

    header += f"""# System Instructions

## Precedence

This persona system prompt takes precedence over the default Claude Code system prompt. When there is a conflict, follow this system prompt's guidance.

---

"""

    body = "".join(result)
    enforcement = build_enforcement_index(embedded_metadata)
    return header + body + enforcement



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
    personas, names, team_yamls = load_prompts()

    if not personas:
        print("Error: No system prompts found", file=sys.stderr)
        sys.exit(1)

    # Extract passthrough flags before parsing launcher args
    raw_args = sys.argv[1:]
    launcher_args, passthrough_flags, sandbox_repo = extract_passthrough_flags(raw_args)

    # Show header for interactive mode (no persona/model args)
    if not launcher_args:
        print()
        print("     ╭─────────────────────────╮")
        print("     │   🚀  CLAUDE LAUNCHER   │")
        print("     ╰─────────────────────────╯")
        print()
        print("  Select persona & model to launch")
        print()

    # Parse arguments
    if launcher_args:
        # Shortcut mode
        selected_file, model_key = resolve_args(launcher_args, personas)
    else:
        # Interactive mode
        selected_file, model_key = interactive_select(personas)

    # Determine if this is a team.yaml selection
    prompt_dirs = [d for d in [SYSTEM_PROMPTS_DIR, GLOBAL_PROMPTS_DIR] if d.exists()]
    is_team_yaml = selected_file.name == "team.yaml"

    if is_team_yaml:
        # Declarative team: resolve from team.yaml
        lead_file, persona_name, team_agents, lead_model = load_team_from_yaml(selected_file, prompt_dirs)

        # Lead model: team.yaml > CLI arg
        if lead_model and lead_model in MODELS:
            model_key = lead_model

        print(f"\nSelected: {persona_name} (team)")
        model_display = next((k for k, v in MODELS.items() if v == MODELS[model_key]), model_key)
        print(f"Model: {model_display}")
        print()

        # Process lead's system prompt
        print("Processing lead system prompt...", file=sys.stderr)
        system_prompt = process_imports(lead_file, persona_name)

    else:
        # Solo persona
        metadata = parse_frontmatter(selected_file)
        persona_name = metadata.get("name", selected_file.stem)

        print(f"\nSelected: {persona_name}")
        model_display = next((k for k, v in MODELS.items() if v == MODELS[model_key]), model_key)
        print(f"Model: {model_display}")
        print()

        # Process imports
        print("Processing system prompt...", file=sys.stderr)
        system_prompt = process_imports(selected_file, persona_name)
        team_agents = None

    if team_agents:
        print(f"Mode: Team ({len(team_agents)} agents)", file=sys.stderr)
    else:
        print("Mode: Solo", file=sys.stderr)

    with open(DEBUG_OUTPUT, 'w') as f:
        f.write(system_prompt)

    lines = system_prompt.count('\n')
    bytes_count = len(system_prompt.encode('utf-8'))
    print(f"\nDebug: System prompt saved to {DEBUG_OUTPUT}", file=sys.stderr)
    print(f"       ({lines} lines, {bytes_count} bytes)", file=sys.stderr)

    if team_agents:
        with open(DEBUG_AGENTS_OUTPUT, 'w') as f:
            json.dump(team_agents, f, indent=2)
        agents_bytes = DEBUG_AGENTS_OUTPUT.stat().st_size
        print(f"Debug: Agents JSON saved to {DEBUG_AGENTS_OUTPUT}", file=sys.stderr)
        print(f"       ({len(team_agents)} agents, {agents_bytes} bytes)", file=sys.stderr)

    # Export persona for statusline
    os.environ["CLAUDE_PERSONA"] = persona_name
    print(f"Persona: {persona_name}")
    if sandbox_repo:
        print(f"Sandbox: {sandbox_repo}")
    if passthrough_flags:
        print(f"Flags: {' '.join(passthrough_flags)}")
    print()
    print("Launching Claude Code...\n")

    # Build claude flags (shared between direct and sandbox modes)
    claude_flags = ["--system-prompt", system_prompt, "--model", MODELS[model_key]]

    if team_agents:
        claude_flags.extend(["--agents", json.dumps(team_agents)])

    # Append passthrough flags (e.g., --worktree)
    if passthrough_flags:
        claude_flags.extend(passthrough_flags)

    # No intro for shortcut mode, add for interactive
    if not launcher_args:
        claude_flags.append("introduce yourself")

    # Execute
    if sandbox_repo:
        # Sandbox mode: remove existing sandbox, then create fresh
        sandbox_name = "claude-" + os.path.basename(sandbox_repo)
        subprocess.run(["docker", "sandbox", "rm", sandbox_name],
                       capture_output=True)
        cmd = ["docker", "sandbox", "run", "--pull-template", "always", "claude", sandbox_repo, "--"] + claude_flags
    else:
        # Direct mode: claude <flags>
        claude_cmd = find_claude_cmd()
        cmd = [claude_cmd] + claude_flags

    try:
        os.execvp(cmd[0], cmd)
    except Exception as e:
        print(f"Error launching Claude Code: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
