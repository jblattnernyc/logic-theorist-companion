#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  scripts/run_logic_theorist_capture.sh [options]

Options:
  --iplv-dir PATH     Path to the local IPL-V executable specimen.
                      Default: sibling IPL-V directory next to this companion repository.
  --run-id ID         Explicit run identifier. Default: YYYYMMDD_HHMMSS.
  --sbcl PATH         SBCL executable. Default: sbcl.
  --dry-run           Print the planned paths and command without creating a run bundle.
  -h, --help          Show this help.

This script runs Logic Theorist from the IPL-V specimen and preserves a
timestamped companion run bundle containing metadata, stdout, stderr, exit
status, generated artifacts, a file listing, a SHA-256 manifest, and a summary.

The script copies generated artifacts. It does not delete, move, clean, or
modify IPL-V source files.
USAGE
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || die "required command not found: $1"
}

append_cmd_output() {
  local output_file=$1
  local cwd=$2
  local label=$3
  shift 3

  {
    printf '\n## %s\n\n' "$label"
    printf 'Working directory: %s\n\n' "$cwd"
    printf 'Command:'
    printf ' %q' "$@"
    printf '\n\n'
  } >> "$output_file"

  set +e
  (
    cd "$cwd"
    "$@"
  ) >> "$output_file" 2>&1
  local status=$?
  set -e

  if [[ $status -ne 0 ]]; then
    printf '\n[exit status: %s]\n' "$status" >> "$output_file"
  fi
}

