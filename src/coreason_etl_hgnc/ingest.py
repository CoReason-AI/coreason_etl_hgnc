# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_hgnc

from collections.abc import Iterator
from typing import Any

import ijson
import requests

from coreason_etl_hgnc.utils.logger import logger


def stream_hgnc_json(url: str) -> Iterator[dict[str, Any]]:
    """Yields individual gene objects from the nested HGNC JSON response.

    AGENT INSTRUCTION:
    This function strictly adheres to the Clean Room Concept by executing the API request
    and yielding the raw JSON objects from the nested `response.docs` array via `ijson`.
    It enforces urllib3's transparent gzip decoding.
    """
    logger.info(f"Initiating stream from: {url}")
    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            # Ensure urllib3 transparently decodes gzip/deflate compressed streams
            r.raw.decode_content = True

            # The target array is located at response -> docs -> item
            genes = ijson.items(r.raw, "response.docs.item")
            yield from genes
    except Exception:
        logger.exception("Failed to stream HGNC JSON")
        raise
