#resume_parser.apps.models.sill.py
import json
import re

from cloudpathlib.local.localclient import clean_temp_dirs

from resume_parser.apps.models.cleaner import clean_resume_text
# Convert to list first

user_skills = clean_resume_text()
user_skills_list = user_skills.tolist()

# Now save as JSON
with open('user_skills.json', 'w') as f:
    json.dump(user_skills_list, f)

# Load the list from JSON
with open('user_skills.json', 'r') as f:
    data = json.load(f)  # data is a list with one string

raw_string = data[0]  # Extract the string

# Split by common delimiters like ',', ':', '(', ')', etc.
tokens = re.split(r'[,:()\-\.\s]+', raw_string)

# Clean up: remove short/incomplete/broken words and trim spaces
cleaned_skills = [token.strip() for token in tokens if len(token.strip()) > 2]

# Optional: remove duplicates
unique_skills = list(set(cleaned_skills))

# Show result
print(unique_skills)

# Optionally save to a new file
with open('cleaned_user_skills.json', 'w') as f:
    json.dump(unique_skills, f)