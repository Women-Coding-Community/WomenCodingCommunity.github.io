#Create the virtual environment On macOS/Linux
python3 -m venv myenv

#Activate the virtual environment:
source myenv/bin/activate

# Install packages
pip install -r requirements.txt

# Enter the parameters: FILE_PATH_MENTORS_XLSX FILE_PATH_MENTORS_YML MODE SKIP_ROWS
# Example: samples/mentors.xlsx samples/mentors.yml a
# mode "a" for APPEND new mentors from the xlsx table to the existing mentors.yml
# mode "w" for WRITE all mentors from the xlsx table to mentors.yml
python3 meetup_import.py "https://www.meetup.com/women-coding-community/events/?type=upcoming" "../_data/events1.yml" a