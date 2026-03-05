#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

SOURCE_DIR="${ROOT_DIR}/skills"
TARGET_DIRS=(
  "${ROOT_DIR}/.codex/skills"
  "${ROOT_DIR}/.copilot/skills"
)

if [ ! -d "${SOURCE_DIR}" ]; then
  echo "source skills directory not found: ${SOURCE_DIR}" >&2
  exit 1
fi

if [ "${DRY_RUN:-0}" = "1" ]; then
  echo "DRY_RUN=1 enabled. No files will be written."
fi

sync_one_target() {
  local target_dir="$1"
  mkdir -p "${target_dir}"

  local source_skill
  for source_skill in "${SOURCE_DIR}"/*; do
    [ -d "${source_skill}" ] || continue

    local skill_name
    skill_name="$(basename "${source_skill}")"
    local target_skill="${target_dir}/${skill_name}"

    echo "install ${skill_name} -> ${target_dir}"

    if [ "${DRY_RUN:-0}" = "1" ]; then
      continue
    fi

    if command -v rsync >/dev/null 2>&1; then
      mkdir -p "${target_skill}"
      rsync -a --delete "${source_skill}/" "${target_skill}/"
    else
      rm -rf "${target_skill}"
      cp -R "${source_skill}" "${target_skill}"
    fi
  done
}

for target_dir in "${TARGET_DIRS[@]}"; do
  sync_one_target "${target_dir}"
done

echo "skill installation complete."
