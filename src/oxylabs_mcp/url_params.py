from typing import Annotated, Literal

from pydantic import Field


# Note: optional types (e.g `str | None`) break the introspection in the Cursor AI.
# See: https://github.com/getcursor/cursor/issues/2932
# Therefore, sentinel values (e.g. `""`, `0`) are used to represent a nullable parameter.
URL_PARAM = Annotated[str, Field(description="Website url to scrape.")]
PARSE_PARAM = Annotated[
    bool,
    Field(
        description="Should result be parsed. If the result is not parsed, the output_format parameter is applied.",
    ),
]
RENDER_PARAM = Annotated[
    Literal["", "html"],
    Field(
        description="""
        Whether a headless browser should be used to render the page.
        For example:
            - 'html' when browser is required to render the page.
        """,
        examples=["", "html"],
    ),
]
OUTPUT_FORMAT_PARAM = Annotated[
    Literal[
        "",
        "links",
        "md",
        "html",
    ],
    Field(
        description="""
        The format of the output. Works only when parse parameter is false.
            - links - Most efficient when the goal is navigation or finding specific URLs. Use this first when you need to locate a specific page within a website.
            - md - Best for extracting and reading visible content once you've found the right page. Use this to get structured content that's easy to read and process.
            - html - Should be used sparingly only when you need the raw HTML structure, JavaScript code, or styling information.
        """
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
        "determine User-Agent header value."
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
        description="""
        Domain localization for Google.
        Use country top level domains.
        For example:
            - 'co.uk' for United Kingdom
            - 'us' for United States
            - 'fr' for France
        """,
        examples=["uk", "us", "fr"],
    ),
]
GEO_LOCATION_PARAM = Annotated[
    str,
    Field(
        description="""
        The geographical location that the result should be adapted for.
        Use ISO-3166 country codes.
        Examples:
            - 'California, United States'
            - 'Mexico'
            - 'US' for United States
            - 'DE' for Germany
            - 'FR' for France
        """,
        examples=["US", "DE", "FR"],
    ),
]
LOCALE_PARAM = Annotated[
    str,
    Field(
        description="""
        Set 'Accept-Language' header value which changes your Google search page web interface language.
        Examples:
            - 'en-US' for English, United States
            - 'de-AT' for German, Austria
            - 'fr-FR' for French, France
        """,
        examples=["en-US", "de-AT", "fr-FR"],
    ),
]
AD_MODE_PARAM = Annotated[
    bool,
    Field(
        description="If true will use the Google Ads source optimized for the paid ads.",
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
        description="Currency that will be used to display the prices.",
        examples=["USD", "EUR", "AUD"],
    ),
]
AUTOSELECT_VARIANT_CONTEXT_PARAM = Annotated[
    bool,
    Field(
        description="To get accurate pricing/buybox data, set this parameter to true.",
    ),
]
