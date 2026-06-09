
import pandas as pd

from src.config import KEYWORDS, DATABASE_PATH, REPORTS_DIR
from src.search_sources import search_all_sources
from src.database import (
    load_database,
    remove_duplicates,
    filter_quality_sources,
    find_new_papers,
    update_database
)
from src.report import generate_report
from src.cleaning import clean_papers, fill_missing_abstracts_with_gemini


def main():
    all_results = []

    for keyword in KEYWORDS:
        print(f"\nSearching keyword: {keyword}")
        results = search_all_sources(keyword, rows=10)
        print(f"Found {len(results)} papers")
        all_results.extend(results)

    found_df = pd.DataFrame(all_results)

    found_df = remove_duplicates(found_df)
    print(f"Total unique papers before quality filter: {len(found_df)}")

    found_df = filter_quality_sources(found_df)
    print(f"Total papers after quality filter: {len(found_df)}")

    existing_df = load_database(DATABASE_PATH)

    if not existing_df.empty:
        existing_df = remove_duplicates(existing_df)

    new_df = find_new_papers(existing_df, found_df)
    print(f"New papers this run: {len(new_df)}")

    # Combine old papers + new papers first
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)

    # Clean duplicate/bad rows
    combined_df = clean_papers(combined_df)

    # Fill missing abstracts with Gemini
    combined_df = fill_missing_abstracts_with_gemini(combined_df)

    # Save final cleaned database
    combined_df.to_csv(DATABASE_PATH, index=False)

    # Generate report only for the new papers
    report_path = generate_report(new_df, REPORTS_DIR)

    print(f"Report created: {report_path}")


if __name__ == "__main__":
    main()
