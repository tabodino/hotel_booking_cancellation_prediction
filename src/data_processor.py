import logging
from config import LOG_LEVEL
from dataset_downloader import DatasetDownloader

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Get the logger
logger = logging.getLogger(__name__)


class HotelBookingProcessor:
    """Process hotel booking dataset"""

    def download_dataset(self) -> bool:
        downloader = DatasetDownloader()
        return downloader.download_dataset()


def main():
    """Main function to run the hotel booking data processor."""
    processor = HotelBookingProcessor()
    if processor.download_dataset():
        logger.info("Dataset processing completed successfully.")
    else:
        logger.error("Failed to download the dataset.")


if __name__ == "__main__":
    main()
