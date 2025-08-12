from __future__ import annotations

from pyspark.sql import SparkSession


def get_spark(app_name: str = "mlops-e2e") -> SparkSession:
    """Create or get a SparkSession with Delta Lake enabled."""
    builder = (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
    )
    # Be lenient with warehouse dir so saveAsTable works in local runs
    builder = builder.config("spark.sql.warehouse.dir", "/tmp/spark-warehouse")
    return builder.getOrCreate()
