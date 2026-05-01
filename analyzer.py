import pandas as pd
import easyocr
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
# OCR Reader Load Once
# ----------------------------
reader = easyocr.Reader(['en'], gpu=False)


# ----------------------------
# Clean OCR Text
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

        if len(item) > 2:
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
def analyze_product(image_path):

    # OCR read image
    results = reader.readtext(image_path, detail=0)

    raw_text = " ".join(results)

    # Extract ingredients
    ingredients = clean_ingredients(raw_text)

    found = []

    # Fuzzy Match Harmful Items
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

    # Risk Result
    status, risk_score = calculate_risk(len(found))

    return {
        "status": status,
        "risk_score": risk_score,
        "ingredients": ingredients,
        "harmful_found": found,
        "raw_text": raw_text
    }
