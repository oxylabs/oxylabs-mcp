from contextlib import nullcontext as does_not_raise

import pytest
from fastmcp.exceptions import ToolError


JOB_RESPONSE = {"id": "7333092420940211201", "status": "done"}
STR_RESPONSE = {
    "results": [{"content": "Mocked content"}],
    "job": JOB_RESPONSE,
}
JSON_RESPONSE = {
    "results": [{"content": {"data": "value"}}],
    "job": JOB_RESPONSE,
}

QUERY_ONLY = pytest.param(
    {"query": "Generic query"},
    does_not_raise(),
    STR_RESPONSE,
    "\n\nMocked content\n\n",
    id="query-only-args",
)
PARSE_ENABLED = pytest.param(
    {"query": "Generic query", "parse": True},
    does_not_raise(),
    JSON_RESPONSE,
    '{"data": "value"}',
    id="parse-enabled-args",
)
RENDER_HTML_WITH_QUERY = pytest.param(
    {"query": "Generic query", "render": "html"},
    does_not_raise(),
    STR_RESPONSE,
    "\n\nMocked content\n\n",
    id="render-enabled-args",
)
RENDER_INVALID_WITH_QUERY = pytest.param(
    {"query": "Generic query", "render": "png"},
    pytest.raises(ToolError),
    STR_RESPONSE,
    None,
    id="render-enabled-args",
)
OUTPUT_FORMATS = [
    pytest.param(
        {"query": "Generic query", "output_format": "links"},
        does_not_raise(),
        {
            "results": [
                {
                    "content": '<html><body><div><p><a href="https://example.com">link</a></p></div></body></html>'
                }
            ],
            "job": JOB_RESPONSE,
        },
        "[link] https://example.com",
        id="links-output-format-args",
    ),
    pytest.param(
        {"query": "Generic query", "output_format": "md"},
        does_not_raise(),
        STR_RESPONSE,
        "\n\nMocked content\n\n",
        id="md-output-format-args",
    ),
    pytest.param(
        {"query": "Generic query", "output_format": "html"},
        does_not_raise(),
        STR_RESPONSE,
        "Mocked content",
        id="html-output-format-args",
    ),
]
USER_AGENTS_WITH_QUERY = [
    pytest.param(
        {"query": "Generic query", "user_agent_type": uat},
        does_not_raise(),
        STR_RESPONSE,
        "\n\nMocked content\n\n",
        id=f"{uat}-user-agent-specified-args",
    )
    for uat in [
        "desktop",
        "desktop_chrome",
        "desktop_firefox",
        "desktop_safari",
        "desktop_edge",
        "desktop_opera",
        "mobile",
        "mobile_ios",
        "mobile_android",
        "tablet",
    ]
]
USER_AGENTS_WITH_URL = [
    pytest.param(
        {"url": "https://example.com", "user_agent_type": uat},
        does_not_raise(),
        STR_RESPONSE,
        "\n\nMocked content\n\n",
        id=f"{uat}-user-agent-specified-args",
    )
    for uat in [
        "desktop",
        "desktop_chrome",
        "desktop_firefox",
        "desktop_safari",
        "desktop_edge",
        "desktop_opera",
        "mobile",
        "mobile_ios",
        "mobile_android",
        "tablet",
    ]
]
INVALID_USER_AGENT = pytest.param(
    {"query": "Generic query", "user_agent_type": "invalid"},
    pytest.raises(ToolError),
    STR_RESPONSE,
    "Mocked content",
    id="invalid-user-agent-specified-args",
)
START_PAGE_SPECIFIED = pytest.param(
    {"query": "Generic query", "start_page": 2},
    does_not_raise(),
    JSON_RESPONSE,
    '{"data": "value"}',
    id="start-page-specified-args",
)
START_PAGE_INVALID = pytest.param(
    {"query": "Generic query", "start_page": -1},
    pytest.raises(ToolError),
    JSON_RESPONSE,
    '{"data": "value"}',
    id="start-page-invalid-args",
)
PAGES_SPECIFIED = pytest.param(
    {"query": "Generic query", "pages": 20},
    does_not_raise(),
    JSON_RESPONSE,
    '{"data": "value"}',
    id="pages-specified-args",
)
PAGES_INVALID = pytest.param(
    {"query": "Generic query", "pages": -10},
    pytest.raises(ToolError),
    JSON_RESPONSE,
    '{"data": "value"}',
    id="pages-invalid-args",
)
LIMIT_SPECIFIED = pytest.param(
    {"query": "Generic query", "limit": 100},
    does_not_raise(),
    JSON_RESPONSE,
    '{"data": "value"}',
    id="limit-specified-args",
)
LIMIT_INVALID = pytest.param(
    {"query": "Generic query", "limit": 0},
    pytest.raises(ToolError),
    JSON_RESPONSE,
    '{"data": "value"}',
    id="limit-invalid-args",
)
DOMAIN_SPECIFIED = pytest.param(
    {"query": "Generic query", "domain": "io"},
    does_not_raise(),
    JSON_RESPONSE,
    '{"data": "value"}',
    id="domain-specified-args",
)
GEO_LOCATION_SPECIFIED_WITH_QUERY = pytest.param(
    {"query": "Generic query", "geo_location": "Miami, Florida"},
    does_not_raise(),
    JSON_RESPONSE,
    '{"data": "value"}',
    id="geo-location-specified-args",
)
GEO_LOCATION_SPECIFIED_WITH_URL = pytest.param(
    {"url": "https://example.com", "geo_location": "Miami, Florida"},
    does_not_raise(),
    STR_RESPONSE,
    "\n\nMocked content\n\n",
    id="geo-location-specified-args",
)
LOCALE_SPECIFIED = pytest.param(
    {"query": "Generic query", "locale": "ja_JP"},
    does_not_raise(),
    JSON_RESPONSE,
    '{"data": "value"}',
    id="locale-specified-args",
)
CATEGORY_SPECIFIED = pytest.param(
    {"query": "Man's T-shirt", "category_id": "QE21R9AV"},
    does_not_raise(),
    JSON_RESPONSE,
    '{"data": "value"}',
    id="category-id-specified-args",
)
MERCHANT_ID_SPECIFIED = pytest.param(
    {"query": "Man's T-shirt", "merchant_id": "QE21R9AV"},
    does_not_raise(),
    JSON_RESPONSE,
    '{"data": "value"}',
    id="merchant-id-specified-args",
)
CURRENCY_SPECIFIED = pytest.param(
    {"query": "Man's T-shirt", "currency": "USD"},
    does_not_raise(),
    JSON_RESPONSE,
    '{"data": "value"}',
    id="currency-specified-args",
)
AUTOSELECT_VARIANT_ENABLED = pytest.param(
    {"query": "B0BVF87BST", "autoselect_variant": True},
    does_not_raise(),
    JSON_RESPONSE,
    '{"data": "value"}',
    id="autoselect-variant-enabled-args",
)
URL_ONLY = pytest.param(
    {"url": "https://example.com"},
    does_not_raise(),
    STR_RESPONSE,
    "\n\nMocked content\n\n",
    id="url-only-args",
)
NO_URL = pytest.param(
    {},
    pytest.raises(ToolError),
    STR_RESPONSE,
    "\n\nMocked content\n\n",
    id="no-url-args",
)
RENDER_HTML_WITH_URL = pytest.param(
    {"url": "https://example.com", "render": "html"},
    does_not_raise(),
    STR_RESPONSE,
    "\n\nMocked content\n\n",
    id="render-enabled-args",
)
RENDER_INVALID_WITH_URL = pytest.param(
    {"url": "https://example.com", "render": "png"},
    pytest.raises(ToolError),
    JSON_RESPONSE,
    None,
    id="render-enabled-args",
)
