#! /usr/bin/bash
VENV="${HOME}"/.venv

python3 -m gzdoomrun is-venv

if [ $? -eq 1 ]
then
    source "${VENV}/bin/activate"
fi

python3 -m gzdoomrun $@