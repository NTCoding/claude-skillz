#!/bin/bash

# Claude Code Profile Launcher with Import Processing
# Automatically resolves @ references in system prompts (1 level only)

PROMPTS_DIR="$HOME/.claude/system-prompts"
DEBUG_OUTPUT="/tmp/claude-launcher-debug.md"
LAUNCHER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_PROMPTS_DIR="$LAUNCHER_DIR/system-prompts"

# Process @ references (single level only)
process_imports() {
    local file="$1"
    local result=""
    local imports=()
    local errors=()

    echo "Processing: $file" >&2

    # Read file and collect imports
    while IFS= read -r line; do
        # Check for @ reference at start of line
        if [[ $line =~ ^[[:space:]]*-?[[:space:]]*@([^[:space:]]+)[[:space:]]*$ ]]; then
            local import_path="${BASH_REMATCH[1]}"
            local import_path_expanded="${import_path/#\~/$HOME}"

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

    # Add manifest header if we found imports
    if [ ${#imports[@]} -gt 0 ]; then
        echo "" >&2
        echo "Loaded ${#imports[@]} skill(s) successfully" >&2

        local manifest="---

# Loaded Skills

The following skills have been loaded and are active for this session:

"
        for import in "${imports[@]}"; do
            local basename=$(basename "$import" .md)
            manifest+="- **$basename** (\`$import\`)
"
        done
        manifest+="
---

"
        echo "$manifest$result"
    else
        echo "$result"
    fi
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

# Display menu with headings
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

echo ""
echo "Selected: $selected_name"
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

# Launch Claude Code with processed prompt
exec claude --system-prompt "$system_prompt" "$@"
