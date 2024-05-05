@echo off

echo Creating virtual environment...
python -m venv ..\.venv

echo Activating virtual environment...
CALL ..\.venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Setup complete.