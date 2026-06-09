
import os
import pandas as pd


def load_database(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def make_paper_id(row):
    doi = str(row.get("doi", "")).lower().strip()
    title = str(row.get("title", "")).lower().strip()

    if doi and doi != "nan":
        return doi

    return title


def remove_duplicates(df):
    if df.empty:
        return df

    df["paper_id"] = df.apply(make_paper_id, axis=1)
    df = df[df["paper_id"] != ""]
    return df.drop_duplicates(subset=["paper_id"])


def filter_quality_sources(df):
    if df.empty:
        return df

    good_journals = [
    # --- Your Original Elite List ---
    "journal of finance",
    "the journal of finance",
    "journal of financial economics",
    "review of financial studies",
    "the review of financial studies",
    "management science",
    "review of finance",
    "journal of financial and quantitative analysis",
    "journal of economic perspectives",
    "american economic review",
    "the american economic review",
    "quarterly journal of economics",
    "the quarterly journal of economics",
    "journal of political economy",
    "the journal of political economy",
    "econometrica",
    "review of economic studies",
    "the review of economic studies",

    # --- Elite General & Field Economics ---
    "journal of the european economic association",
    "review of economics and statistics",
    "the review of economics and statistics",
    "international economic review",
    "economic journal",
    "the economic journal",
    "american economic review: insights",
    "journal of economic literature",

    # --- Econometrics & Theory ---
    "journal of econometrics",
    "journal of business & economic statistics",
    "econometric theory",
    "quantitative economics",
    "journal of economic theory",
    "theoretical economics",
    "journal of applied econometrics",

    # --- AEJ Outlets ---
    "american economic journal: applied economics",
    "american economic journal: economic policy",
    "american economic journal: macroeconomics",
    "american economic journal: microeconomics",

    # --- Macro, Banking, & International ---
    "journal of monetary economics",
    "journal of international economics",
    "journal of money, credit and banking",
    "journal of economic dynamics and control",

    # --- Corporate Finance, Intermediation, & Banking ---
    "journal of banking & finance",
    "journal of financial intermediation",
    "journal of corporate finance",
    "journal of empirical finance",
    "financial management",

    # --- Micro, Labor, & Behavioral ---
    "journal of labor economics",
    "journal of human resources",
    "games and economic behavior",
    "journal of risk and uncertainty",

    # --- Public, Development, Urban, & History ---
    "journal of public economics",
    "journal of development economics",
    "journal of urban economics",
    "journal of environmental economics and management",
    "world development",
    "journal of economic growth",
    "journal of economic history",
    "journal of law and economics"
]

    working_paper_series = [
        "nber working paper",
        "bis working paper",
        'bis',
        "nber working papers",
        "cepr discussion paper",
        "cepr discussion papers",
        "iza discussion paper",
        "iza discussion papers",
        "ssrn electronic journal",
        "ssrn",
        "working paper",
        "working papers",
        "discussion paper",
        "discussion papers",
        "research paper series",
        "research papers in economics",
        "repec",
        "arxiv",
        "econpapers",
        "staff report",
        "federal reserve",
        "fed working paper",
        "bank of england working paper",
        "ecb working paper",
        "imf working paper",
        "world bank policy research working paper",
    ]

    venue = df["venue"].fillna("").str.lower()
    source = df["source"].fillna("").str.lower()
    url = df["url"].fillna("").str.lower()

    keep_good_journal = venue.apply(
        lambda x: any(journal in x for journal in good_journals)
    )

    keep_working_paper = (
        venue.apply(lambda x: any(wp in x for wp in working_paper_series))
        | source.apply(lambda x: any(wp in x for wp in working_paper_series))
        | url.apply(lambda x: any(wp in x for wp in working_paper_series))
    )

    return df[keep_good_journal | keep_working_paper].copy()


def find_new_papers(existing_df, found_df):
    if existing_df.empty:
        return found_df

    existing_ids = set(existing_df["paper_id"])
    return found_df[~found_df["paper_id"].isin(existing_ids)]


def update_database(existing_df, new_df, path):
    combined = pd.concat([existing_df, new_df], ignore_index=True)
    combined = remove_duplicates(combined)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    combined.to_csv(path, index=False)

    return combined
