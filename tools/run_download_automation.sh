#Create the virtual environment On macOS/Linux
python3 -m venv myenv

#Activate the virtual environment:
source myenv/bin/activate

# Install packages
pip install -r requirements.txt

# Enter the parameters: XLSX_FILE_PATH
# Example: samples/mentors.xlsx (should contain two sheets: "WCC All Approved Mentors" and "Mentors Images")
python3 download_image.py samples/mentors.xlsx