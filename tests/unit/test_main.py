from unittest.mock import patch

import pytest

from oxylabs_mcp import main


@pytest.mark.parametrize(
    ("oxylabs_credentials", "ai_studio_key", "should_call_run"),
    [
        pytest.param(False, False, False, id="no-credentials"),
        pytest.param(True, False, True, id="oxylabs-credentials-only"),
        pytest.param(False, True, True, id="ai-studio-key-only"),
        pytest.param(True, True, True, id="both-credentials"),
    ],
)
def test_main_credential_validation(oxylabs_credentials, ai_studio_key, should_call_run):
    """Test that main() validates credentials before starting the server."""
    with (
        patch(
            "oxylabs_mcp.server.is_oxylabs_credentials_available", return_value=oxylabs_credentials
        ),
        patch("oxylabs_mcp.server.is_ai_studio_api_key_available", return_value=ai_studio_key),
        patch("oxylabs_mcp.server.mcp.run") as mock_run,
    ):

        if should_call_run:
            # If credentials are available, main() should call mcp.run()
            main()
            mock_run.assert_called_once()
        else:
            # If no credentials, main() should raise ValueError before calling mcp.run()
            with pytest.raises(ValueError):
                main()
            mock_run.assert_not_called()


def test_main_no_credentials_error_message():
    """Test that main() raises a specific error message when no credentials are provided."""
    with (
        patch("oxylabs_mcp.server.is_oxylabs_credentials_available", return_value=False),
        patch("oxylabs_mcp.server.is_ai_studio_api_key_available", return_value=False),
    ):

        with pytest.raises(ValueError) as exc_info:
            main()

        error_message = str(exc_info.value)
        assert "Oxylabs credentials not set" in error_message
        assert "OXYLABS_USERNAME" in error_message
        assert "OXYLABS_PASSWORD" in error_message
        assert "OXYLABS_AI_STUDIO_API_KEY" in error_message
