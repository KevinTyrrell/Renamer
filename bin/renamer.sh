#!/bin/bash
# https://stackoverflow.com/a/4774063
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
python "${SCRIPTPATH}/../renamer/renamer.py" "$@"