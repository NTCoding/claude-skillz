#!/bin/bash
read -r input
command=$(echo "$input" | jq -r '.tool_input.command // ""')

# Block commands that bypass safety checks
if echo "$command" | grep -qE '(--no-verify|--force|-f\s|--hard)'; then
  echo "Blocked: This command bypasses safety checks (--no-verify, --force, --hard)" >&2
  exit 2
fi

exit 0
