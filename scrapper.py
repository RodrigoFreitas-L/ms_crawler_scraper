from bs4 import BeautifulSoup
from parsel import Selector
from fetch_url import fetch
from wiki_range_links import get_pedia_all_links
from write_mon_links import write_mon_links
import json
import re


BASE_URL = "https://monster-strike-enjp.fandom.com"
NEW_URL_RANGE = ""
URL_RANGES = 0
ALL_MONS_INFO = []


def links_from_file():
    all_links = []
    with open("mon_links.json", "r") as f:
        links = f.read()
        data = json.loads(links)
        for d in data:
            all_links.append(d)
    while URL_RANGES < len(all_links):
        print(len(all_links))
        NEW_URL_RANGE = all_links.pop(0)
        print(NEW_URL_RANGE)
        fetch_monster = fetch(BASE_URL + NEW_URL_RANGE)
        URL_RANGES + 1
        if fetch_monster is not None:
            individual_monster(fetch_monster)


def individual_monster(html_content):
    selector = Selector(text=html_content)
    url = selector.css("h1[class='page-header__title']::text").get()
    title = re.sub("\n|\t", "", url)
    soup = BeautifulSoup(html_content, "lxml")
    rows = soup.find_all("tbody")
    keys = [
        "JP Name",
        "JP #",
        "ID",
        "Rarity",
        "Sling",
        "Type",
        "HP",
        "ATK",
        "SPD",
        "Ability",
        "Gauge",
        "Strike Shot",
        "Bump Combo",
        "Sub Bump",
    ]
    element_keys = [
        ("Wood", "green"),
        ("Fire", "red"),
        ("Water", "blue"),
        ("Light", "yellow"),
        ("Dark", "purple"),
    ]
    for row in range(len(rows)):
        columns_ths = rows[row].find_all("th")
        columns_tds = rows[row].find_all("td")
        monster = {}
        for col in columns_ths:
            mon_img_div = rows[row].find_previous("div", {"class": "center"})
            if hasattr(mon_img_div, "find"):
                mon_img = mon_img_div.find("img")
                if (
                    mon_img is not None
                    and hasattr(mon_img, "get")
                    and mon_img.get("src").startswith("https")
                ):
                    monster["THUMB"] = mon_img.get("src")
                elif (
                    mon_img is not None
                    and hasattr(mon_img, "get")
                    and mon_img.get("data-src").startswith("https")
                ):
                    monster["THUMB"] = mon_img.get("data-src")
                else:
                    monster["THUMB"] = None
            for key in keys:
                if key in col.get_text(strip=True):
                    if hasattr(col.find_next("td"), "get_text"):
                        value = col.find_next("td").get_text(strip=True)
                        if key == "JP Name":
                            value = value.replace("\u3000", " ")
                            monster["JP_Name"] = value
                            monster["ENG_Name"] = title
                        elif key == "JP #":
                            monster["MON_ID"] = value
                        elif key == "Strike Shot":
                            value = value.replace("Turns", "Turns - ")
                            monster["Strike_Shot"] = value
                        elif key == "Bump Combo":
                            value = value.replace(")", ") - ")
                            monster["Bump_Combo"] = value
                        else:
                            monster[key] = value
                            for column in columns_tds:
                                sub_bump = list()
                                if hasattr(column, "find_all"):
                                    data_src = column.find_all(
                                        "img", {"alt": True}
                                    )
                                    # for data in data_src:
                                    #     mon_id = monster["MON_ID"]
                                    #     if mon_id in data["alt"]:
                                    #         monster["THUMB"] = data.get(
                                    #             "data-src"
                                    #         )
                                    # Ill keep it here in case I find a way
                                    # to get only the "small" in game images
                                    for data in data_src:
                                        for element, color in element_keys:
                                            if element in data["alt"]:
                                                monster["Element"] = color
                                if "Sub Bump" in column.get_text(strip=True):
                                    value = column.find_next("td").get_text(
                                        strip=True
                                    )
                                    replaced = value.replace(
                                        "One of the following:", ""
                                    ).split(".")
                                    for element in replaced:
                                        if element != "":
                                            sub_bump.append(
                                                element.replace(")", ") - ")
                                            )
                                    monster["Sub_Bump"] = sub_bump
        if len(monster) > 0:
            ALL_MONS_INFO.append(monster)
        json_object = json.dumps(ALL_MONS_INFO, ensure_ascii=False, indent=4)
        with open("ms_db.json", "w") as f:
            f.write(json_object)


if __name__ == "__main__":
    get_pedia_all_links()
    write_mon_links()
    links_from_file()
