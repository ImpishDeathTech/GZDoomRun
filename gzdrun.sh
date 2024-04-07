#! /usr/bin/bash
VENV="${HOME}"/.venv

if [ $(python3 -m gzdoomrun is-venv) = false ]
then
    source "${VENV}/bin/activate"
fi

python3 -m gzdoomrun $@