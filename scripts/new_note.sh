#!/usr/bin/env bash
#
# new_note.sh — Create a new note from template with auto-generated frontmatter
#
# Usage:
#   ./scripts/new_note.sh <phase> <kind> "<Title>"
#
# Arguments:
#   phase   Phase directory (e.g., 01_foundations, 03_deep_learning)
#   kind    Note type: notes | exercises | proofs | projects
#   title   Note title in quotes (will be kebab-cased for the filename)
#
# Examples:
#   ./scripts/new_note.sh 03_deep_learning notes "Backpropagation Intuition"
#   ./scripts/new_note.sh 05_llm_engineering exercises "LoRA Fine-tuning"
#
# Cross-platform: works on Linux, macOS, and Windows (Git Bash / WSL).

set -euo pipefail

# --- Configuration ---
TEMPLATES_DIR="$(cd "$(dirname "$0")/../templates" && pwd)"
PHASE="$1"
KIND="$2"
TITLE="$3"

# --- Validation ---
if [ $# -lt 3 ]; then
    echo "Usage: $0 <phase> <kind> \"<Title>\""
    echo "  phase: 01_foundations | 02_classical_ml | 03_deep_learning |"
    echo "         04_nlp_and_transformers | 05_llm_engineering | 06_production_ai | 07_capstone"
    echo "  kind:  notes | exercises | proofs | projects"
    exit 1
fi

# Map kind to template file
case "$KIND" in
    notes)     TPL="note.md" ;;
    exercises) TPL="exercise.md" ;;
    proofs)    TPL="proof.md" ;;
    projects)  TPL="project.md" ;;
    *)
        echo "Error: unknown kind '$KIND'. Use: notes, exercises, proofs, or projects."
        exit 1
        ;;
esac

# --- Generate filename from title (kebab-case, cross-platform) ---
# Lowercase, replace spaces/special chars with hyphens, strip leading/trailing hyphens
FILENAME="$(echo "$TITLE" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -e 's/[^a-z0-9]/-/g' -e 's/--*/-/g' -e 's/^-//' -e 's/-$//')"
DEST="${PHASE}/${KIND}/${FILENAME}.md"

# --- Check if template exists ---
if [ ! -f "${TEMPLATES_DIR}/${TPL}" ]; then
    echo "Error: template '${TEMPLATES_DIR}/${TPL}' not found."
    exit 1
fi

# --- Check if destination already exists ---
if [ -f "$DEST" ]; then
    echo "Error: $DEST already exists."
    exit 1
fi

# --- Get current date (ISO 8601, works on Linux, macOS, BSD) ---
DATE=$(date -u +%Y-%m-%d)

# --- Extract phase number from directory name ---
PHASE_NUM=$(echo "$PHASE" | sed 's/^0*//' | cut -d'_' -f1)

# --- Create the note from template ---
# Use sed to substitute placeholders (works with both GNU and BSD sed)
if sed --version >/dev/null 2>&1; then
    # GNU sed
    sed "s/{{title}}/$TITLE/g; s/{{date}}/$DATE/g" "${TEMPLATES_DIR}/${TPL}" > "$DEST"
else
    # BSD sed (macOS)
    sed -e "s/{{title}}/$TITLE/g" -e "s/{{date}}/$DATE/g" "${TEMPLATES_DIR}/${TPL}" > "$DEST"
fi

echo "Created: $DEST"

# --- Suggest wikilink to paste ---
echo ""
echo "Add this link where needed:"
echo "  [[${PHASE}/${KIND}/${FILENAME}|${TITLE}]]"