copy_newer_tree_files() {
  local source_dir=$1
  local destination_dir=$2
  local marker_file=$3
  shift 3

  [[ -d "$source_dir" ]] || return 0
  mkdir -p "$destination_dir"

  while IFS= read -r -d '' source_file; do
    local relative_path=${source_file#"$source_dir"/}
    local destination_file="$destination_dir/$relative_path"
    mkdir -p "$(dirname "$destination_file")"
    cp -p "$source_file" "$destination_file"
  done < <(find "$source_dir" -type f "$@" -newer "$marker_file" -print0)
}

copy_newer_file_glob() {
  local destination_dir=$1
  local marker_file=$2
  shift 2

  mkdir -p "$destination_dir"

  local source_file
  for source_file in "$@"; do
    [[ -e "$source_file" ]] || continue
    [[ -f "$source_file" ]] || continue
    if [[ "$source_file" -nt "$marker_file" ]]; then
      cp -p "$source_file" "$destination_dir/"
    fi
  done
}

write_manifest() {
  local run_dir=$1
  local manifest_file="$run_dir/manifest.sha256"

  (
    cd "$run_dir"
    find . -type f ! -name 'manifest.sha256' | LC_ALL=C sort | while IFS= read -r file; do
      shasum -a 256 "$file"
    done
  ) > "$manifest_file"
}

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
COMPANION_DIR=$(cd -- "$SCRIPT_DIR/.." && pwd -P)
WORKSPACE_DIR=$(cd -- "$COMPANION_DIR/.." && pwd -P)

IPLV_DIR=${IPLV_DIR:-"$WORKSPACE_DIR/IPL-V"}
RUN_ID=${RUN_ID:-"$(date +%Y%m%d_%H%M%S)"}
SBCL_BIN=${SBCL_BIN:-sbcl}
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --iplv-dir)
      [[ $# -ge 2 ]] || die "--iplv-dir requires a path"
      IPLV_DIR=$2
      shift 2
      ;;
    --run-id)
      [[ $# -ge 2 ]] || die "--run-id requires an identifier"
      RUN_ID=$2
      shift 2
      ;;
    --sbcl)
      [[ $# -ge 2 ]] || die "--sbcl requires an executable path"
      SBCL_BIN=$2
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown argument: $1"
      ;;
  esac
done

[[ "$RUN_ID" =~ ^[A-Za-z0-9._-]+$ ]] || die "run id contains unsupported characters: $RUN_ID"

IPLV_DIR=$(cd -- "$IPLV_DIR" && pwd -P)
RUN_DIR="$COMPANION_DIR/runs/$RUN_ID"
ARTIFACT_DIR="$RUN_DIR/generated_artifacts"
MARKER_FILE="$RUN_DIR/run_start.marker"

LT_COMMAND=(
  "$SBCL_BIN"
  --dynamic-space-size 4096
  --eval '(load (compile-file "lt.lisp"))'
  --eval '(sb-ext:exit)'
)

require_command git
require_command find
require_command shasum
require_command uname
require_command date
require_command cp
require_command mkdir
require_command "$SBCL_BIN"

[[ -d "$COMPANION_DIR/.git" ]] || die "companion repository is not a Git repository: $COMPANION_DIR"
[[ -d "$IPLV_DIR/.git" ]] || die "IPL-V directory is not a Git repository: $IPLV_DIR"
[[ -f "$IPLV_DIR/lt.lisp" ]] || die "lt.lisp not found in IPL-V directory: $IPLV_DIR"

if [[ $DRY_RUN -eq 1 ]]; then
  printf 'Companion repository: %s\n' "$COMPANION_DIR"
  printf 'IPL-V specimen:       %s\n' "$IPLV_DIR"
  printf 'Run ID:               %s\n' "$RUN_ID"
  printf 'Run directory:        %s\n' "$RUN_DIR"
  printf 'Command:'
  printf ' %q' "${LT_COMMAND[@]}"
  printf '\n'
  exit 0
fi

[[ ! -e "$RUN_DIR" ]] || die "run directory already exists: $RUN_DIR"

mkdir -p "$ARTIFACT_DIR"
touch "$MARKER_FILE"

METADATA_FILE="$RUN_DIR/metadata.txt"
POST_METADATA_FILE="$RUN_DIR/post_run_metadata.txt"
STDOUT_FILE="$RUN_DIR/stdout.txt"
STDERR_FILE="$RUN_DIR/stderr.txt"
EXIT_STATUS_FILE="$RUN_DIR/exit_status.txt"
ARTIFACT_LISTING_FILE="$RUN_DIR/generated_artifacts_listing.txt"
SUMMARY_FILE="$RUN_DIR/summary.md"

{
  printf '# Logic Theorist Run Metadata\n\n'
  printf 'Run ID: %s\n' "$RUN_ID"
  printf 'Companion repository: %s\n' "$COMPANION_DIR"
  printf 'IPL-V specimen: %s\n' "$IPLV_DIR"
  printf 'Run directory: %s\n' "$RUN_DIR"
  printf 'Start date: %s\n' "$(date)"
  printf 'Command:'
  printf ' %q' "${LT_COMMAND[@]}"
  printf '\n'
} > "$METADATA_FILE"

append_cmd_output "$METADATA_FILE" "$IPLV_DIR" "pwd" pwd
append_cmd_output "$METADATA_FILE" "$IPLV_DIR" "git rev-parse HEAD" git rev-parse HEAD
append_cmd_output "$METADATA_FILE" "$IPLV_DIR" "git branch --show-current" git branch --show-current
append_cmd_output "$METADATA_FILE" "$IPLV_DIR" "git remote -v" git remote -v
append_cmd_output "$METADATA_FILE" "$IPLV_DIR" "git status --short" git status --short
append_cmd_output "$METADATA_FILE" "$IPLV_DIR" "git diff --stat" git diff --stat
append_cmd_output "$METADATA_FILE" "$IPLV_DIR" "git log -1 --oneline" git log -1 --oneline
append_cmd_output "$METADATA_FILE" "$IPLV_DIR" "sbcl --version" "$SBCL_BIN" --version
append_cmd_output "$METADATA_FILE" "$IPLV_DIR" "uname -a" uname -a
append_cmd_output "$METADATA_FILE" "$IPLV_DIR" "date" date
append_cmd_output "$METADATA_FILE" "$COMPANION_DIR" "companion git rev-parse HEAD" git rev-parse HEAD
append_cmd_output "$METADATA_FILE" "$COMPANION_DIR" "companion git status --short --untracked-files=no" git status --short --untracked-files=no

set +e
(
  cd "$IPLV_DIR"
  "${LT_COMMAND[@]}"
) > "$STDOUT_FILE" 2> "$STDERR_FILE"
RUN_STATUS=$?
set -e

printf '%s\n' "$RUN_STATUS" > "$EXIT_STATUS_FILE"

copy_newer_tree_files \
  "$IPLV_DIR/ltresults" \
  "$ARTIFACT_DIR/ltresults" \
  "$MARKER_FILE" \
  \( -name '*.log' -o -name '*.dotstar' \)

copy_newer_file_glob "$ARTIFACT_DIR/iplv-root" "$MARKER_FILE" "$IPLV_DIR"/*.fasl "$IPLV_DIR"/proof-*.pdf
copy_newer_file_glob "$ARTIFACT_DIR/tmp" "$MARKER_FILE" /tmp/lt-proof-*.dot

{
  printf '# Post-Run Metadata\n\n'
  printf 'End date: %s\n' "$(date)"
  printf 'Exit status: %s\n' "$RUN_STATUS"
} > "$POST_METADATA_FILE"

append_cmd_output "$POST_METADATA_FILE" "$IPLV_DIR" "post-run git status --short" git status --short
append_cmd_output "$POST_METADATA_FILE" "$IPLV_DIR" "post-run git diff --stat" git diff --stat
append_cmd_output "$POST_METADATA_FILE" "$IPLV_DIR" "post-run date" date

(
  cd "$ARTIFACT_DIR"
  find . -type f | LC_ALL=C sort
) > "$ARTIFACT_LISTING_FILE"

ARTIFACT_COUNT=$(wc -l < "$ARTIFACT_LISTING_FILE" | tr -d ' ')

{
  printf '# Logic Theorist Run Summary\n\n'
  printf '- Run ID: `%s`\n' "$RUN_ID"
  printf '- IPL-V path: `%s`\n' "$IPLV_DIR"
  printf '- Companion run directory: `%s`\n' "$RUN_DIR"
  printf '- Exit status: `%s`\n' "$RUN_STATUS"
  printf '- Generated artifact count copied: `%s`\n' "$ARTIFACT_COUNT"
  printf '\n'
  printf 'This run summary records local executable behavior only. It is not a historical claim and should be interpreted with the accompanying metadata, stdout, stderr, generated artifacts, and manifest.\n'
} > "$SUMMARY_FILE"

write_manifest "$RUN_DIR"

printf 'Logic Theorist run bundle created: %s\n' "$RUN_DIR"
printf 'Exit status: %s\n' "$RUN_STATUS"

exit "$RUN_STATUS"
