@echo off

echo Creating virtual environment...
python -m venv ..\.venv

echo Activating virtual environment...
call ..\.venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

setlocal
echo Enter arguments for Python script: FILE_PATH_MENTORS_XLSX FILE_PATH_MENTORS_YML MODE SKIP_ROWS
echo Example: mentors_test.xlsx mentors_test.yml a 1
echo MODE: a - to append new mentors from the xlsx table to mentors.yml
echo MODE: w - to create a new mentors.yml file with all mentors that are in the xlsx table
echo SKIP_ROWS: To start XLSX in the line 1
python automation_add_or_update_mentors.py samples/mentors.xlsx samples/mentors.yml a 1
@echo on