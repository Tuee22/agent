#!/usr/bin/env bash
# ------------------------------------------------------------------
# dev.sh – convenience launcher for the *agent* project
# ------------------------------------------------------------------
set -euo pipefail

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DC_FILE="$THIS_DIR/docker/docker-compose.yaml"

command_exists() { command -v "$1" >/dev/null 2>&1; }

die() { echo "❌  $*" >&2; exit 1; }

check_prereqs() {
  command_exists docker || die "Docker is not installed or not in PATH."
  if command_exists docker-compose; then
    DC="docker-compose"
  elif docker compose version >/dev/null 2>&1; then
    DC="docker compose"
  else
    die "Docker Compose plugin not available."
  fi
}

usage() {
cat <<'USAGE'
dev.sh – handy tasks for the *agent* repo

USAGE:
  ./dev.sh build        Build (or rebuild) the dev container
  ./dev.sh shell        Drop into an interactive shell (with live code mount)
  ./dev.sh publish SRC  Build & install a wheel from local source into the
                        running container, upgrading the pinned 'agent' inside.
                        Typically: ./dev.sh publish .

  ./dev.sh help         This help message
USAGE
}

build()   { $DC -f "$DC_FILE" build; }
shell()   { $DC -f "$DC_FILE" run --rm agent-dev; }
publish() {
  local SRC=${1:-.}
  $DC -f "$DC_FILE" run --rm agent-dev bash -c "
    cd /workspace &&
    poetry version patch &&
    poetry build -f wheel &&
    pip install --upgrade --no-cache-dir dist/agent-*.whl
  "
  echo "✅  agent upgraded inside container."
}

main() {
  check_prereqs
  case "${1-}" in
    build)   build   ;;
    shell)   shell   ;;
    publish) publish "${2:-.}" ;;
    help|"") usage ;;
    *) die "Unknown command: $1 (see './dev.sh help')" ;;
  esac
}

main "$@"
