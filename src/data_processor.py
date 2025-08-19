from pyspark.sql import SparkSession, DataFrame
from typing import Tuple
import os
from pathlib import Path
from dataset_downloader import DatasetDownloader
from spark_file_manager import SparkFileManager
from data_transformer import DataTransformer
import logging
from config import LOG_LEVEL, KAGGLE_DATASET_NAME

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

PROCESSED_FOLDER = "data/processed"
DEFAULT_TRAIN_RATIO = 0.8
DEFAULT_SEED = 42


class HotelBookingProcessor:
    """Main processor for hotel booking dataset with improved architecture."""

    def __init__(self, app_name: str = "HotelRevenueAnalysis"):
        """Initialize the processor with Spark session."""
        self.spark = SparkSession.builder.appName(app_name).getOrCreate()
        self.downloader = DatasetDownloader()
        self.file_manager = SparkFileManager()
        self.transformer = DataTransformer()
        logger.info(f"Initialized {app_name} Spark session")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures Spark session is closed."""
        self.close()

    def close(self) -> None:
        """Close the Spark session."""
        if self.spark:
            self.spark.stop()
            logger.info("Spark session closed")

    def download_dataset(self) -> bool:
        """Download the dataset using DatasetDownloader."""
        try:
            return self.downloader.download_dataset()
        except Exception as e:
            logger.error(f"Error downloading dataset: {e}")
            return False

    def load_data(self, input_path: str) -> DataFrame:
        """Load CSV data into Spark DataFrame."""
        try:
            logger.info(f"Loading data from {input_path}")
            df = self.spark.read.csv(input_path, header=True, inferSchema=True)
            logger.info(f"Loaded {df.count()} rows with {len(df.columns)} columns")
            return df
        except Exception as e:
            logger.error(f"Error loading data from {input_path}: {e}")
            return None

    def preprocess_dataset(self, input_path: str, output_path: str) -> DataFrame:
        """
        Preprocess the hotel booking dataset with comprehensive transformations.

        Args:
            input_path: Path to the input CSV file
            output_path: Path to save the processed data

        Returns:
            Processed DataFrame or None if processing failed
        """
        logger.info("Starting dataset preprocessing...")

        try:
            # Load data
            df = self.load_data(input_path)
            if df is None:
                return None

            # Apply transformations
            df = self.transformer.add_date_features(df)
            df = self.transformer.add_cyclical_features(df)
            df = self.transformer.encode_categorical_features(df)

            # Remove unused columns
            columns_to_drop = ["Profit"]  # Make this configurable if needed
            for col_name in columns_to_drop:
                if col_name in df.columns:
                    df = df.drop(col_name)
                    logger.info(f"Dropped column: {col_name}")

            # Save processed data
            df.coalesce(1).write.csv(output_path, header=True, mode="overwrite")
            logger.info(f"Preprocessing completed. Saved to {output_path}")

            return df

        except Exception as e:
            logger.error(f"Error during preprocessing: {e}")
            return None

    def finalize_csv_output(
        self, output_dir: str = PROCESSED_FOLDER, filename: str = KAGGLE_DATASET_NAME
    ) -> bool:
        """
        Finalize CSV output by cleaning up Spark metadata files.

        Args:
            output_dir: Directory containing the processed files
            filename: Final filename for the CSV

        Returns:
            bool: True if successful, False otherwise
        """
        return self.file_manager.clean_spark_output(output_dir, filename)

    def split_and_save_datasets(
        self,
        df: DataFrame,
        output_dir: str,
        train_ratio: float = DEFAULT_TRAIN_RATIO,
        seed: int = DEFAULT_SEED,
    ) -> Tuple[DataFrame, DataFrame]:
        """
        Split DataFrame into train/test sets and save as CSV files.

        Args:
            df: DataFrame to split
            output_dir: Directory to save the CSV files
            train_ratio: Proportion of data for training (0.0 to 1.0)
            seed: Random seed for reproducibility

        Returns:
            Tuple of (train_df, test_df) or (None, None) if failed
        """
        try:
            if not (0.0 < train_ratio < 1.0):
                raise ValueError(
                    f"train_ratio must be between 0 and 1, got {train_ratio}"
                )

            # Split the data
            train_df, test_df = df.randomSplit(
                [train_ratio, 1 - train_ratio], seed=seed
            )

            train_count = train_df.count()
            test_count = test_df.count()
            logger.info(f"Split data: Train={train_count}, Test={test_count}")

            # Prepare output paths
            output_path = Path(output_dir)
            train_path = output_path / "train"
            test_path = output_path / "test"

            # Save datasets
            train_df.coalesce(1).write.csv(
                str(train_path), header=True, mode="overwrite"
            )
            test_df.coalesce(1).write.csv(str(test_path), header=True, mode="overwrite")

            logger.info(f"Train set saved to: {train_path}")
            logger.info(f"Test set saved to: {test_path}")

            return train_df, test_df

        except Exception as e:
            logger.error(f"Error splitting and saving datasets: {e}")
            return None, None

    def clean_split_outputs(self, output_dir: str) -> bool:
        """
        Clean up both train and test split outputs.

        Args:
            output_dir: Base directory containing train/test subdirectories

        Returns:
            bool: True if both cleanups successful, False otherwise
        """
        train_success = self.file_manager.clean_spark_output(
            os.path.join(output_dir, "train"), "train.csv"
        )
        test_success = self.file_manager.clean_spark_output(
            os.path.join(output_dir, "test"), "test.csv"
        )

        return train_success and test_success

    def process_complete_pipeline(
        self, input_path: str, output_dir: str = PROCESSED_FOLDER
    ) -> bool:
        """
        Execute the complete data processing pipeline.

        Args:
            input_path: Path to raw data file
            output_dir: Directory for processed outputs

        Returns:
            bool: True if pipeline completed successfully
        """
        try:
            # Preprocess the dataset
            df_processed = self.preprocess_dataset(input_path, output_dir)
            if df_processed is None:
                return False

            # Clean up main processed file
            if not self.finalize_csv_output(output_dir):
                logger.error("Failed to finalize main CSV output")
                return False

            # Split and save train/test sets
            train_df, test_df = self.split_and_save_datasets(df_processed, output_dir)
            if train_df is None or test_df is None:
                return False

            # Clean up split outputs
            if not self.clean_split_outputs(output_dir):
                logger.error("Failed to clean split outputs")
                return False

            logger.info("Complete pipeline executed successfully")
            return True

        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            return False


def main():
    """Main function to run the hotel booking data processor."""

    # Use context manager to ensure proper resource cleanup
    with HotelBookingProcessor() as processor:

        # Download dataset
        if not processor.download_dataset():
            logger.error("Failed to download the dataset.")
            return False

        # Execute complete pipeline
        input_path = f"data/raw/{KAGGLE_DATASET_NAME}"
        success = processor.process_complete_pipeline(input_path)

        if success:
            logger.info("Hotel booking data processing completed successfully!")
        else:
            logger.error("Data processing pipeline failed.")

        return success


if __name__ == "__main__":
    main()
