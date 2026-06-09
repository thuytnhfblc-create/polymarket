
import os
import time
import pandas as pd
from google import genai


def clean_papers(df):
    # 1. Identify duplicate titles
    is_duplicate = df.duplicated(subset=["title"], keep=False)

    # 2. Mark rows where authors contain numbers
    has_digits = df["authors"].astype(str).str.contains(r"\d+", na=False)

    # 3. Mark rows where abstract is missing
    if "abstract" in df.columns:
        has_null_abstract = df["abstract"].isna()
    else:
        df["abstract"] = pd.NA
        has_null_abstract = df["abstract"].isna()

    # 4. Remove duplicate rows only if they are bad
    df_cleaned = df[~(is_duplicate & (has_digits | has_null_abstract))].copy()

    # 5. If duplicates still remain, keep the first one
    df_cleaned = df_cleaned.drop_duplicates(subset=["title"], keep="first")

    return df_cleaned


def fill_missing_abstracts_with_gemini(df):
    # Get Gemini API key from GitHub secret or local environment
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("No GEMINI_API_KEY found. Skipping Gemini abstract step.")
        return df

    client = genai.Client(api_key=api_key)

    for index, row in df.iterrows():
        if pd.isna(row.get("abstract")) or row.get("abstract") == "":
            print(f"Fetching abstract: {row['title']}")

            prompt = (
                f"Provide only the academic abstract for the paper titled "
                f"'{row['title']}' by {row['authors']}. "
                f"Do not include any other text."
            )

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                df.at[index, "abstract"] = response.text.strip()

                # You can adjust this if Gemini rate limits you
                time.sleep(10)

            except Exception as e:
                print(f"Skipped {row['title']} due to error: {e}")

    # Remove JATS tags if they appear
    df["abstract"] = df["abstract"].astype(str).str.replace(
        r"</?jats:p>",
        "",
        regex=True
    )

    return df
