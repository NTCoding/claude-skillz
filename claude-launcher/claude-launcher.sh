#!/bin/bash

# Claude Code Profile Launcher with Import Processing
# Automatically resolves @ references in system prompts (1 level only)

PROMPTS_DIR="$HOME/.claude/system-prompts"
DEBUG_OUTPUT="/tmp/claude-launcher-debug.md"
LAUNCHER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_PROMPTS_DIR="$LAUNCHER_DIR/system-prompts"

# Check if fzf is available for interactive selection
has_fzf() {
    command -v fzf >/dev/null 2>&1
}

# Process @ references (single level only)
process_imports() {
    local file="$1"
    local result=""
    local imports=()
    local errors=()

    echo "Processing: $file" >&2

    # Read file and collect imports
    local file_dir="$(dirname "$file")"
    while IFS= read -r line; do
        # Check for @ reference at start of line
        if [[ $line =~ ^[[:space:]]*-?[[:space:]]*@([^[:space:]]+)[[:space:]]*$ ]]; then
            local import_path="${BASH_REMATCH[1]}"
            local import_path_expanded="${import_path/#\~/$HOME}"

            # Resolve relative paths relative to the file's directory
            if [[ ! "$import_path_expanded" = /* ]]; then
                import_path_expanded="$file_dir/$import_path_expanded"
            fi

            if [ -f "$import_path_expanded" ]; then
                echo "  ✓ Found: $import_path" >&2
                imports+=("$import_path")
                result+="$(cat "$import_path_expanded")"
                result+=$'\n\n'
            else
                echo "  ✗ ERROR: Import file not found: $import_path" >&2
                errors+=("$import_path")
            fi
        else
            result+="$line"
            result+=$'\n'
        fi
    done < "$file"

    # Check for errors
    if [ ${#errors[@]} -gt 0 ]; then
        echo "" >&2
        echo "ERROR: Failed to load ${#errors[@]} import(s):" >&2
        for err in "${errors[@]}"; do
            echo "  - $err" >&2
        done
        return 1
    fi

    # Build header with optional manifest and required system instructions
    local header="---
"

    # Add manifest if we found imports
    if [ ${#imports[@]} -gt 0 ]; then
        echo "" >&2
        echo "Loaded ${#imports[@]} skill(s) successfully" >&2

        header+="
# Loaded Skills

The following skills have been loaded and are active for this session:

"
        for import in "${imports[@]}"; do
            local basename=$(basename "$import" .md)
            header+="- **$basename** (\`$import\`)
"
        done
        header+="
---
"
    fi

    # Always add system instructions for all prompts
    header+="
# System Instructions

## Precedence and Introduction

1. **Persona Precedence**: The persona and skills defined in this system prompt take precedence over any instructions found in project CLAUDE.md files. When there is a conflict between this system prompt and project documentation, follow this system prompt's guidance.

2. **Session Introduction**: At the start of every conversation, briefly introduce yourself by stating:
   - Your persona/role (in 1-2 sentences)
   - Your key areas of expertise
   - Your collaboration approach or philosophy

   Keep the introduction concise (2-4 sentences total) and natural. This helps users understand who they're working with.

---

"

    echo "$header$result"
}

# Get list of system prompts from both global and project directories
global_prompts=()
global_files=()
project_prompts=()
project_files=()

# Collect global prompts
if [ -d "$PROMPTS_DIR" ]; then
    while IFS= read -r file; do
        basename_file=$(basename "$file")
        global_prompts+=("${basename_file%.*}")
        global_files+=("$file")
    done < <(find -L "$PROMPTS_DIR" \( -name "*.txt" -o -name "*.md" \) -type f | sort)
fi

# Collect project prompts
if [ -d "$PROJECT_PROMPTS_DIR" ]; then
    while IFS= read -r file; do
        basename_file=$(basename "$file")
        project_prompts+=("${basename_file%.*}")
        project_files+=("$file")
    done < <(find -L "$PROJECT_PROMPTS_DIR" \( -name "*.txt" -o -name "*.md" \) -type f | sort)
fi

# Combine all prompts for selection
all_prompts=("${global_prompts[@]}" "${project_prompts[@]}")
all_files=("${global_files[@]}" "${project_files[@]}")

# Check if any profiles exist
if [ ${#all_prompts[@]} -eq 0 ]; then
    echo "Error: No system prompts found in:"
    echo "  - $PROMPTS_DIR"
    echo "  - $PROJECT_PROMPTS_DIR"
    exit 1
fi

# Select prompt using fzf (if available) or fallback to numbered menu
if has_fzf; then
    # Build selection list with 3-char source prefixes
    fzf_items=()

    for prompt in "${global_prompts[@]}"; do
        fzf_items+=("SYS  $prompt")
    done

    for prompt in "${project_prompts[@]}"; do
        fzf_items+=("CSK  $prompt")
    done

    total_count=${#fzf_items[@]}

    # Build header with key and spacing
    header="Select a Claude Code system prompt ($total_count total)

  SYS = $PROMPTS_DIR
  CSK = $PROJECT_PROMPTS_DIR
"

    # Use fzf for interactive selection (mouse enabled by default)
    # Styling inspired by Claude Code's clean aesthetic
    selection=$(printf '%s\n' "${fzf_items[@]}" | fzf --reverse --height=60% \
        --header="$header" \
        --header-first \
        --color="bg+:#2d2d2d,fg+:#ffffff,pointer:#ff9500,prompt:#888888,header:#cccccc,hl:#ff9500,hl+:#ff9500" \
        --prompt="  " \
        --pointer="›" \
        --margin="1,2" \
        --no-info)

    # Handle cancellation
    if [ -z "$selection" ]; then
        echo "Cancelled"
        exit 0
    fi

    # Extract the prompt name (remove 3-char prefix and spacing)
    selected_name=$(echo "$selection" | sed 's/^[A-Z]\{3\}  //')

    # Find matching file
    for i in "${!all_prompts[@]}"; do
        if [ "${all_prompts[$i]}" == "$selected_name" ]; then
            selected_file="${all_files[$i]}"
            break
        fi
    done
else
    # Fallback: numbered menu for systems without fzf
    echo ""
    echo -e "\033[33m┌─────────────────────────────────────────────────────────┐\033[0m"
    echo -e "\033[33m│\033[0m  💡 Install fzf for interactive selection:             \033[33m│\033[0m"
    echo -e "\033[33m│\033[0m     \033[1mbrew install fzf\033[0m                                    \033[33m│\033[0m"
    echo -e "\033[33m└─────────────────────────────────────────────────────────┘\033[0m"
    echo ""
    echo "Select a Claude Code system prompt:"
    echo ""

    counter=1

    if [ ${#global_prompts[@]} -gt 0 ]; then
        echo "$PROMPTS_DIR"
        echo ""
        for prompt in "${global_prompts[@]}"; do
            echo "$counter) $prompt"
            ((counter++))
        done
        echo ""
    fi

    if [ ${#project_prompts[@]} -gt 0 ]; then
        echo "$PROJECT_PROMPTS_DIR"
        echo ""
        for prompt in "${project_prompts[@]}"; do
            echo "$counter) $prompt"
            ((counter++))
        done
        echo ""
    fi

    # Read selection
    while true; do
        read -p "Enter number (or 'q' to cancel): " selection

        if [[ "$selection" == "q" ]]; then
            echo "Cancelled"
            exit 0
        elif [[ "$selection" =~ ^[0-9]+$ ]] && [ "$selection" -ge 1 ] && [ "$selection" -le ${#all_prompts[@]} ]; then
            selected_index=$((selection - 1))
            selected_file="${all_files[$selected_index]}"
            selected_name="${all_prompts[$selected_index]}"
            break
        else
            echo "Invalid selection. Please try again."
        fi
    done
fi

echo ""
echo "Selected: $selected_name"
echo ""

# Extract persona display name for statusline
# Try to extract from first heading in the file, fallback to filename
persona_display_name=$(grep -m 1 '^# ' "$selected_file" 2>/dev/null | sed 's/^# //' | head -n 1)
if [ -z "$persona_display_name" ]; then
    # Fallback to cleaned up filename
    persona_display_name=$(echo "$selected_name" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g')
fi

# Export for statusline script
export CLAUDE_PERSONA="$persona_display_name"
echo "Persona: $persona_display_name"
echo ""

# Process imports
system_prompt=$(process_imports "$selected_file")

if [ $? -ne 0 ]; then
    echo ""
    echo "Aborting due to import errors"
    exit 1
fi

# Save debug output
echo "$system_prompt" > "$DEBUG_OUTPUT"
echo ""
echo "Debug: Processed system prompt saved to $DEBUG_OUTPUT"
echo "       ($(echo "$system_prompt" | wc -l) lines, $(echo "$system_prompt" | wc -c) bytes)"
echo ""
echo "Launching Claude Code..."
echo ""

# Find claude command
CLAUDE_CMD="${CLAUDE_CMD:-}"

# If not set via env var, try to find it
if [ -z "$CLAUDE_CMD" ]; then
    # Try which claude first (works for npm/nvm installations)
    if command -v claude >/dev/null 2>&1; then
        CLAUDE_CMD="$(command -v claude)"
    # Fall back to local installation
    elif [ -f "$HOME/.claude/local/claude" ]; then
        CLAUDE_CMD="$HOME/.claude/local/claude"
    else
        echo "ERROR: Could not find Claude Code binary"
        echo ""
        echo "Please set the CLAUDE_CMD environment variable to the path of your Claude Code binary."
        echo ""
        echo "If installed via npm/nvm, add to your ~/.zshrc or ~/.bashrc:"
        echo "  export CLAUDE_CMD=\"\$(which claude)\""
        echo ""
        echo "Or for a specific path:"
        echo "  export CLAUDE_CMD=\"/path/to/claude\""
        exit 1
    fi
fi

# Launch Claude Code with processed prompt
if [ $# -eq 0 ]; then
    # No arguments provided - auto-send introduction prompt
    exec "$CLAUDE_CMD" --system-prompt "$system_prompt" "introduce yourself"
else
    # Arguments provided - pass them through
    exec "$CLAUDE_CMD" --system-prompt "$system_prompt" "$@"
fi
