import pandas as pd

df = pd.read_excel("harmful.xlsx")
harmful_list = df.iloc[:,0].astype(str).str.strip().tolist()

def analyze_product(image_path):

    ingredients = ["water", "paraben"]

    found = []

    for item in ingredients:
        for harmful in harmful_list:
            if item.lower() in harmful.lower():
                found.append(item)
                break

    status = "RISKY" if found else "SAFE"

    return {
        "status": status,
        "ingredients": ingredients,
        "harmful_found": found
    }