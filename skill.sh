#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="reader-aware-writing"
SKILL_DIR="${SCRIPT_DIR}/skills/${SKILL_NAME}"

usage() {
  cat <<'EOF'
Usage:
  ./skill.sh install codex
  ./skill.sh install claude
  ./skill.sh install all
  ./skill.sh path
  ./skill.sh validate

Examples:
  ./skill.sh install codex
  ./skill.sh install claude
  ./skill.sh install all
EOF
}

ensure_skill_dir() {
  if [[ ! -f "${SKILL_DIR}/SKILL.md" ]]; then
    echo "Skill directory not found: ${SKILL_DIR}" >&2
    exit 1
  fi
}

install_skill() {
  local target="$1"
  local dest_dir

  case "${target}" in
    codex)
      dest_dir="${CODEX_HOME:-${HOME}/.codex}/skills"
      ;;
    claude)
      dest_dir="${HOME}/.claude/skills"
      ;;
    *)
      echo "Unknown install target: ${target}" >&2
      usage
      exit 1
      ;;
  esac

  mkdir -p "${dest_dir}"
  rm -rf "${dest_dir}/${SKILL_NAME}"
  cp -R "${SKILL_DIR}" "${dest_dir}/"
  echo "Installed ${SKILL_NAME} to ${dest_dir}/${SKILL_NAME}"
}

validate_skill() {
  ensure_skill_dir

  if [[ ! -r "${SKILL_DIR}/SKILL.md" ]]; then
    echo "Cannot read ${SKILL_DIR}/SKILL.md" >&2
    exit 1
  fi

  if ! grep -q '^name: reader-aware-writing$' "${SKILL_DIR}/SKILL.md"; then
    echo "Missing or incorrect skill name in SKILL.md" >&2
    exit 1
  fi

  if ! grep -q '^description: ' "${SKILL_DIR}/SKILL.md"; then
    echo "Missing skill description in SKILL.md" >&2
    exit 1
  fi

  echo "Skill metadata looks valid: ${SKILL_DIR}"
}

main() {
  ensure_skill_dir

  local cmd="${1:-}"
  case "${cmd}" in
    install)
      local target="${2:-}"
      case "${target}" in
        codex|claude)
          install_skill "${target}"
          ;;
        all)
          install_skill codex
          install_skill claude
          ;;
        *)
          usage
          exit 1
          ;;
      esac
      ;;
    path)
      echo "${SKILL_DIR}"
      ;;
    validate)
      validate_skill
      ;;
    ""|-h|--help|help)
      usage
      ;;
    *)
      echo "Unknown command: ${cmd}" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
