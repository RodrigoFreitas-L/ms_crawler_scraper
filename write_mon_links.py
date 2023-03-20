from parsel import Selector
from fetch_url import fetch
import json

BASE_URL = "https://monster-strike-enjp.fandom.com"
mon_links = set()


def write_mon_links():
    mons_links = set()
    with open("pedia_links.json", "r") as r:
        links = r.read()
        data = json.loads(links)
        for link in data:
            mons_links.add(link)
    for link in mons_links:
        wiki = fetch(BASE_URL + link)
        selector = Selector(text=wiki)
        monster_url = selector.css("table a::attr(href)").getall()
        for mon in monster_url:
            if not mon.startswith("https") and not mon.endswith("_Gem"):
                mon_links.add(mon)
                print("Writing on file:", mon)
    json_object = json.dumps(list(mon_links), indent=4)
    with open("mon_links.json", "w") as f:
        f.write(json_object)


if __name__ == "__main__":
    write_mon_links()
