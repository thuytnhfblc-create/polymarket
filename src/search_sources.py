
import time
import requests
from datetime import datetime

TODAY = datetime.today().strftime("%Y-%m-%d")


def search_openalex(query, rows=20):
    url = "https://api.openalex.org/works"

    params = {
        "search": query,
        "per-page": rows,
        "sort": "publication_date:desc" # Pick newest paper
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"OpenAlex error for {query}: {e}")
        return []

    papers = []

    for item in response.json().get("results", []):
        authors = []

        for authorship in item.get("authorships", []):
            author = authorship.get("author", {})
            if author.get("display_name"):
                authors.append(author["display_name"])

        doi = item.get("doi", "")
        if doi:
            doi = doi.replace("https://doi.org/", "")

        primary_location = item.get("primary_location") or {}
        source = primary_location.get("source") or {}

        papers.append({
            "source": "OpenAlex",
            "query": query,
            "title": item.get("display_name", ""),
            "authors": ", ".join(authors),
            "year": item.get("publication_year", ""),
            "publication_date": item.get("publication_date", ""),
            "venue": source.get("display_name", ""),
            "abstract": "",
            "doi": doi,
            "url": item.get("id", ""),
            "date_found": TODAY
        })

    return papers


def search_crossref(query, rows=20):
    url = "https://api.crossref.org/works"

    params = {
        "query.bibliographic": query,
        "rows": rows,
        "sort": "published",
        "order": "desc" # Pick newest paper
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Crossref error for {query}: {e}")
        return []

    papers = []

    for item in response.json().get("message", {}).get("items", []):
        title_list = item.get("title", [""])
        venue_list = item.get("container-title", [""])

        date_parts = (
            item.get("published-print")
            or item.get("published-online")
            or item.get("published")
            or {}
        ).get("date-parts", [[None]])

        year = date_parts[0][0] if date_parts and date_parts[0] else ""

        papers.append({
            "source": "Crossref",
            "query": query,
            "title": title_list[0] if title_list else "",
            "authors": ", ".join(
                f"{a.get('given', '')} {a.get('family', '')}".strip()
                for a in item.get("author", [])
            ),
            "year": year,
            "publication_date": "",
            "venue": venue_list[0] if venue_list else "",
            "abstract": item.get("abstract", ""),
            "doi": item.get("DOI", ""),
            "url": item.get("URL", ""),
            "date_found": TODAY
        })

    return papers


def search_all_sources(query, rows=20):
    papers = []

    print(f"Searching OpenAlex: {query}")
    papers.extend(search_openalex(query, rows=rows))

    time.sleep(1)

    print(f"Searching Crossref: {query}")
    papers.extend(search_crossref(query, rows=rows))

    time.sleep(10)

    return papers
