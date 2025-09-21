#Create the virtual environment On macOS/Linux
python3 -m venv myenv

#Activate the virtual environment:
source myenv/bin/activate

# Install packages
pip install -r requirements.txt

# Enter the parameters: IMAGE_URL MENTOR_NAME
python3 download_image.py "Mentor Name" "image_url_here"