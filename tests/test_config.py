import os

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from coreason_etl_hgnc.config import Settings


def test_settings_default() -> None:
    settings = Settings()
    assert (
        str(settings.hgnc_json_url)
        == "https://storage.googleapis.com/public-download-files/hgnc/json/json/hgnc_complete_set.json"
    )


@given(  # type: ignore[misc]
    test_url=st.from_regex(r"^https?://[a-z0-9.-]+\.[a-z]{2,}(?:/[a-zA-Z0-9_-]+)*$", fullmatch=True).map(
        lambda u: u if u.endswith("/") or u.count("/") > 2 else u + "/"
    )
)
def test_settings_env_override_hypothesis(test_url: str) -> None:
    original = os.environ.get("COREASON_ETL_HGNC_HGNC_JSON_URL")
    os.environ["COREASON_ETL_HGNC_HGNC_JSON_URL"] = test_url
    try:
        settings = Settings()
        assert str(settings.hgnc_json_url) == test_url
    finally:
        if original is None:
            del os.environ["COREASON_ETL_HGNC_HGNC_JSON_URL"]
        else:
            os.environ["COREASON_ETL_HGNC_HGNC_JSON_URL"] = original


@given(  # type: ignore[misc]
    test_url=st.text().filter(
        lambda x: not x.startswith("http://") and not x.startswith("https://") and "\x00" not in x
    )
)
def test_settings_invalid_url_hypothesis(test_url: str) -> None:
    original = os.environ.get("COREASON_ETL_HGNC_HGNC_JSON_URL")
    os.environ["COREASON_ETL_HGNC_HGNC_JSON_URL"] = test_url
    try:
        with pytest.raises(ValidationError):
            Settings()
    finally:
        if original is None:
            del os.environ["COREASON_ETL_HGNC_HGNC_JSON_URL"]
        else:
            os.environ["COREASON_ETL_HGNC_HGNC_JSON_URL"] = original
