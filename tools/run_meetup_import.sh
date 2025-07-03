#Create the virtual environment On macOS/Linux
python3.12 -m venv myenv

#Activate the virtual environment:
source myenv/bin/activate

# Install packages
pip install -r requirements.txt

python3.12 meetup_import.py