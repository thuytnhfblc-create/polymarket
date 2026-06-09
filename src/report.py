
import os
from datetime import date


def generate_report(new_papers, reports_dir):
    os.makedirs(reports_dir, exist_ok=True)

    today = date.today().strftime("%Y-%m-%d")
    path = f"{reports_dir}/weekly_digest_{today}.md"

    with open(path, "w", encoding="utf-8") as f:
        f.write("# Weekly Prediction Market Literature Digest\n\n")
        f.write(f"Date: {today}\n\n")

        if new_papers.empty:
            f.write("No new high-quality papers found this week.\n")
            return path

        for _, row in new_papers.iterrows():
            f.write(f"## {row['title']}\n\n")
            f.write(f"**Source:** {row['source']}\n\n")
            f.write(f"**Authors:** {row['authors']}\n\n")
            f.write(f"**Year:** {row['year']}\n\n")
            f.write(f"**Venue:** {row['venue']}\n\n")
            f.write(f"**DOI:** {row['doi']}\n\n")
            f.write(f"**URL:** {row['url']}\n\n")
            f.write("---\n\n")

    return path
