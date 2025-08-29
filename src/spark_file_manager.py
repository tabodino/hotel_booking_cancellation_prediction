import shutil
from pathlib import Path
from src.utils import get_logger


logger = get_logger(__name__)

# Constants
PROCESSED_FOLDER = "data/processed"


class SparkFileManager:
    """Handles Spark output file management and cleanup operations."""

    @staticmethod
    def clean_spark_output(output_dir: str, final_filename: str) -> bool:
        """
        Clean Spark output directory by renaming part files and removing metadata files.

        Args:
            output_dir: Directory containing Spark output files
            final_filename: Final name for the consolidated CSV file

        Returns:
            bool: True if cleanup was successful, False otherwise
        """
        try:
            output_path = Path(output_dir)
            final_path = output_path / final_filename

            # Check for _SUCCESS file to ensure write completed
            success_file = output_path / "_SUCCESS"
            if not success_file.exists():
                logger.error(f"Missing _SUCCESS file in {output_dir}")
                return False

            # Find and rename part file
            part_files = list(output_path.glob("part-*.csv"))
            if not part_files:
                logger.error(f"No part files found in {output_dir}")
                return False

            # Move the first part file to final location
            src_file = part_files[0]
            shutil.move(str(src_file), str(final_path))
            logger.info(f"Renamed {src_file.name} to {final_path}")

            # Remove .crc files
            SparkFileManager._remove_crc_files(output_path)

            # Remove _SUCCESS file
            success_file.unlink()
            logger.info("Removed _SUCCESS file")

            # Remove the output directory if it's empty or only contains metadata
            SparkFileManager._cleanup_directory(output_path)

            return True

        except Exception as e:
            logger.error(f"Error during Spark output cleanup: {e}")
            return False

    @staticmethod
    def _remove_crc_files(directory: Path) -> None:
        """Remove all .crc files from the directory."""
        crc_files = list(directory.glob("*.crc"))
        for crc_file in crc_files:
            try:
                crc_file.unlink()
                logger.info(f"Removed .crc file: {crc_file.name}")
            except Exception as e:
                logger.error(f"Error removing .crc file {crc_file.name}: {e}")

    @staticmethod
    def _cleanup_directory(directory: Path) -> None:
        """Remove directory if it's empty or only contains Spark metadata."""
        try:
            remaining_files = list(directory.iterdir())
            if not remaining_files:
                directory.rmdir()
                logger.info(f"Removed empty directory: {directory}")
            else:
                # Only remove if remaining files are just Spark metadata
                metadata_flags = ["_SUCCESS", "_committed_", "_started_"]
                metadata_only = all(
                    f.name.startswith(".") or f.name in metadata_flags
                    for f in remaining_files
                )
                if metadata_only:
                    shutil.rmtree(str(directory), ignore_errors=True)
                    logger.info(f"Removed metadata directory: {directory}")
        except Exception as e:
            logger.error(f"Error cleaning up directory {directory}: {e}")
