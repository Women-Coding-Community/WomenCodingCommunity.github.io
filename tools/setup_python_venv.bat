@echo off

echo Creating virtual environment...
python -m venv ..\.venv

echo Activating virtual environment...
CALL ..\.venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Setup complete.

setlocal
echo Enter arguments for Python script: FILE_PATH_MENTORS_XLSX FILE_PATH_MENTORS_YML MODE SKIP_ROWS
echo Example: mentors_test.xlsx mentors_test.yml a 0
echo MODE: a - to append new mentors from the xlsx table to mentors.yml
echo MODE: w - to create a new mentors.yml file with all mentors that are in the xlsx table
call ..\.venv\Scripts\activate

set /p args=Enter arguments for Python script:
python automation.py %args%

if %ERRORLEVEL% neq 0 (
    echo Invalid arguments provided.
    echo Please check the usage and try again.
)
call deactivate
set args=
endlocal
@echo on