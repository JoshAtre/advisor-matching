import math
import re
from collections import Counter

STOP_WORDS = set(['the', 'and', 'in', 'of', 'to', 'a', 'for', 'on', 'with', 'is', 'my', 'i', 'am', 'interested', 'looking', 'work'])

def tokenize(text: str):
    if not text: return []
    text = re.sub(r'[^\w\s]', '', text.lower())
    return [w for w in text.split() if w not in STOP_WORDS]

def calculate_cosine_similarity(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    if not denominator: return 0.0
    return float(numerator) / denominator

def generate_weighted_match(user_profile, advisor):
    # 1. Construct User Vector
    user_text = f"{user_profile.interests} {user_profile.goals}"
    user_tokens = tokenize(user_text)
    user_vec = Counter(user_tokens)

    # 2. Construct Advisor Vector (Weighted)
    # We repeat research areas to give them 2x weight in the bag of words
    research_tokens = tokenize(advisor.research_areas) * 2
    bio_tokens = tokenize(advisor.bio)
    dept_tokens = tokenize(advisor.department)
    
    advisor_tokens = research_tokens + bio_tokens + dept_tokens
    advisor_vec = Counter(advisor_tokens)

    # 3. Calculate Score
    score = calculate_cosine_similarity(user_vec, advisor_vec)
    normalized_score = min(round(score * 100, 1), 99.9)

    # 4. Generate Explanation
    common = set(user_tokens).intersection(set(advisor_tokens))
    explanation = ""
    if common:
        top_matches = list(common)[:3]
        explanation = f"Strong match on: {', '.join(top_matches)}."
    else:
        explanation = "Matched based on department alignment."

    return normalized_score, explanation
