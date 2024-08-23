#Create the virtual environment On macOS/Linux
python3 -m venv myenv

#Activate the virtual environment:
source myenv/bin/activate

# Install packages
pip install -r requirements.txt

# Enter the parameters: IMAGE_URL MENTOR_NAME
python3 download_image.py "https://media.licdn.com/dms/image/v2/D4E03AQFLzC76FGXhiQ/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1711114395505?e=1729728000&v=beta&t=P3FN1bSt0aMtt42YyJfiZCRxSqOPllf8U7O9jr2Ki_U" "Samuela Smolorz"