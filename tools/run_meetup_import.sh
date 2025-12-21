# Check we are in the tools directory else exit with warning message
if [ "$(basename "$PWD")" != "tools" ]; then
    echo "Please run this script from the repository's tools/ directory."
    exit 1
fi

#Create the virtual environment On macOS/Linux if it doesn't exist:
if [ ! -d "myenv" ]; then
    python3.12 -m venv myenv
fi

#Activate the virtual environment:
source myenv/bin/activate

# Install packages
pip install -r requirements.txt

python3.12 download_meetup_ics.py

python3.12 meetup_import.py