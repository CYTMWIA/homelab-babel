#! /bin/bash
set -e

playbook=${1%.*}
playbook=${playbook//\//\.}
python -m ${playbook} "${@:2}"
