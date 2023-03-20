from parsel import Selector
from fetch_url import fetch
import json


BASE_URL = "https://monster-strike-enjp.fandom.com"
MONSTERPEDIA_URL = "/wiki/Monsterpedia"
PEDIA_LINKS = []


def get_pedia_all_links():
    wiki = fetch(BASE_URL + MONSTERPEDIA_URL)
    selector = Selector(text=wiki)
    monsters_url = selector.css(".article-table a::attr(href)").getall()
    if len(PEDIA_LINKS) == 0 or len(PEDIA_LINKS) != monsters_url:
        for url in monsters_url:
            PEDIA_LINKS.append(url)
    json_object = json.dumps(PEDIA_LINKS, indent=4)
    with open("pedia_links.json", "w") as f:
        f.write(json_object)


if __name__ == "__main__":
    get_pedia_all_links()
