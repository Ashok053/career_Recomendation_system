# resume_parser/apps/models/fuzzy_keyword_matcher.py

import re
from thefuzz import fuzz

def fuzzy_keyword_match(text: str, keywords: list, threshold: int = 85):
    # Extract tokens from text, remove very short tokens to reduce noise
    tokens = set(re.findall(r'\b\w{3,}\b', text.lower()))
    matched = set()
    for kw in keywords:
        kw_lower = kw.lower()
        for token in tokens:
            score = fuzz.partial_ratio(token, kw_lower)
            if score >= threshold:
                matched.add(kw)
                break
    return sorted(matched)
