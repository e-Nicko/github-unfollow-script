#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_NAME=$(basename "$0")

print_usage() {
  cat <<USAGE
Usage: $SCRIPT_NAME [options]

Create or recreate a Python virtual environment and optionally install dependencies.

Options:
  -p, --python CMD          Python interpreter to use (default: auto-detect)
  -v, --venv-dir DIR        Virtualenv directory (default: venv)
  -r, --requirements FILE   Requirements file to install (default: requirements.txt if present)
      --recreate            Remove existing venv directory before creating a new one
      --no-install          Do not install any dependencies
      --no-upgrade-pip      Do not upgrade pip/setuptools/wheel
  -q, --quiet               Reduce output verbosity
  -h, --help                Show this help and exit

Examples:
  $SCRIPT_NAME
  $SCRIPT_NAME -p python3.11 -v .venv --recreate -r requirements.txt
USAGE
}

log() { if [[ "${QUIET:-false}" != "true" ]]; then echo -e "$1"; fi }
log_err() { echo -e "$1" >&2; }

on_error() {
  log_err "An error occurred while setting up the virtual environment."
}
trap on_error ERR

PYTHON_CMD=""
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
RECREATE=false
DO_INSTALL=true
UPGRADE_PIP=true
QUIET=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--python)
      [[ $# -ge 2 ]] || { log_err "Missing value for $1"; exit 1; }
      PYTHON_CMD="$2"; shift 2;;
    -v|--venv-dir)
      [[ $# -ge 2 ]] || { log_err "Missing value for $1"; exit 1; }
      VENV_DIR="$2"; shift 2;;
    -r|--requirements)
      [[ $# -ge 2 ]] || { log_err "Missing value for $1"; exit 1; }
      REQUIREMENTS_FILE="$2"; shift 2;;
    --recreate)
      RECREATE=true; shift;;
    --no-install)
      DO_INSTALL=false; shift;;
    --no-upgrade-pip)
      UPGRADE_PIP=false; shift;;
    -q|--quiet)
      QUIET=true; shift;;
    -h|--help)
      print_usage; exit 0;;
    *)
      log_err "Unknown option: $1"; print_usage; exit 1;;
  esac
done

# Resolve Python interpreter
if [[ -z "$PYTHON_CMD" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
  elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
  else
    log_err "Python interpreter not found. Please install Python 3.8+ or specify with --python."; exit 1
  fi
fi

log "Using Python: $PYTHON_CMD"
log "Virtualenv directory: $VENV_DIR"

if [[ "$RECREATE" == "true" && -d "$VENV_DIR" ]]; then
  log "Removing existing virtual environment: $VENV_DIR"
  rm -rf "$VENV_DIR"
fi

if [[ ! -d "$VENV_DIR" ]]; then
  log "Creating virtual environment..."
  "$PYTHON_CMD" -m venv "$VENV_DIR"
else
  log "Virtual environment already exists; skipping creation. Use --recreate to rebuild."
fi

# Determine the venv python path across platforms
VENV_PYTHON=""
if [[ -x "$VENV_DIR/bin/python" ]]; then
  VENV_PYTHON="$VENV_DIR/bin/python"
elif [[ -x "$VENV_DIR/Scripts/python.exe" ]]; then
  VENV_PYTHON="$VENV_DIR/Scripts/python.exe"
elif [[ -x "$VENV_DIR/Scripts/python" ]]; then
  VENV_PYTHON="$VENV_DIR/Scripts/python"
else
  log_err "Unable to locate the virtual environment's python executable in '$VENV_DIR'."; exit 1
fi

log "Venv python: $VENV_PYTHON"

if [[ "$UPGRADE_PIP" == "true" ]]; then
  log "Upgrading pip, setuptools, and wheel..."
  if [[ "$QUIET" == "true" ]]; then
    "$VENV_PYTHON" -m pip install --upgrade pip setuptools wheel >/dev/null
  else
    "$VENV_PYTHON" -m pip install --upgrade pip setuptools wheel
  fi
fi

if [[ "$DO_INSTALL" == "true" ]]; then
  if [[ -f "$REQUIREMENTS_FILE" ]]; then
    log "Installing dependencies from $REQUIREMENTS_FILE ..."
    if [[ "$QUIET" == "true" ]]; then
      "$VENV_PYTHON" -m pip install -r "$REQUIREMENTS_FILE" >/dev/null
    else
      "$VENV_PYTHON" -m pip install -r "$REQUIREMENTS_FILE"
    fi
  else
    log "No requirements file found at '$REQUIREMENTS_FILE'; skipping dependency installation."
  fi
else
  log "Dependency installation skipped (--no-install)."
fi

ACTIVATE_POSIX="source $VENV_DIR/bin/activate"
ACTIVATE_WINDOWS_PS=".\\$VENV_DIR\\Scripts\\Activate.ps1"

log "\nDone. To activate the environment:"
log "- POSIX shells: $ACTIVATE_POSIX"
log "- Windows PowerShell: $ACTIVATE_WINDOWS_PS"

exit 0