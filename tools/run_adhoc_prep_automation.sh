#Create the virtual environment On macOS/Linux
python3 -m venv myenv

#Activate the virtual environment:
source myenv/bin/activate

# Install packages
pip install -r requirements.txt

# Enter the parameters: FILE_PATH_XLSX MONTH
# Example: samples/adhoc-prep.xlsx 9
# month: the adhoc month in number e.g 4 -> April, 11 -> November
python3 automation_prepare_adhoc_availability.py samples/adhoc-prep.xlsx 10
