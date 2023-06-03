import requests
import os
from bs4 import BeautifulSoup
import json


def get_headers():
    import random
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
    ]

    return {
        "User-Agent": user_agents[random.randint(0, len(user_agents)-1)],
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }

# Gets the current details of the site used


def site_details(url):
   # Please note the json file is partially AI generated, so it may not be 100% accurate
   # If you find any errors, you can contribute to the project by making a pull request
    sites = json.load(open(
        "data/amazon-sites.json", "r",
        encoding="UTF-8"
    ))
    for site in sites:
        if site+"/" in url[:40]:
            return sites[site]
    return None

# Gets the details of the item


def get_item_details(url):
    try:
        # get the html content for the product page
        html = BeautifulSoup(requests.get(
            url,headers=get_headers()).content, 'html.parser')

        # get the title
        title = html.find('span', id='productTitle').text.strip()
        # get the price
        price_placeholder = html.find('div', id='apex_desktop')
        price = price_placeholder.find(
            'span', class_='a-offscreen').text.strip()
        print("ok")
        return {
            "title": title,
            "price": price,
            "url": url
        }
    except Exception as er:
        if "robot" in str(html) and "accepting cookies" in str(html):
            print("Error, you may have been detected as a robot, please try again later.")
            return
        print(er)
        print("Error, this may be an invalid URL, please try using the share button on the Amazon page.")


# Test
url = input("Enter Amazon URL: ")
print(get_item_details(url))
print(site_details(url))
