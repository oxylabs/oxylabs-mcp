from contextlib import nullcontext as does_not_raise
from unittest.mock import patch

import pytest

from oxylabs_mcp.utils import extract_links_with_text, get_auth_from_env, strip_html


TEST_FIXTURES = "tests/unit/fixtures/"


@pytest.mark.parametrize(
    ("env_vars", "expectation"),
    [
        pytest.param(
            {"OXYLABS_USERNAME": "test_user", "OXYLABS_PASSWORD": "test_pass"},
            does_not_raise(),
            id="valid-env",
        ),
        pytest.param(
            {"OXYLABS_PASSWORD": "test_pass"},
            pytest.raises(ValueError),
            id="no-username",
        ),
        pytest.param(
            {"OXYLABS_USERNAME": "test_user"},
            pytest.raises(ValueError),
            id="no-password",
        ),
        pytest.param({}, pytest.raises(ValueError), id="no-username-and-no-password"),
    ],
)
def test_get_auth_from_env(mocker, env_vars, expectation):
    with expectation, patch("os.environ", new=env_vars):
        get_auth_from_env()


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
