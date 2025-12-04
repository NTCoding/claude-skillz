#!/usr/bin/env bash
set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "ERROR: jq is required but not installed." >&2
  echo "Install with: brew install jq (macOS) or apt-get install jq (Linux)" >&2
  exit 0
fi

COMMAND="${1:-}"

if [[ -z "$COMMAND" ]]; then
  echo "Usage: $0 {log|review}" >&2
  exit 1
fi

timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

log_event() {
  local session_id="$1"
  local event_type="$2"
  shift 2

  local log_file="/tmp/event-log-${session_id}.jsonl"
  touch "$log_file"

  local event_json
  case "$event_type" in
    file_modified)
      local file="$1"
      local tool="$2"
      event_json=$(jq -nc \
        --arg ts "$(timestamp)" \
        --arg event "$event_type" \
        --arg file "$file" \
        --arg tool "$tool" \
        '{timestamp: $ts, event: $event, file: $file, tool: $tool}')
      ;;

    review_triggered)
      local files="$1"
      event_json=$(jq -nc \
        --arg ts "$(timestamp)" \
        --arg event "$event_type" \
        --argjson files "$files" \
        '{timestamp: $ts, event: $event, files: $files}')
      ;;

    *)
      return 1
      ;;
  esac

  echo "$event_json" >> "$log_file"
}

has_new_files() {
  local session_id="$1"
  local log_file="/tmp/event-log-${session_id}.jsonl"

  [[ ! -f "$log_file" ]] && return 1

  local last_idx=-1
  local idx=0

  while IFS= read -r line; do
    if [[ -n "$line" ]] && echo "$line" | jq -e '.event == "review_triggered"' >/dev/null 2>&1; then
      last_idx=$idx
    fi
    ((idx++)) || true
  done < "$log_file"

  idx=0
  while IFS= read -r line; do
    if [[ $idx -gt $last_idx ]] && [[ -n "$line" ]]; then
      if echo "$line" | jq -e '.event == "file_modified"' >/dev/null 2>&1; then
        return 0
      fi
    fi
    ((idx++)) || true
  done < "$log_file"

  return 1
}

get_modified_files() {
  local session_id="$1"
  local log_file="/tmp/event-log-${session_id}.jsonl"

  [[ ! -f "$log_file" ]] && echo "[]" && return

  local last_idx=-1
  local idx=0

  while IFS= read -r line; do
    if [[ -n "$line" ]] && echo "$line" | jq -e '.event == "review_triggered"' >/dev/null 2>&1; then
      last_idx=$idx
    fi
    ((idx++)) || true
  done < "$log_file"

  local -a files=()
  idx=0
  while IFS= read -r line; do
    if [[ $idx -gt $last_idx ]] && [[ -n "$line" ]]; then
      if echo "$line" | jq -e '.event == "file_modified"' >/dev/null 2>&1; then
        local file=$(echo "$line" | jq -r '.file')
        files+=("$file")
      fi
    fi
    ((idx++)) || true
  done < "$log_file"

  printf '%s\n' "${files[@]}" | sort -u | jq -R . | jq -s .
}

get_or_initialize_plugin_settings() {
  local session_id="$1"

  local settings_file=".claude/settings.json"
  local rules_file=".claude/automatic-code-review/rules.md"

  if [[ ! -f "$settings_file" ]] || ! jq -e '.automaticCodeReview' "$settings_file" >/dev/null 2>&1; then
    local init_flag="/tmp/code-review-initialized-${session_id}"
    if [[ ! -f "$init_flag" ]]; then
      mkdir -p .claude/automatic-code-review

      local existing
      if [[ -f "$settings_file" ]]; then
        existing=$(cat "$settings_file")
      else
        existing="{}"
      fi

      echo "$existing" | jq '.automaticCodeReview = {"enabled": true, "fileExtensions": ["ts", "tsx"], "rulesFile": ".claude/automatic-code-review/rules.md"}' > "$settings_file"

      if [[ ! -f "$rules_file" ]]; then
        cp "${CLAUDE_PLUGIN_ROOT}/default-rules.md" "$rules_file" 2>/dev/null || true
      fi

      echo "✅ automatic-code-review plugin initialized!" >&2
      echo "   Updated: .claude/settings.json" >&2
      echo "   Created: .claude/automatic-code-review/rules.md (default rules)" >&2
      echo "   Customize .claude/automatic-code-review/rules.md for your project." >&2

      touch "$init_flag"
    fi
  fi

  jq -r '.automaticCodeReview' "$settings_file"
}

cmd_log() {
  INPUT=$(cat)

  TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""')
  SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""')
  FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

  [[ -z "$SESSION_ID" ]] && exit 0

  SETTINGS=$(get_or_initialize_plugin_settings "$SESSION_ID")
  ENABLED=$(echo "$SETTINGS" | jq -r '.enabled // true')

  [[ "$ENABLED" != "true" ]] && exit 0

  case "$TOOL_NAME" in
    Write|Edit|MultiEdit) ;;
    *) exit 0 ;;
  esac

  [[ -z "$FILE_PATH" ]] && exit 0

  EXTENSIONS=$(echo "$SETTINGS" | jq -r '.fileExtensions | join("|")' 2>/dev/null || echo "")
  if [[ -z "$EXTENSIONS" ]]; then
    exit 0
  fi

  FILE_MATCHES=false
  for ext in $(echo "$EXTENSIONS" | tr '|' ' '); do
    if [[ "$FILE_PATH" == *".$ext" ]]; then
      FILE_MATCHES=true
      break
    fi
  done

  [[ "$FILE_MATCHES" = false ]] && exit 0

  log_event "$SESSION_ID" file_modified "$FILE_PATH" "$TOOL_NAME" || true

  exit 0
}

cmd_review() {
  INPUT=$(cat)
  SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""')

  [[ -z "$SESSION_ID" ]] && exit 0

  SETTINGS=$(get_or_initialize_plugin_settings "$SESSION_ID")
  ENABLED=$(echo "$SETTINGS" | jq -r '.enabled // true')

  [[ "$ENABLED" != "true" ]] && exit 0

  if ! has_new_files "$SESSION_ID"; then
    exit 0
  fi

  FILES_JSON=$(get_modified_files "$SESSION_ID")
  FILE_COUNT=$(echo "$FILES_JSON" | jq 'length' 2>/dev/null || echo "0")

  if [[ "$FILE_COUNT" -eq 0 ]]; then
    exit 0
  fi

  log_event "$SESSION_ID" review_triggered "$FILES_JSON" || true

  FILES_LIST=$(echo "$FILES_JSON" | jq -r '.[] | "- " + .' 2>/dev/null || echo "")

  cat >&2 <<EOF
📋 CODE REVIEW REQUIRED

Files modified since last review:
$FILES_LIST

INSTRUCTION: Use the Task tool with subagent_type "automatic-code-reviewer". Pass only the file list as the prompt. The agent will follow its configured review procedure.

CRITICAL: After receiving review results, you MUST:
1. Show all findings to the user
2. IMMEDIATELY fix ALL violations without asking for permission
3. Treat every violation as a hard requirement - not a suggestion
4. Do NOT ask "would you like me to fix these?" - just fix them
5. After fixing, briefly confirm what was fixed

The review findings are NON-NEGOTIABLE. Fix them all, then continue.
EOF

  echo "$FILES_LIST"

  exit 2
}

case "$COMMAND" in
  log) cmd_log ;;
  review) cmd_review ;;
  *)
    echo "Error: unknown command: $COMMAND" >&2
    echo "Usage: $0 {log|review}" >&2
    exit 1
    ;;
esac
