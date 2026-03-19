# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_hgnc

from datetime import UTC, datetime
from typing import Any

import dlt

from coreason_etl_hgnc.config import settings
from coreason_etl_hgnc.ingest import stream_hgnc_json
from coreason_etl_hgnc.utils.logger import logger


@dlt.resource(  # type: ignore[misc, unused-ignore]
    name="coreason_etl_hgnc_bronze_hgnc_genes_raw",
    write_disposition="replace",
)
def hgnc_resource() -> Any:
    """Resource to ingest HGNC genes from the JSON URL into the Bronze layer."""
    url = str(settings.hgnc_json_url)
    logger.info(f"Yielding genes from HGNC source URL: {url}")

    ingestion_time = datetime.now(tz=UTC)
    for gene in stream_hgnc_json(url):
        yield {
            "ingestion_ts": ingestion_time,
            "raw_data": gene,
        }


@dlt.source(max_table_nesting=0)  # type: ignore[misc, unused-ignore]
def hgnc_source() -> Any:
    """Source configuration for HGNC genes ingestion.

    AGENT INSTRUCTION:
    This function explicitly sets `max_table_nesting=0`. This forces `dlt` to land the nested
    JSON arrays as strings/JSONB, preventing aggressive unpacking into relational child tables.
    """
    return hgnc_resource()


def run_pipeline(
    destination: str | Any = "postgres",
    dataset_name: str = "bronze",
) -> Any:
    """Creates and runs the dlt pipeline for HGNC genes ingestion."""
    pipeline = dlt.pipeline(
        pipeline_name="hgnc_pipeline",
        destination=destination,
        dataset_name=dataset_name,
    )

    logger.info("Running dlt pipeline to ingest HGNC genes...")
    load_info = pipeline.run(hgnc_source())
    logger.info(f"Pipeline run completed: {load_info}")

    return pipeline
