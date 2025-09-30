# mypy: disable-error-code=import-untyped
from oxylabs_ai_studio import client


def setup() -> None:
    """Setups the environment."""
    client._UA_API = "py-mcp"
