"""
Created by: https://github.com/Ginotuch/

This scrapes http://simonstalenhag.se/ for all full resolution images.
This is an unofficial script, and unaffiliated with http://simonstalenhag.se/ or Simon Stålenhag

Use at own risk
"""

from multiprocessing.dummy import Pool as ThreadPool

import requests

image_links = []
r = requests.get("http://simonstalenhag.se/", stream=True)
for x in r.text.split("href=\""):
    if "jpg" in x.split("\"")[0] or "png" in x.split("\"")[0] or "gif" in x.split("\"")[0]:  # Only downloads images
        if "http://simonstalenhag.se/" + x.split("\"")[0] not in image_links:  # Removes duplicate links
            if "gui/" not in x.split("\"")[0]:  # Removes page buttons
                image_links.append("http://simonstalenhag.se/" + x.split("\"")[0])


def download_image(url):
    try:
        with open(url.split("/")[-1]) as test_file:  # Only opens if the file exists, otherwise errors out
            print("Already downloaded:", url)
    except FileNotFoundError or FileExistsError:
        try:
            r = requests.get(url, timeout=10)
        except:
            print("FAILED:", url)
            return
        if r.status_code != requests.codes.ok:
            print("ERROR 404:", url)
            return
        with open(url.split("/")[-1], "wb") as out:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    out.write(chunk)
        print("SUCCESS:", url)


with ThreadPool(processes=20) as pool:
    pool.map(download_image, image_links)
