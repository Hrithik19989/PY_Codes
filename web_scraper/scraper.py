import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import time

BASE_URL    = "http://books.toscrape.com"
OUTPUT_FILE = Path("books.csv")

RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3,
    "Four": 4, "Five": 5
}


# ── Fetch ──────────────────────────────────────────────────────────────────────

def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.HTTPError as e:
        print(f"  HTTP error: {e}")
    except requests.exceptions.ConnectionError:
        print("  No internet connection.")
    except requests.exceptions.Timeout:
        print("  Request timed out.")
    return None


# ── Parse ──────────────────────────────────────────────────────────────────────

def parse_books(soup):
    books    = []
    articles = soup.find_all("article", class_="product_pod")

    for article in articles:
        title  = article.h3.a["title"]
        price  = article.find("p", class_="price_color").text.strip()
        rating = article.find("p", class_="star-rating")["class"][1]
        avail  = article.find("p", class_="availability").text.strip()

        books.append({
            "title":        title,
            "price":        float(price.replace("£", "").replace("Â", "")),
            "rating":       RATING_MAP.get(rating, 0),
            "availability": avail
        })

    return books


def get_next_page(soup, current_url):
    next_btn = soup.find("li", class_="next")
    if not next_btn:
        return None

    next_href = next_btn.a["href"]

    if "catalogue/" in current_url:
        base = current_url.rsplit("/", 1)[0]
        return f"{base}/{next_href}"
    else:
        return f"{BASE_URL}/catalogue/{next_href}"


def get_categories(soup):
    sidebar = soup.find("ul", class_="nav-list")
    links   = sidebar.find_all("a")[1:]

    categories = {}
    for link in links:
        name = link.text.strip()
        url  = f"{BASE_URL}/{link['href']}"
        categories[name.lower()] = url

    return categories


# ── Scrape ─────────────────────────────────────────────────────────────────────

def scrape(url, max_pages=None):
    all_books   = []
    page_num    = 1
    current_url = url

    while current_url:
        if max_pages and page_num > max_pages:
            break

        print(f"  Scraping page {page_num}... ", end="", flush=True)
        soup = fetch_page(current_url)

        if not soup:
            break

        books = parse_books(soup)
        all_books.extend(books)
        print(f"{len(books)} books found.")

        current_url = get_next_page(soup, current_url)
        page_num   += 1
        time.sleep(0.5)

    print(f"\n  ✓ Total: {len(all_books)} books scraped.")
    return all_books


# ── Save ───────────────────────────────────────────────────────────────────────

def save_to_csv(books, filename=OUTPUT_FILE):
    df = pd.DataFrame(books)
    df = df.sort_values("rating", ascending=False)
    df.to_csv(filename, index=False)
    print(f"  ✓ Saved to {filename}")


# ── Menu ───────────────────────────────────────────────────────────────────────

def menu():
    print("\n  🕷️  WEB SCRAPER — Books to Scrape")
    print("  " + "=" * 35)
    print("  1. Scrape all books (all pages)")
    print("  2. Scrape a specific category")
    print("  3. Scrape first N pages only")
    print("  4. Exit")


def main():
    while True:
        menu()
        choice = input("\n  Choose (1-4): ").strip()

        if choice == "1":
            print("\n  Scraping all books...")
            books = scrape(f"{BASE_URL}/catalogue/page-1.html")
            if books:
                save_to_csv(books)

        elif choice == "2":
            soup = fetch_page(BASE_URL)
            if not soup:
                continue
            cats = get_categories(soup)
            print("\n  Available categories:")
            for i, name in enumerate(sorted(cats.keys()), 1):
                print(f"    {i:>2}. {name.title()}")

            cat_name = input("\n  Enter category name: ").strip().lower()
            if cat_name not in cats:
                print(f"  Category '{cat_name}' not found.")
                continue

            print(f"\n  Scraping '{cat_name}'...")
            books = scrape(cats[cat_name])
            if books:
                filename = Path(f"{cat_name.replace(' ', '_')}_books.csv")
                save_to_csv(books, filename)

        elif choice == "3":
            try:
                n = int(input("  How many pages? "))
                if n < 1:
                    print("  Enter at least 1.")
                    continue
            except ValueError:
                print("  Please enter a valid number.")
                continue

            print(f"\n  Scraping first {n} page(s)...")
            books = scrape(f"{BASE_URL}/catalogue/page-1.html", max_pages=n)
            if books:
                save_to_csv(books, Path(f"books_page1to{n}.csv"))

        elif choice == "4":
            print("\n  Goodbye! 👋\n")
            break

        else:
            print("  Invalid choice. Enter 1 to 4.")


if __name__ == "__main__":
    main()