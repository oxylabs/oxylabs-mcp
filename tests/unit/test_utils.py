import re
from unittest.mock import MagicMock, patch

import pytest

from oxylabs_mcp.config import settings
from oxylabs_mcp.utils import (
    _get_default_headers,
    _normalize_client_name,
    extract_links_with_text,
    get_oxylabs_api_token,
    get_oxylabs_auth,
    strip_html,
)


TEST_FIXTURES = "tests/unit/fixtures/"


@pytest.mark.parametrize(
    "env_vars",
    [
        pytest.param(
            {"OXYLABS_USERNAME": "test_user", "OXYLABS_PASSWORD": "test_pass"},
            id="valid-env",
        ),
        pytest.param(
            {"OXYLABS_PASSWORD": "test_pass"},
            id="no-username",
        ),
        pytest.param(
            {"OXYLABS_USERNAME": "test_user"},
            id="no-password",
        ),
        pytest.param({}, id="no-username-and-no-password"),
    ],
)
def test_get_oxylabs_auth(env_vars):
    with patch("os.environ", new=env_vars):
        settings.MCP_TRANSPORT = "stdio"
        username, password = get_oxylabs_auth()
        assert username == env_vars.get("OXYLABS_USERNAME")
        assert password == env_vars.get("OXYLABS_PASSWORD")


@pytest.mark.parametrize(
    ("env_vars", "expected"),
    [
        pytest.param({"OXYLABS_API_TOKEN": "test_token"}, "test_token", id="token-set"),
        pytest.param({"OXYLABS_API_TOKEN": ""}, None, id="token-empty"),
        pytest.param({}, None, id="token-unset"),
    ],
)
def test_get_oxylabs_api_token(env_vars, expected):
    with patch("os.environ", new=env_vars):
        settings.MCP_TRANSPORT = "stdio"
        assert get_oxylabs_api_token() == expected


@pytest.mark.parametrize(
    ("html_input", "expected_output"),
    [pytest.param("before_strip.html", "after_strip.html", id="strip-html")],
)
def test_strip_html(html_input: str, expected_output: str):
    with (
        open(TEST_FIXTURES + html_input, "r", encoding="utf-8") as input_file,
        open(TEST_FIXTURES + expected_output, "r", encoding="utf-8") as output_file,
    ):
        input_html = input_file.read()
        expected_html = output_file.read()

        actual_output = strip_html(input_html)
        assert actual_output == expected_html


@pytest.mark.parametrize(
    ("html_input", "expected_output"),
    [
        pytest.param(
            "with_links.html",
            "[More information...] https://www.iana.org/domains/example\n"
            "[Another link] https://example.com",
            id="strip-html",
        )
    ],
)
def test_extract_links_with_text(html_input: str, expected_output: str):
    with open(TEST_FIXTURES + html_input, "r", encoding="utf-8") as input_file:
        input_html = input_file.read()

        links = extract_links_with_text(input_html)
        assert "\n".join(links) == expected_output


# Same pattern the API uses to parse the header (apiritif pkg/sdk/middleware.go).
API_SDK_HEADER = re.compile(r"([a-z-]+)/(\d+\.\d+\.\d+)(?: ([^()]+?))? \(.*\)")


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        pytest.param("claude-ai", "claude-ai", id="already-normalized"),
        pytest.param("Visual Studio Code", "visual-studio-code", id="spaces-and-case"),
        pytest.param("Claude\r\nCode", "claude-code", id="header-injection"),
        pytest.param("Cursor™", "cursor", id="non-ascii"),
        pytest.param("クライ", None, id="only-non-ascii"),
        pytest.param("  \t ", None, id="blank"),
        pytest.param(None, None, id="missing"),
        pytest.param("a" * 100, "a" * 64, id="too-long"),
    ],
)
def test_normalize_client_name(name, expected):
    assert _normalize_client_name(name) == expected


@pytest.mark.parametrize(
    ("client_name", "sdk_name", "expected"),
    [
        pytest.param(
            "Visual Studio Code",
            "oxylabs-mcp",
            ("oxylabs-mcp", "visual-studio-code"),
            id="local-with-client",
        ),
        pytest.param(
            None, "oxylabs-mcp-remote", ("oxylabs-mcp-remote", None), id="stateless-remote"
        ),
    ],
)
def test_default_headers_match_api_format(client_name, sdk_name, expected):
    context = MagicMock()
    context.request_context.session.client_params.clientInfo.name = client_name

    with (
        patch("oxylabs_mcp.utils.get_context", return_value=context),
        patch.object(settings, "OXYLABS_SDK_NAME", sdk_name),
    ):
        header = _get_default_headers()["x-oxylabs-sdk"]

    match = API_SDK_HEADER.fullmatch(header)
    assert match
    assert (match[1], match[3]) == expected


def test_default_headers_without_request_context():
    with patch("oxylabs_mcp.utils.get_context", side_effect=RuntimeError("no context")):
        header = _get_default_headers()["x-oxylabs-sdk"]

    assert header.startswith("oxylabs-mcp/")
    assert API_SDK_HEADER.fullmatch(header)
