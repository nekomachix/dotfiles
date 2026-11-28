#!/usr/bin/env bash
# Planning only: never executes the printed installation command.
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec python3 "$root/scripts/dotctl" plan "$@"
