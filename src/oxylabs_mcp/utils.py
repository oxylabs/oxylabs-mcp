import os
from lxml.html.clean import Cleaner
from lxml.html import defs, fromstring, tostring
import re
from markdownify import markdownify as md


def get_auth_from_env() -> tuple[str, str]:
    """Gets Username and password from enviroment variables"""
    USERNAME = os.getenv('OXYLABS_USERNAME')
    PASSWORD = os.getenv('OXYLABS_PASSWORD')

    if not USERNAME or not PASSWORD:
        raise ValueError(
            "OXYLABS_USERNAME and OXYLABS_PASSWORD "
            "must be set in the environment variables."
        )
    return USERNAME, PASSWORD


def clean_html(html: str):
    cleaner = Cleaner(
        scripts=True,
        javascript=True,
        style=True,
        remove_tags=[],
        kill_tags=["nav", "svg", "footer", "noscript", "script", "form"],
        safe_attrs=list(defs.safe_attrs) + ["idx"],
        comments=True,
        inline_style=True,
        links=True,
        meta=False,
        page_structure=False,
        embedded=True,
        frames=False,
        forms=False,
        annoying_tags=False,
    )
    return cleaner.clean_html(html)


def strip_html(html: str) -> str:
    """
    Cleans and simplifies an HTML string by removing unwanted elements,
    attributes, and redundant content.

    Args:
        html (str): The input HTML string.

    Returns:
        str: The cleaned and simplified HTML string.
    """
    cleaned_html = clean_html(html)
    html_tree = fromstring(cleaned_html)

    for element in html_tree.iter():
        # Remove style attributes.
        if "style" in element.attrib:
            del element.attrib["style"]

        # Remove elements that have no attributes, no content and no children.
        if (
            (
                not element.attrib
                or (len(element.attrib) == 1 and "idx" in element.attrib)
            )
            and not element.getchildren()
            and (not element.text or not element.text.strip())
            and (not element.tail or not element.tail.strip())
        ):
            parent = element.getparent()
            if parent is not None:
                parent.remove(element)

    # Remove elements with footer and hidden in class or id
    xpath_query = (
        ".//*[contains(@class, 'footer') or contains(@id, 'footer') or "
        "contains(@class, 'hidden') or contains(@id, 'hidden')]")
    elements_to_remove = html_tree.xpath(xpath_query)
    for element in elements_to_remove:
        parent = element.getparent()
        if parent is not None:
            parent.remove(element)

    # Serialize the HTML tree back to a string
    stripped_html = tostring(html_tree, encoding="unicode")
    # Previous cleaning produces empty spaces.
    # Replace multiple spaces with an single one
    stripped_html = re.sub(r"\s{2,}", " ", stripped_html)
    # Replace consecutive newlines with an empty string
    stripped_html = re.sub(r"\n{2,}", "", stripped_html)
    return stripped_html


def convert_html_to_md(html: str) -> str:
    return md(html)
