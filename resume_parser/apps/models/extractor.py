#resume_parser.api.models.extractor.py

import re

def extract_basic_fields(text):
    cleaned = text.replace('\r', '').replace('\t', '').replace('|', ' ')
    name = extract_name(cleaned)

    email = re.findall(r"[\w\.-]+@[\w\.-]+", cleaned)
    phone = re.findall(r"\+?\d[\d \-\(\)]{8,14}\d", cleaned)
    linkedin = re.findall(r"https?://[^\s]*linkedin\.com[^\s]*", cleaned)
    github = re.findall(r"https?://[^\s]*github\.com[^\s]*", cleaned)

    return {
        "name": name,
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None,
        "linkedin": linkedin[0] if linkedin else None,
        "github": github[0] if github else None
    }



def extract_section(text, section):
    pattern = rf"{section}\s*(.*?)(?=(EXPERIENCE|PROJECTS|EDUCATION|SKILLS|CERTIFICATIONS|TRAINING|REFERENCES|AWARDS|$))"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None




def extract_name(text):
    lines = text.split('\n')[:15]

    for line in lines:
        line = line.strip()

        # === STEP 1: Handle spaced-out OCR name like 'A s h o k   L a m s a l' ===
        if re.fullmatch(r'([A-Za-z]\s*){4,}', line):
            # Collapse spaces between characters and try again
            collapsed = ''.join(line.split())
            name_parts = re.findall(r'[A-Z][a-z]{1,}', collapsed)
            if 2 <= len(name_parts) <= 4:
                return ' '.join(name_parts)

        # === STEP 2: Normal full name like 'Ashok Lamsal' ===
        match = re.match(r'^([A-Z][a-z]+)\s+([A-Z][a-z]+)', line)
        if match:
            return match.group().strip()

    # === STEP 3: Fallback — Use first non-empty 2–4 word line ===
    for line in lines:
        words = line.strip().split()
        if 2 <= len(words) <= 4 and all(w.isalpha() for w in words):
            return ' '.join(words)

    return None
