"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>

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
