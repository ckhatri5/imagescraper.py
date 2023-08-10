import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def download_images_from_page(url, dest_folder):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    image_tags = soup.find_all("img")

    for img_tag in image_tags:
        img_url = img_tag.get("src")
        if img_url and img_url.startswith("http"):
            img_response = requests.get(img_url, stream=True)
            img_name = os.path.basename(img_url)
            img_path = os.path.join(dest_folder, img_name)
            with open(img_path, "wb") as img_file:
                for chunk in img_response.iter_content(chunk_size=8192):
                    img_file.write(chunk)

def crawl_and_download(start_url, dest_folder, depth):
    visited_urls = set()
    queue = [(start_url, depth)]

    while queue:
        current_url, current_depth = queue.pop(0)

        if current_url not in visited_urls and current_depth > 0:
            download_images_from_page(current_url, dest_folder)
            visited_urls.add(current_url)

            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, "html.parser")

            for a_tag in soup.find_all("a", href=True):
                new_url = urljoin(current_url, a_tag["href"])
                queue.append((new_url, current_depth - 1))

# Get user input for website URL, destination folder, and depth
user_url = input("Enter the website URL: ")
user_dest_folder = input("Enter the destination folder path: ")
user_depth = int(input("Enter the depth: "))

crawl_and_download(user_url, user_dest_folder, depth=user_depth)
