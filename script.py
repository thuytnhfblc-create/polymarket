import google.genai as genai
import pandas as pd
import json
API_KEY='AIzaSyDT8b6cU-zJ6RRjY9xhM0GxBZnOv3CdfHk'
client=genai.Client(api_key=API_KEY)
def classify_batch(entities):
    prompt = f"""Classify each financial institution into one of:
asset manager, bank, dealer, hedge fund, insurer, non-financial, official, other financial, pension fund, ptf, trading services

Entities:
{json.dumps(entities, indent=2)}

Return ONLY a valid JSON array, each object with:
- lei
- legal name 
- sector
- confidence (HIGH/MEDIUM/LOW)
- reasoning (one sentence)"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    text = response.text.strip()
    if text.startswith("```json"):
        text = text.replace("```json", "", 1).replace("```", "", 1).strip()
    elif text.startswith("```"):
        text = text.replace("```", "", 2).strip()

    return json.loads(text)

INPUT_PATH = r"\\wwz-jumbo.storage.p.unibas.ch\wwz-home01$\hoang0000\Downloads\unclassified_counterparty_ids.txt"
OUTPUT_PATH = r"\\wwz-jumbo.storage.p.unibas.ch\wwz-home01$\hoang0000\Downloads\lei_classified.csv"

df = pd.read_csv(INPUT_PATH, sep='\t', names=['lei'])
results = []

print(f"Starting processing of {len(df)} records...")
batch = df.to_dict("records")

try:
        classified = classify_batch(batch)
        results.extend(classified)

except Exception as e:
        print(f"Error at batch: {e}")
        if "429" in str(e):
            print("Quota exceeded. Waiting 30 seconds...")

final_df = pd.DataFrame(results)
final_df.to_csv(OUTPUT_PATH, index=False)
print(f"Process completed. File saved to: {OUTPUT_PATH}")
