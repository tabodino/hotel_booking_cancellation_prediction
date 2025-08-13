from pathlib import Path
import os
import logging
from config import (
    LOG_LEVEL,
    KAGGLE_DATASET_NAME,
    KAGGLE_DATASET_ID,
    GIST_RAW_URL,
    DATASET_SOURCE,
)
from kaggle.api.kaggle_api_extended import KaggleApi

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Get the logger
logger = logging.getLogger(__name__)


class DatasetDownloader:
    """Download dataset from a specified source."""

    def __init__(self, data_path: str = "data/raw/"):
        self.data_path = Path(data_path)
        self.data_path.mkdir(exist_ok=True)
        self.source = DATASET_SOURCE.lower()

    def download_dataset(self) -> bool:
        """Download the dataset from the configured source."""
        if self.source == "kaggle":
            return self._download_from_kaggle()
        elif self.source == "gist":
            return self._download_from_gist()
        else:
            logger.error(f"Unknown dataset source: {self.source}")
            return False

    def _download_from_kaggle(self) -> bool:
        """Download the dataset from Kaggle."""
        dataset_path = self.data_path / KAGGLE_DATASET_NAME
        if dataset_path.exists():
            logger.info(f"Dataset already exists: {dataset_path}")
            return True

        try:
            api = KaggleApi()
            api.authenticate()

            filename = api.dataset_list_files(KAGGLE_DATASET_ID).files[0].name
            api.dataset_download_files(
                KAGGLE_DATASET_ID, path=str(self.data_path), unzip=True
            )

            original_path = self.data_path / filename
            renamed_path = self.data_path / KAGGLE_DATASET_NAME
            if original_path.exists():
                os.rename(original_path, renamed_path)

            logger.info(f"Dataset '{KAGGLE_DATASET_NAME}' downloaded successfully.")
            return True

        except Exception as e:
            logger.error(f"Error downloading dataset via Kaggle API: {e}")
            logger.info("Dataset should be downloaded manually from Kaggle:")
            logger.info(f"https://www.kaggle.com/datasets/{KAGGLE_DATASET_ID}")
            return False

    def _download_from_gist(self) -> bool:
        """Download the dataset from a public Gist or raw URL."""
        import requests

        dataset_path = self.data_path / KAGGLE_DATASET_NAME
        if dataset_path.exists():
            logger.info(f"Dataset already exists: {dataset_path}")
            return True

        try:
            response = requests.get(GIST_RAW_URL)
            response.raise_for_status()

            with open(dataset_path, "wb") as file:
                file.write(response.content)

            logger.info(f"Dataset downloaded from Gist to: {dataset_path}")
            return True

        except Exception as e:
            logger.error(f"Error downloading dataset from Gist: {e}")
            logger.info("You can manually download it from:")
            logger.info(GIST_RAW_URL)
            return False
