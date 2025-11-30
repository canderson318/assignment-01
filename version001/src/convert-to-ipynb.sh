#!/usr/bin/env bash

cd /Users/canderson/Documents/school/CPBS7602-class/assignment-01/version001/src

shopt -s nullglob
for file in ./*.py; do
    jupytext "$file" --to notebook
done