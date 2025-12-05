import math
import re
from collections import Counter

# A simple but effective deterministic keyword matching engine.
# No external API keys required.

STOP_WORDS = set(['the', 'and', 'in', 'of', 'to', 'a', 'for', 'on', 'with', 'is', 'my', 'i', 'am', 'interested'])

def tokenize(text: str):
    if not text: return []
    # Lowercase and remove punctuation
    text = re.sub(r'[^\w\s]', '', text.lower())
    return [w for w in text.split() if w not in STOP_WORDS]

def calculate_cosine_similarity(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    if not denominator:
        return 0.0
    return float(numerator) / denominator

def generate_match(user_text: str, advisor_text: str):
    user_tokens = tokenize(user_text)
    advisor_tokens = tokenize(advisor_text)
    
    user_vec = Counter(user_tokens)
    advisor_vec = Counter(advisor_tokens)
    
    score = calculate_cosine_similarity(user_vec, advisor_vec)
    normalized_score = min(round(score * 100, 1), 99.9) # 0 to 100
    
    # Generate explanation
    common = set(user_tokens).intersection(set(advisor_tokens))
    if common:
        top_matches = list(common)[:3]
        explanation = f"Matches on topics: {', '.join(top_matches)}."
    else:
        explanation = "Based on general academic alignment."
        
    return normalized_score, explanation
