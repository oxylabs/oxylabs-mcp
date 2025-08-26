from unittest.mock import patch

import pytest

from oxylabs_mcp.config import settings
from oxylabs_mcp.utils import extract_links_with_text, get_oxylabs_auth, strip_html


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
    with (open(TEST_FIXTURES + html_input, "r", encoding="utf-8") as input_file,):
        input_html = input_file.read()

        links = extract_links_with_text(input_html)
        assert "\n".join(links) == expected_output
