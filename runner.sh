#!/bin/bash

# cd to the directory of this file
cd "$(dirname "$0")" || exit
# shellcheck source=venv/bin/activate
. venv/bin/activate
python bot.py
