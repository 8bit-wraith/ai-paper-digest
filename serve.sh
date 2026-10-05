#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec "${AI_PAPER_PYTHON:-$ROOT/.venv-viewer/bin/python}" "$ROOT/flask_server.py"
