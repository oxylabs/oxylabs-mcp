from contextlib import nullcontext as does_not_raise

import pytest
from mcp.server.fastmcp.tools.base import ToolError


QUERY_ONLY = pytest.param(
    {"query": "Generic query"},
    does_not_raise(),
    {"results": [{"content": "Mocked content"}]},
    "Mocked content",
    id="query-only-args",
)
PARSE_ENABLED = pytest.param(
    {"query": "Generic query", "parse": True},
    does_not_raise(),
    {"results": [{"content": '{"data": "value"}'}]},
    '{"data": "value"}',
    id="parse-enabled-args",
)
RENDER_HTML = pytest.param(
    {"query": "Generic query", "render": "html"},
    does_not_raise(),
    {"results": [{"content": "Mocked content"}]},
    "Mocked content",
    id="render-enabled-args",
)
USER_AGENTS = [
    pytest.param(
        {"query": "Generic query", "user_agent_type": "mobile"},
        does_not_raise(),
        {"results": [{"content": "Mocked content"}]},
        "Mocked content",
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
    {"results": [{"content": "Mocked content"}]},
    "Mocked content",
    id="invalid-user-agent-specified-args",
)
START_PAGE_SPECIFIED = pytest.param(
    {"query": "Generic query", "start_page": 2},
    does_not_raise(),
    {"results": [{"content": '{"data": "value"}'}]},
    '{"data": "value"}',
    id="start-page-specified-args",
)
START_PAGE_INVALID = pytest.param(
    {"query": "Generic query", "start_page": -1},
    pytest.raises(ToolError),
    {"results": [{"content": '{"data": "value"}'}]},
    '{"data": "value"}',
    id="start-page-invalid-args",
)
PAGES_SPECIFIED = pytest.param(
    {"query": "Generic query", "pages": 20},
    does_not_raise(),
    {"results": [{"content": '{"data": "value"}'}]},
    '{"data": "value"}',
    id="pages-specified-args",
)
PAGES_INVALID = pytest.param(
    {"query": "Generic query", "pages": -10},
    pytest.raises(ToolError),
    {"results": [{"content": '{"data": "value"}'}]},
    '{"data": "value"}',
    id="pages-invalid-args",
)
LIMIT_SPECIFIED = pytest.param(
    {"query": "Generic query", "limit": 100},
    does_not_raise(),
    {"results": [{"content": '{"data": "value"}'}]},
    '{"data": "value"}',
    id="limit-specified-args",
)
LIMIT_INVALID = pytest.param(
    {"query": "Generic query", "limit": 0},
    pytest.raises(ToolError),
    {"results": [{"content": '{"data": "value"}'}]},
    '{"data": "value"}',
    id="limit-invalid-args",
)
DOMAIN_SPECIFIED = pytest.param(
    {"query": "Generic query", "domain": "io"},
    does_not_raise(),
    {"results": [{"content": '{"data": "value"}'}]},
    '{"data": "value"}',
    id="domain-specified-args",
)
GEO_LOCATION_SPECIFIED = pytest.param(
    {"query": "Generic query", "geo_location": "Miami, Florida"},
    does_not_raise(),
    {"results": [{"content": '{"data": "value"}'}]},
    '{"data": "value"}',
    id="geo-location-specified-args",
)
LOCALE_SPECIFIED = pytest.param(
    {"query": "Generic query", "locale": "ja_JP"},
    does_not_raise(),
    {"results": [{"content": '{"data": "value"}'}]},
    '{"data": "value"}',
    id="locale-specified-args",
)
CATEGORY_SPECIFIED = pytest.param(
    {"query": "Man's T-shirt", "category_id": "QE21R9AV"},
    does_not_raise(),
    {"results": [{"content": '{"data": "value"}'}]},
    '{"data": "value"}',
    id="category-id-specified-args",
)
MERCHANT_ID_SPECIFIED = pytest.param(
    {"query": "Man's T-shirt", "merchant_id": "QE21R9AV"},
    does_not_raise(),
    {"results": [{"content": '{"data": "value"}'}]},
    '{"data": "value"}',
    id="merchant-id-specified-args",
)
CURRENCY_SPECIFIED = pytest.param(
    {"query": "Man's T-shirt", "currency": "USD"},
    does_not_raise(),
    {"results": [{"content": '{"data": "value"}'}]},
    '{"data": "value"}',
    id="currency-specified-args",
)
AUTOSELECT_VARIANT_ENABLED = pytest.param(
    {"query": "B0BVF87BST", "autoselect_variant": True},
    does_not_raise(),
    {"results": [{"content": '{"data": "value"}'}]},
    '{"data": "value"}',
    id="autoselect-variant-enabled-args",
)
