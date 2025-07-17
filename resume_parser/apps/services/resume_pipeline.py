# resume_parser/apps/services/resume_pipeline.py

from typing import Dict, Any
from resume_parser.apps.models.text_extractor import extract_text
from resume_parser.apps.models.cleaner import clean_resume_text
from resume_parser.apps.models.extractor import extract_section, extract_basic_fields
from resume_parser.apps.models.trie_keyword_extractor import build_trie_from_skill_list, extract_tech_keywords
from resume_parser.apps.models.fuzzy_keyword_matcher import fuzzy_keyword_match
from resume_parser.apps.services.constants import TECH_KEYWORDS

# Build Trie once on module load
trie = build_trie_from_skill_list(TECH_KEYWORDS)

def parse_resume_file(file_path: str) -> Dict[str, Any]:
    # 1. Extract and clean text
    raw_text = extract_text(file_path)
    cleaned_text = clean_resume_text(raw_text)

    # 2. Extract sections
    sections = {
        "experience": extract_section(cleaned_text, "EXPERIENCE") or "",
        "projects": extract_section(cleaned_text, "PROJECTS") or "",
        "skills": extract_section(cleaned_text, "SKILLS") or "",
        "certifications": extract_section(cleaned_text, "CERTIFICATIONS") or "",
        "education": extract_section(cleaned_text, "EDUCATION") or "",
    }

    # 3. Extract basic info
    basic_info = extract_basic_fields(cleaned_text)

    # 4. Combine relevant sections
    combined_text = " ".join([
        sections["experience"],
        sections["projects"],
        sections["skills"],
        sections["certifications"],
    ]).lower()

    # 5. Step 1: Extract exact matches using Trie
    exact_matches = set(extract_tech_keywords(combined_text, trie))

    # 6. Step 2: Extract fuzzy matches on leftover text tokens
    # Remove exact matches tokens from combined_text tokens to avoid duplicates
    tokens = set(combined_text.split())
    exact_tokens = set()
    for phrase in exact_matches:
        exact_tokens.update(phrase.split())
    leftover_tokens_text = ' '.join([t for t in tokens if t not in exact_tokens])

    fuzzy_matches = set(fuzzy_keyword_match(leftover_tokens_text, TECH_KEYWORDS))

    # Combine exact and fuzzy matches
    all_skills = sorted(exact_matches.union(fuzzy_matches))


    # 8. Return full structured data
    return {
        "profile": {
            "name": basic_info.get("name"),
            "email": basic_info.get("email"),
            "phone": basic_info.get("phone"),
            "linkedin": basic_info.get("linkedin"),
            "github": basic_info.get("github"),
        },
        "sections": sections,
        "extracted_skills": all_skills,
        "raw_text": cleaned_text
    }
