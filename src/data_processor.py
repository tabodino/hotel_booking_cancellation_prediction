from pathlib import Path
import logging
from config import LOG_LEVEL, KAGGLE_DATASET_NAME, KAGGLE_DATASET_URL
from urllib.request import urlretrieve

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Get the logger
logger = logging.getLogger(__name__)


class HotelBookingProcessor:
    """Process hotel booking data from Kaggle dataset"""

    def __init__(self, data_path: str = "data/raw/"):
        self.data_path = Path(data_path)
        self.data_path.mkdir(exist_ok=True)

    def download_dataset(self) -> bool:
        """Download the hotel booking dataset using the direct URL."""
        dataset_path = self.data_path / KAGGLE_DATASET_NAME
        if dataset_path.exists():
            logger.info(f"Dataset already exists: {dataset_path}")
            return True

        try:
            urlretrieve(KAGGLE_DATASET_URL, str(dataset_path))
            logger.info(f"Dataset '{KAGGLE_DATASET_NAME}' downloaded successfully.")
            return True

        except Exception as e:
            logger.error(f"Error downloading dataset: {e}")
            return False


def main():
    """Main function to run the hotel booking data processor."""
    processor = HotelBookingProcessor()
    if processor.download_dataset():
        logger.info("Dataset processing completed successfully.")
    else:
        logger.error("Failed to download the dataset.")


if __name__ == "__main__":
    main()
