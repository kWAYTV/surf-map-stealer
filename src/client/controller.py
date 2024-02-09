import os
import requests
import threading
from loguru import logger
from bs4 import BeautifulSoup

class MapDownloader:
    def __init__(self, base_url, output_folder):
        self.base_url = base_url
        self.output_folder = output_folder
        self.log_lock = threading.Lock()

    def get_file_list(self, url):
        with self.log_lock:
            logger.info(f"Fetching file list from {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return [link.get('href') for link in soup.find_all('a') if link.get('href')]

    def download_file(self, url, file_name):
        full_path = os.path.join(self.output_folder, file_name)
        with self.log_lock:
            logger.info(f"Downloading {url} to {full_path}")
        response = requests.get(url)
        if response.status_code == 200:
            with open(full_path, 'wb') as file:
                file.write(response.content)
            with self.log_lock:
                logger.info(f"Saved {full_path}")
        else:
            with self.log_lock:
                logger.error(f"Failed to download file: {response.status_code}")

    def download_maps(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        files = self.get_file_list(self.base_url)
        if not files:
            with self.log_lock:
                logger.error("No files found or unable to fetch the file list.")
            return

        surf_maps = [(f, f.replace('.bsp', '.nav')) for f in files if 'surf_' in f and f.endswith('.bsp') and f.replace('.bsp', '.nav') in files]

        with self.log_lock:
            logger.info(f"Found {len(surf_maps)} matching files with corresponding .nav files.")

        # Ask for user confirmation
        with self.log_lock:
            logger.info(f"{len(surf_maps)} matching files found. Do you want to continue with the download? (yes/no): ")
        confirm = input()
        if confirm.lower() != 'yes':
            logger.info("Download cancelled by user.")
            return

        threads = []

        for map_file, nav_file in surf_maps:
            map_url = (self.base_url + map_file) if not map_file.startswith('http') else map_file
            nav_url = (self.base_url + nav_file) if not nav_file.startswith('http') else nav_file

            # Create threads for downloading each file
            t1 = threading.Thread(target=self.download_file, args=(map_url, map_file.split('/')[-1]))
            t2 = threading.Thread(target=self.download_file, args=(nav_url, nav_file.split('/')[-1]))
            threads.extend([t1, t2])

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()