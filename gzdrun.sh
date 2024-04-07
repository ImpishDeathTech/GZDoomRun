#! /usr/bin/bash
VENV="${HOME}"/.venv

if [ $(python3 - gzdoomrun venv?) = false ]
then
    source "${VENV}/bin/activate"
fi

python3 -m gzdoomrun $@