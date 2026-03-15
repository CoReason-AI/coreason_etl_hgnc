# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_hgnc

from io import BytesIO
from unittest.mock import MagicMock

import pytest
import requests
from pytest_mock import MockerFixture

from coreason_etl_hgnc.ingest import stream_hgnc_json


def test_stream_hgnc_json_success(mocker: MockerFixture) -> None:
    # Arrange
    test_url = "https://example.com/hgnc.json"

    # Mock json response containing response.docs array
    json_bytes = b'{"response": {"docs": [{"hgnc_id": "HGNC:5"}, {"hgnc_id": "HGNC:7"}]}}'

    mock_response = MagicMock(spec=requests.Response)
    mock_response.raise_for_status = MagicMock()

    # Need to simulate a raw stream that ijson can consume, and support decode_content
    class MockRaw(BytesIO):
        decode_content: bool = False

    mock_response.raw = MockRaw(json_bytes)

    mock_get = mocker.patch("requests.get", return_value=MagicMock(__enter__=MagicMock(return_value=mock_response)))

    # Act
    genes = list(stream_hgnc_json(test_url))

    # Assert
    mock_get.assert_called_once_with(test_url, stream=True, timeout=30)
    assert mock_response.raise_for_status.called
    assert getattr(mock_response.raw, "decode_content", False) is True

    assert len(genes) == 2
    assert genes[0] == {"hgnc_id": "HGNC:5"}
    assert genes[1] == {"hgnc_id": "HGNC:7"}


def test_stream_hgnc_json_http_error(mocker: MockerFixture) -> None:
    # Arrange
    test_url = "https://example.com/hgnc.json"

    mock_response = MagicMock(spec=requests.Response)
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

    mocker.patch("requests.get", return_value=MagicMock(__enter__=MagicMock(return_value=mock_response)))

    # Act & Assert
    with pytest.raises(requests.HTTPError):
        list(stream_hgnc_json(test_url))


def test_stream_hgnc_json_connection_error(mocker: MockerFixture) -> None:
    # Arrange
    test_url = "https://example.com/hgnc.json"

    mocker.patch("requests.get", side_effect=requests.ConnectionError("Failed to connect"))

    # Act & Assert
    with pytest.raises(requests.ConnectionError):
        list(stream_hgnc_json(test_url))
