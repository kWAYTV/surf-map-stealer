from loguru import logger
from src.utils.utils import Utils
from src.client.controller import MapDownloader

class Main:
    def __init__(self):
        # Initialize the Utils class
        self.utils = Utils()

        # Set logging system handler
        logger.add("map_stealer.log", mode="w+")

        # Initialize the MapDownloader class to handle the download process later
        self.downloader = None

    def take_input(self) -> tuple:
        # Ask for user input
        logger.info("FastDL URL to steal maps from: ")
        base_url = input() or None

        if not base_url:
            logger.error("No URL provided. Exiting...")
            exit(1)

        logger.info("Output folder (default: output): ")
        output_folder = input() or 'output'

        return base_url, output_folder

    def start(self):
        self.utils.print_logo()
        logger.info("Welcome to Map Stealer!")

        # Ask for user input
        base_url, output_folder = self.take_input()

        # Initialize the MapDownloader class
        self.downloader = MapDownloader(base_url, output_folder)

        # Start the download process
        self.downloader.download_maps()

        logger.info("All done! Exiting...")
        exit(0)

if __name__ == "__main__":
    Main().start()
