from typing import Annotated, Literal

from pydantic import Field


# Note: optional types (e.g `str | None`) break the introspection in the Cursor AI.
# See: https://github.com/getcursor/cursor/issues/2932
# Therefore, sentinel values (e.g. `""`, `0`) are used to represent a nullable parameter.
URL_PARAM = Annotated[str, Field(description="Url to scrape with web scraper.")]
PARSE_PARAM = Annotated[
    bool,
    Field(
        description="Should result be parsed. "
        "If result should not be parsed then html "
        "will be stripped and converted to markdown file."
    ),
]
RENDER_PARAM = Annotated[
    Literal["", "html"],
    Field(
        description="Whether a headless browser should be used "
        "to render the page. See: "
        "https://developers.oxylabs.io/scraper-apis"
        "/web-scraper-api/features/javascript-rendering "
        "`html` will return rendered html page "
        "`None` will not use render for scraping."
    ),
]
GOOGLE_QUERY_PARAM = Annotated[str, Field(description="URL-encoded keyword to search for.")]
AMAZON_SEARCH_QUERY_PARAM = Annotated[str, Field(description="Keyword to search for.")]
USER_AGENT_TYPE_PARAM = Annotated[
    Literal[
        "",
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
    ],
    Field(
        description="Device type and browser that will be used to "
        "determine User-Agent header value. "
        "See: https://developers.oxylabs.io/scraper-apis"
        "/web-scraper-api/features/user-agent-type"
    ),
]
START_PAGE_PARAM = Annotated[
    int,
    Field(description="Starting page number."),
]
PAGES_PARAM = Annotated[
    int,
    Field(description="Number of pages to retrieve."),
]
LIMIT_PARAM = Annotated[
    int,
    Field(description="Number of results to retrieve in each page."),
]
DOMAIN_PARAM = Annotated[
    str,
    Field(
        description="Domain localization for Google. See: "
        "https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com"
        "/o/spaces%2FiwDdoZGfMbUe5cRL2417%2Fuploads%2FS6e9iUtXb5YkRLlfQdm6%2F"
        "locale.json?alt=media&token=435886ac-6223-42d4-8204-1e7d53512a42"
    ),
]
GEO_LOCATION_PARAM = Annotated[
    str,
    Field(
        description="The geographical location that the result should be adapted "
        "for. See: https://developers.oxylabs.io/scraper-apis/web-scraper-api"
        "/features/serp-localization#google"
    ),
]
LOCALE_PARAM = Annotated[
    str,
    Field(
        description="'Accept-Language' header value which changes your Google "
        "search page web interface language. See: https://developers.oxylabs.io/"
        "scraper-apis/web-scraper-api/features/domain-locale-results-language"
        "#locale-1"
    ),
]
AD_MODE_PARAM = Annotated[
    bool,
    Field(
        description="If true will use the Google Ads source optimized for the "
        "paid ads. See: https://developers.oxylabs.io/scraper-apis"
        "/web-scraper-api/google/ads"
    ),
]
CATEGORY_ID_CONTEXT_PARAM = Annotated[
    str,
    Field(
        description="Search for items in a particular browse node (product category).",
    ),
]
MERCHANT_ID_CONTEXT_PARAM = Annotated[
    str,
    Field(
        description="Search for items sold by a particular seller.",
    ),
]
CURRENCY_CONTEXT_PARAM = Annotated[
    str,
    Field(
        description="Currency that will be used to display the prices. "
        "See: https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com"
        "/o/spaces%2FzrXw45naRpCZ0Ku9AjY1%2Fuploads%2FIAHLazcDOwZSiZ6s8IJt"
        "%2FAmazon_search_currency_values.json?alt=media"
        "&token=b72b5c4d-3820-42a6-8e74-78ea6b44e93f",
        examples=["USD", "EUR", "AUD"],
    ),
]
AUTOSELECT_VARIANT_CONTEXT_PARAM = Annotated[
    bool,
    Field(
        description="To get accurate pricing/buybox data, set this parameter "
        "to true (which tells us to append the th=1&psc=1 "
        "URL parameters to the end of the product URL).",
    ),
]
