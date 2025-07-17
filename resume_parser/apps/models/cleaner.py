#resume_parser.apps.models.cleaner.py
import re

def clean_resume_text(text):
    text = re.sub(r'\s+', ' ', text)
    headers = ['EXPERIENCE', 'PROJECTS', 'EDUCATION', 'SKILLS', 'CERTIFICATIONS', 'TRAINING', 'REFERENCES']
    for h in headers:
        broken = r'\s*'.join(h)
        text = re.sub(broken, h, text, flags=re.IGNORECASE)
    return re.sub(
        r'(?i)(Experience|Projects|Education|Skills|Certifications|Training|References)',
        lambda m: m.group().upper(),
        text
    )
