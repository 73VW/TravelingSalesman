#!/bin/sh

pip install flake8 isort pycodestyle pydocstyle
pycodestyle . > result.log
pydocstyle . >> result.log
isort --recursive . >> result.log
flake8 . >> result.log
