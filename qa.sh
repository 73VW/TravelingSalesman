#!/bin/sh

pycodestyle . > result.log
pydocstyle . >> result.log
isort --recursive . >> result.log
flake8 . >> result.log
