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
from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from coreason_etl_hgnc.pipeline import hgnc_resource, hgnc_source, run_pipeline


def test_hgnc_resource(mocker: MockerFixture) -> None:
    # Arrange
    test_genes = [{"hgnc_id": "HGNC:5"}, {"hgnc_id": "HGNC:7"}]
    mock_stream = mocker.patch("coreason_etl_hgnc.pipeline.stream_hgnc_json", return_value=iter(test_genes))
    mock_settings = mocker.patch("coreason_etl_hgnc.pipeline.settings")
    mock_settings.hgnc_json_url = "https://example.com/hgnc.json"

    mock_now = datetime(2025, 1, 1, tzinfo=UTC)
    mock_datetime = mocker.patch("coreason_etl_hgnc.pipeline.datetime")
    mock_datetime.now.return_value = mock_now

    # Act
    # Since it's a DltResource, we can iterate over it to get the yielded items
    result = list(hgnc_resource())

    # Assert
    mock_stream.assert_called_once_with("https://example.com/hgnc.json")
    assert len(result) == 2
    assert result[0] == {"ingestion_ts": mock_now, "raw_data": {"hgnc_id": "HGNC:5"}}
    assert result[1] == {"ingestion_ts": mock_now, "raw_data": {"hgnc_id": "HGNC:7"}}


def test_hgnc_source_max_table_nesting() -> None:
    # Act
    source = hgnc_source()

    # Assert
    # Verify that the max_table_nesting config is set to 0
    assert source.max_table_nesting == 0
    # The source should contain the 'bronze_hgnc_genes_raw' resource
    assert "bronze_hgnc_genes_raw" in source.resources


def test_run_pipeline(mocker: MockerFixture) -> None:
    # Arrange
    mock_pipeline_run = MagicMock(return_value="LoadInfoMock")
    mock_pipeline_instance = MagicMock()
    mock_pipeline_instance.run = mock_pipeline_run

    mock_dlt_pipeline = mocker.patch("dlt.pipeline", return_value=mock_pipeline_instance)
    mock_hgnc_source = mocker.patch("coreason_etl_hgnc.pipeline.hgnc_source", return_value="SourceMock")

    # Act
    pipeline = run_pipeline(destination="duckdb", dataset_name="test_dataset")

    # Assert
    mock_dlt_pipeline.assert_called_once_with(
        pipeline_name="hgnc_pipeline",
        destination="duckdb",
        dataset_name="test_dataset",
    )
    mock_hgnc_source.assert_called_once()
    mock_pipeline_run.assert_called_once_with("SourceMock")
    assert pipeline == mock_pipeline_instance


def test_run_pipeline_default_args(mocker: MockerFixture) -> None:
    # Arrange
    mock_pipeline_run = MagicMock(return_value="LoadInfoMock")
    mock_pipeline_instance = MagicMock()
    mock_pipeline_instance.run = mock_pipeline_run

    mock_dlt_pipeline = mocker.patch("dlt.pipeline", return_value=mock_pipeline_instance)
    mock_hgnc_source = mocker.patch("coreason_etl_hgnc.pipeline.hgnc_source", return_value="SourceMock")

    # Act
    pipeline = run_pipeline()

    # Assert
    mock_dlt_pipeline.assert_called_once_with(
        pipeline_name="hgnc_pipeline",
        destination="postgres",
        dataset_name="bronze_hgnc",
    )
    mock_hgnc_source.assert_called_once()
    mock_pipeline_run.assert_called_once_with("SourceMock")
    assert pipeline == mock_pipeline_instance
