import pandas as pd
import re
from rapidfuzz import fuzz

# ----------------------------
# Load harmful ingredient file
# ----------------------------
df = pd.read_excel("harmful.xlsx")

harmful_list = (
    df.iloc[:, 0]
    .dropna()
    .astype(str)
    .str.strip()
    .str.lower()
    .tolist()
)

# ----------------------------
# Ignore marketing / fake text
# ----------------------------
ignore_words = [
    "no parabens",
    "paraben free",
    "cruelty free",
    "not tested on animals",
    "hypoallergenic",
    "100 halal",
    "100% halal",
    "halal",
    "vegan",
    "organic",
    "natural",
    "dermatologically tested"
]


# ----------------------------
# Clean OCR / Input Text
# ----------------------------
def clean_ingredients(text):
    text = text.lower()
    text = text.replace("\n", ",")
    text = text.replace(";", ",")
    text = text.replace("|", ",")

    items = text.split(",")

    final_items = []

    for item in items:
        item = re.sub(r'[^a-zA-Z0-9\s\-]', '', item)
        item = item.strip()

        if len(item) > 2 and item not in ignore_words:
            final_items.append(item)

    return list(set(final_items))


# ----------------------------
# Risk Score Logic
# ----------------------------
def calculate_risk(count):
    if count == 0:
        return "SAFE", 0
    elif count == 1:
        return "LOW RISK", 30
    elif count <= 3:
        return "MEDIUM RISK", 65
    else:
        return "HIGH RISK", 90


# ----------------------------
# Main Analyze Function
# ----------------------------
def analyze_product(raw_text):

    ingredients = clean_ingredients(raw_text)

    found = []

    for ingredient in ingredients:
        for harmful in harmful_list:

            score = fuzz.partial_ratio(
                ingredient.lower(),
                harmful.lower()
            )

            if score >= 85:
                found.append(ingredient)
                break

    found = list(set(found))

    status, risk_score = calculate_risk(len(found))

    return {
        "status": status,
        "risk_score": risk_score,
        "ingredients": ingredients,
        "harmful_found": found,
        "raw_text": raw_text
    }
