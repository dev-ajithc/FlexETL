"""
Main entry point for FlexETL pipeline.

Phase 1: Basic ETL with hardcoded parameters for sales data aggregation.
"""

import logging
import sys
from pathlib import Path

from flexetl.extractor import CSVExtractor
from flexetl.transformer import DataTransformer
from flexetl.loader import SQLiteLoader


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('output/pipeline.log', mode='a')
    ]
)

logger = logging.getLogger(__name__)


def main() -> int:
    """
    Execute the ETL pipeline for sales data aggregation.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    try:
        logger.info("=" * 60)
        logger.info("FlexETL Pipeline v0.1.0 - Phase 1 MVP")
        logger.info("=" * 60)

        Path("output").mkdir(exist_ok=True)

        logger.info("Step 1: Extract data from CSV")
        extractor = CSVExtractor("data/sales_data.csv")
        raw_data = extractor.extract()
        logger.info(f"Extracted {len(raw_data)} records")

        logger.info("Step 2: Transform data")
        transformer = DataTransformer(raw_data)

        transformed_data = (
            transformer
            .filter_nulls(['product_id', 'quantity', 'unit_price'])
            .filter_by_value('quantity', '>', 0)
            .calculate_revenue('quantity', 'unit_price', 'revenue')
        )

        result_df = transformed_data.get_result()

        aggregated = (
            DataTransformer(result_df)
            .aggregate(
                group_by=['date', 'product_id', 'product_name'],
                aggregations={
                    'total_quantity': 'sum(quantity)',
                    'total_revenue': 'sum(revenue)'
                }
            )
            .get_result()
        )

        logger.info(f"Transformed to {len(aggregated)} aggregated records")

        logger.info("Step 3: Load data to SQLite")
        loader = SQLiteLoader(
            database_path="output/sales.db",
            table_name="daily_product_revenue",
            if_exists="replace"
        )

        rows_loaded = loader.load(aggregated)

        verified_count = loader.verify_load()

        logger.info("=" * 60)
        logger.info("Pipeline completed successfully!")
        logger.info(f"Records processed: {len(raw_data)}")
        logger.info(f"Records after transformation: {len(result_df)}")
        logger.info(f"Aggregated records: {len(aggregated)}")
        logger.info(f"Records loaded: {rows_loaded}")
        logger.info(f"Records verified: {verified_count}")
        logger.info("=" * 60)

        return 0

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return 1
    except Exception as e:
        logger.exception(f"Pipeline failed with error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
