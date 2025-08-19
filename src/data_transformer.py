# pylint: disable=invalid-name
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, sin, cos, to_date, dayofmonth, month, dayofweek
from pyspark.ml.feature import StringIndexer
import logging
import math
from config import LOG_LEVEL

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


CYCLICAL_MONTHS = 12
CYCLICAL_WEEKDAYS = 7


class DataTransformer:
    """Handles data transformation operations for hotel booking data."""

    @staticmethod
    def add_date_features(df: DataFrame) -> DataFrame:
        """Add date-based features to the DataFrame."""
        logger.info("Adding date features...")

        df = df.withColumn("Date", to_date(col("Date"), "dd/MM/yyyy"))
        df = df.withColumn("Month", month(col("Date")))
        df = df.withColumn("Weekday", dayofweek(col("Date")))
        df = df.withColumn("Day", dayofmonth(col("Date")))

        return df

    @staticmethod
    def add_cyclical_features(df: DataFrame) -> DataFrame:
        """Add cyclical encoding for temporal features."""
        logger.info("Adding cyclical features...")

        # Month cyclical encoding
        df = df.withColumn(
            "Month_sin", sin(2 * math.pi * col("Month") / CYCLICAL_MONTHS)
        )
        df = df.withColumn(
            "Month_cos", cos(2 * math.pi * col("Month") / CYCLICAL_MONTHS)
        )

        # Weekday cyclical encoding
        df = df.withColumn(
            "Weekday_sin", sin(2 * math.pi * col("Weekday") / CYCLICAL_WEEKDAYS)
        )
        df = df.withColumn(
            "Weekday_cos", cos(2 * math.pi * col("Weekday") / CYCLICAL_WEEKDAYS)
        )

        return df

    @staticmethod
    def encode_categorical_features(df: DataFrame) -> DataFrame:
        """Apply string indexing to categorical variables."""
        logger.info("Encoding categorical features...")

        categorical_vars = [
            "Season",
            "Booking_Channel",
            "Guest_Type",
            "Market_Segment",
            "Guest_Country",
        ]

        for var in categorical_vars:
            try:
                indexer = StringIndexer(inputCol=var, outputCol=f"{var}_idx")
                df = indexer.fit(df).transform(df)
                logger.info(f"Encoded categorical variable: {var}")
            except Exception as e:
                logger.error(f"Error encoding {var}: {e}")

        return df
