#Create the virtual environment On macOS/Linux
python3 -m venv myenv

#Activate the virtual environment:
source myenv/bin/activate

# Install packages
pip install -r requirements.txt

# Enter the parameters: FILE_PATH_MENTORS_XLSX FILE_PATH_MENTORS_YML CURRENT_PERIOD MODE SKIP_ROWS
# Example: samples/mentors.xlsx samples/mentors.yml default a 0
# mode "a" for APPEND new mentors from the xlsx table to the existing mentors.yml
# mode "w" for WRITE all mentors from the xlsx table to mentors.yml
# CURRENT_PERIOD: default or long-term (use long-term if currently during long-term registration period)
python3 automation_add_or_update_mentors.py samples/mentors.xlsx ../_data/mentors.yml default a 0