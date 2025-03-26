import pandas as pd
import os
import re
import copy  # Import copy module for deep copying

# Load the mentee registration data
file_path = "Mentorship Programme long-term Registration Form for Mentees (Responses).xlsx"
sheet_name = "Revised Mentees"
df = pd.read_excel(file_path, sheet_name=sheet_name)  # Read the specified sheet from the Excel file

# Define the relevant columns based on the example file
columns_to_keep = [
    "Mentee Id", "What is your full name?", "What is your email address?",
    "Slack Name\nPlease note your application will be rejected if you are not in our Slack community.\nClick here to join us on Slack.",
    "Where are you based? (Country and/or city)", "What is your current job title / education status?",
    "Company / University name", "Your LinkedIn Profile", "How many years of experience do you have in the tech industry?",
    "What tech skill you are most interested in? Mark your preference from 1 to 5 (1 - lowest, 5 - highest) [5]",
    "What tech skill you are most interested in? Mark your preference from 1 to 5 (1 - lowest, 5 - highest) [4]",
    "What tech skill you are most interested in? Mark your preference from 1 to 5 (1 - lowest, 5 - highest) [3]",
    "What tech skill you are most interested in? Mark your preference from 1 to 5 (1 - lowest, 5 - highest) [2]",
    "What tech skill you are most interested in? Mark your preference from 1 to 5 (1 - lowest, 5 - highest) [1]",
    "What is your preferred programming language? Mark your preference from 1 to 5 (1 - lowest, 5 - highest) [5]",
    "What is your preferred programming language? Mark your preference from 1 to 5 (1 - lowest, 5 - highest) [4]",
    "What is your preferred programming language? Mark your preference from 1 to 5 (1 - lowest, 5 - highest) [3]",
    "What is your preferred programming language? Mark your preference from 1 to 5 (1 - lowest, 5 - highest) [2]",
    "What is your preferred programming language? Mark your preference from 1 to 5 (1 - lowest, 5 - highest) [1]",
    "Please share your goals and expectations for this mentorship programme",
    "Did you participate in the previous mentorship cycle in 2024?",
    "Please describe how much experience you have in the area you would like to be mentored in. \n\nIf you are studying, tell us about your accomplished courses, projects, achievements, or interests",
    "How many hours per week would you be able to dedicate to mentoring? (on average)",
    "Why do you believe these mentor(s) can help you achieve your goals this year?\n\nPlease include which aspects of the mentor’s profile interest you the most and how they align with the skills the mentor offers and the ones you are also interested in developing."
]

# Ensure output directory exists
output_dir = "Long Term Mentors"
os.makedirs(output_dir, exist_ok=True)  # Create folder if it does not exist

# Process mentor selections
mentor_column = "Which is the mentor's name would you like to be matched with?\nMake sure the name of the mentor is in WCC active mentors here.\n(Note: you can indicate interest for up to five mentors) in the respective priority you would like to be matched\n1. Full Name\n2. Full Name\n3. Full Name\n4. Full Name\n5. Full Name"
mentor_dict = {}  # Dictionary to store mentees grouped by mentor

for _, row in df.iterrows():  # Iterate through each row in the DataFrame
    mentee_data = row[columns_to_keep].to_dict()  # Extract mentee's details as a dictionary
    if pd.notna(row[mentor_column]):  # Check if the mentor column is not empty
        mentor_entries = re.split(r"\n|\d+[.-]\s*", str(row[mentor_column]))  # Split multiple mentor entries into a list
        mentors = []
        reasons = {}  # Dictionary to store mentor-specific reasons
        
        for entry in mentor_entries:
            entry = entry.strip()  # Remove extra spaces
            if not entry:
                continue
            
            # Extract mentor name and reason (if any)
            match = re.match(r"^([^\-\n]+)\s*-?\s*(.*)$", entry)
            if match:
                mentor_name = match.group(1).strip()
                entry_reason = match.group(2).strip()
                mentors.append(mentor_name)
                reasons[mentor_name] = entry_reason if entry_reason else ""
            else:
                mentors.append(entry)
                reasons[entry] = ""
        
        for mentor_name in mentors:
            mentee_copy = copy.deepcopy(mentee_data)  # Create a separate copy for each mentor
            mentee_copy["Why do you believe these mentor(s) can help you achieve your goals this year?\n\nPlease include which aspects of the mentor’s profile interest you the most and how they align with the skills the mentor offers and the ones you are also interested in developing."] = reasons[mentor_name]
            
            if mentor_name not in mentor_dict:
                mentor_dict[mentor_name] = []  # Create a new list for the mentor if not already present
            mentor_dict[mentor_name].append(mentee_copy)  # Add mentee's details to the mentor's list

# Save each mentor's mentee list as an Excel file
for mentor, mentees in mentor_dict.items():  # Loop through each mentor
    mentor_df = pd.DataFrame(mentees)  # Create a DataFrame for the mentor's mentees
    mentor_filename = os.path.join(output_dir, f"WCC - Long Term - {mentor}.xlsx")  # Define file name
    mentor_df.to_excel(mentor_filename, index=False)  # Save to an Excel file

print("Files created successfully in 'Mentor_Files' folder.")  # Confirmation message