import importlib
import sys

from pytest_mock import MockerFixture


def test_logger_initialization(mocker: MockerFixture) -> None:
    """Test logger initialization and directory creation."""
    # Ensure any previous load is removed so we re-execute module level code
    if "coreason_etl_hgnc.utils.logger" in sys.modules:
        del sys.modules["coreason_etl_hgnc.utils.logger"]

    mock_path_exists = mocker.patch("coreason_etl_hgnc.utils.logger.Path.exists", return_value=False)
    mock_path_mkdir = mocker.patch("coreason_etl_hgnc.utils.logger.Path.mkdir")

    import coreason_etl_hgnc.utils.logger

    importlib.reload(coreason_etl_hgnc.utils.logger)

    mock_path_exists.assert_called()
    mock_path_mkdir.assert_called_with(parents=True, exist_ok=True)
