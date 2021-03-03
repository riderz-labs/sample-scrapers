import requests
from bs4 import BeautifulSoup
import os


def get(url):
    response = requests.get(
        url, headers={"User-Agent": "richard fongs elite web browser"}
    )
    return response


def get_audio_paths(base_url):
    res = get(base_url)
    soup = BeautifulSoup(res.text, "html.parser")
    audio_links = []
    for l in soup.select("a"):
        href = l["href"]
        if not href.endswith(".mp3"):
            continue
        audio_links.append(href)

    return audio_links


def download(base_url, path, output_dir):
    output_path = os.path.join(output_dir, path)
    full_url = base_url + path
    res = get(full_url)
    print(full_url + " -> " + output_path)

    parent_dirs = os.path.split(output_path)
    os.makedirs(parent_dirs[0], exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(res.content)


def download_all(output_dir):
    base_url = "https://www.trekcore.com/audio/"
    paths = get_audio_paths(base_url)
    for p in paths:
        download(base_url, p, output_dir)


download_all(output_dir="./downloads")
