#! /bin/bash
set -e

playbook=$(
python - ${1} <<EOF
import sys
path = sys.argv[1]
mod = path.replace('/', '.').strip().strip('.').removesuffix('.py')
print(mod)
EOF
)

python -m ${playbook} "${@:2}"
