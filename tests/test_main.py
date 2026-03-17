# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_hgnc


from pytest_mock import MockerFixture

from coreason_etl_hgnc.main import HgncIngestionIntent, main


def test_hgnc_ingestion_intent_execute(mocker: MockerFixture) -> None:
    """Verifies that HgncIngestionIntent executes the pipeline."""
    mock_run_pipeline = mocker.patch("coreason_etl_hgnc.main.run_pipeline")
    mock_logger = mocker.patch("coreason_etl_hgnc.main.logger")

    intent = HgncIngestionIntent()
    intent.execute()

    mock_run_pipeline.assert_called_once()
    mock_logger.info.assert_called_with("Executing HgncIngestionIntent")


def test_main(mocker: MockerFixture) -> None:
    """Verifies that the main entry point works correctly."""
    mock_execute = mocker.patch.object(HgncIngestionIntent, "execute")
    main()
    mock_execute.assert_called_once()
