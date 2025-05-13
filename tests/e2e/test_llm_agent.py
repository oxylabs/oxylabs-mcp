import json
import os
from contextlib import asynccontextmanager

import pytest
from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools


MCP_SERVER = "local"  # local, uvx
MODELS_CONFIG = [
    ("GOOGLE_API_KEY", "gemini"),
    # ("OPENAI_API_KEY", "openai"),
]


def get_agent(model: str, oxylabs_mcp: MCPTools) -> Agent:
    if model == "gemini":
        model_ = Gemini(api_key=os.getenv("GOOGLE_API_KEY"))
    elif model == "openai":
        model_ = OpenAIChat(api_key=os.getenv("OPENAI_API_KEY"))
    else:
        raise ValueError(f"Unknown model: {model}")

    return Agent(
        model=model_,
        tools=[oxylabs_mcp],
        instructions=["Use MCP tools to fulfil the requests"],
        markdown=True,
    )


def get_models() -> list[str]:
    models = []

    for env_var, model_name in MODELS_CONFIG:
        if os.getenv(env_var):
            models.append(model_name)

    return models


@asynccontextmanager
async def oxylabs_mcp_server():
    if MCP_SERVER == "local":
        command = f"uv run --directory {os.getenv('LOCAL_OXYLABS_MCP_DIRECTORY')} oxylabs-mcp"
    elif MCP_SERVER == "uvx":
        command = "uvx oxylabs-mcp"
    else:
        raise ValueError(f"Unknown mcp server option: {MCP_SERVER}")

    async with MCPTools(
        command,
        env={
            "OXYLABS_USERNAME": os.getenv("OXYLABS_USERNAME"),
            "OXYLABS_PASSWORD": os.getenv("OXYLABS_PASSWORD"),
        },
    ) as mcp_server:
        yield mcp_server


@pytest.mark.skipif(not os.getenv("OXYLABS_USERNAME"), reason="`OXYLABS_USERNAME` is not set")
@pytest.mark.skipif(not os.getenv("OXYLABS_PASSWORD"), reason="`OXYLABS_PASSWORD` is not set")
@pytest.mark.asyncio
@pytest.mark.parametrize("model", get_models())
@pytest.mark.parametrize(
    ("query", "tool", "arguments", "expected_content"),
    [
        (
            "Search for iPhone 16 in google with parsed result",
            "google_search_scraper",
            {
                "query": "iPhone 16",
                "parse": True,
            },
            "iPhone 16",
        ),
        (
            "Search for iPhone 16 in google with render html",
            "google_search_scraper",
            {
                "query": "iPhone 16",
                "render": "html",
            },
            "iPhone 16",
        ),
        (
            "Search for iPhone 16 in google with browser rendering",
            "google_search_scraper",
            {
                "query": "iPhone 16",
                "render": "html",
            },
            "iPhone 16",
        ),
        (
            "Search for iPhone 16 in google with user agent type mobile",
            "google_search_scraper",
            {
                "query": "iPhone 16",
                "user_agent_type": "mobile",
            },
            "iPhone 16",
        ),
        (
            "Search for iPhone 16 in google starting from the second page",
            "google_search_scraper",
            {
                "query": "iPhone 16",
                "start_page": 2,
            },
            "iPhone 16",
        ),
        (
            "Search for iPhone 16 in google with United Kingdom domain",
            "google_search_scraper",
            {
                "query": "iPhone 16",
                "domain": "co.uk",
            },
            "iPhone 16",
        ),
        (
            "Search for iPhone 16 in google with Brazil geolocation",
            "google_search_scraper",
            {
                "query": "iPhone 16",
                "geo_location": "BR",
            },
            "iPhone 16",
        ),
        (
            "Search for iPhone 16 in google with French locale",
            "google_search_scraper",
            {
                "query": "iPhone 16",
                "locale": "fr-FR",
            },
            "iPhone 16",
        ),
    ],
)
async def test_basic_agent_prompts(
    model: str,
    query: str,
    tool: str,
    arguments: dict,
    expected_content: str,
):
    async with oxylabs_mcp_server() as mcp_server:
        agent = get_agent(model, mcp_server)
        response = await agent.arun(query)

    tool_calls = agent.memory.get_tool_calls(agent.session_id)

    # [tool_call, tool_call_result]
    assert len(tool_calls) == 2, "Extra tool calls found!"

    assert tool_calls[0]["function"]["name"] == tool
    assert json.loads(tool_calls[0]["function"]["arguments"]) == arguments

    assert expected_content in response.content


@pytest.mark.asyncio
@pytest.mark.parametrize("model", get_models())
async def test_complex_agent_prompt(model: str):
    async with oxylabs_mcp_server() as mcp_server:
        agent = get_agent(model, mcp_server)

        await agent.arun(
            "Go to oxylabs.io, look for career page, "
            "go to it and return all job titles in markdown format. "
            "Don't invent URLs, start from one provided."
        )

    tool_calls = agent.memory.get_tool_calls(agent.session_id)
    assert len(tool_calls) == 4, f"Not enough tool_calls, got {len(tool_calls)}: {tool_calls}"

    oxylabs_page_call, _, careers_page_call, _ = agent.memory.get_tool_calls(agent.session_id)
    assert oxylabs_page_call["function"]["name"] == "universal_scraper"
    assert json.loads(oxylabs_page_call["function"]["arguments"]) == {
        "output_format": "links",
        "url": "https://oxylabs.io",
    }
    assert careers_page_call["function"]["name"] == "universal_scraper"
    assert json.loads(careers_page_call["function"]["arguments"]) == {
        "output_format": "md",
        "url": "https://career.oxylabs.io/",
    }
