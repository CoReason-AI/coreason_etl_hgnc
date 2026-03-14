import pytest
from pydantic import ValidationError

from coreason_etl_hgnc.config import Settings


def test_settings_default() -> None:
    settings = Settings()
    assert (
        str(settings.hgnc_json_url)
        == "https://storage.googleapis.com/public-download-files/hgnc/json/json/hgnc_complete_set.json"
    )


def test_settings_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    test_url = "https://example.com/hgnc.json"
    monkeypatch.setenv("COREASON_ETL_HGNC_HGNC_JSON_URL", test_url)
    settings = Settings()
    assert str(settings.hgnc_json_url) == test_url


def test_settings_invalid_url(monkeypatch: pytest.MonkeyPatch) -> None:
    test_url = "not-a-valid-url"
    monkeypatch.setenv("COREASON_ETL_HGNC_HGNC_JSON_URL", test_url)
    with pytest.raises(ValidationError):
        Settings()
