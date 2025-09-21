@echo off

echo Creating virtual environment...
python -m venv ..\.venv

echo Activating virtual environment...
call ..\.venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

setlocal
echo Enter arguments for Python script: FILE_PATH_MENTORS_XLSX FILE_PATH_MENTORS_YML CURRENT_PERIOD MODE SKIP_ROWS
echo Example: mentors_test.xlsx mentors_test.yml default a 1
echo CURRENT_PERIOD: use 'default' or 'long-term' ('long-term' if during long-term registration period)
echo MODE: a - to append new mentors from the xlsx table to mentors.yml
echo MODE: w - to create a new mentors.yml file with all mentors that are in the xlsx table
echo SKIP_ROWS: To start XLSX in the line 1
python automation_mentors.py samples/mentors.xlsx samples/mentors.yml default a 1
@echo on