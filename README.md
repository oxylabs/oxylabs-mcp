# MCP Server for Oxylabs Scraper
[![smithery badge](https://smithery.ai/badge/@oxylabs/oxylabs-mcp)](https://smithery.ai/server/@oxylabs/oxylabs-mcp)

The scraper tool is an asynchronous utility that leverages the Oxylabs Web Scraper API to fetch and process content from a given URL. This tool is designed to handle various scraping scenarios efficiently, with flexible options for parsing and rendering web pages.

## Key Features

1. **URL Scraping**
    - Fetches the content of a specified URL using Oxylabs' API.

2. **HTML Parsing**
    - If parsing is enabled, the content is returned in a processed format, suitable for handling by downstream systems like language models (LLMs).
    - If parsing is disabled, the tool strips unnecessary HTML tags and converts the cleaned content into a Markdown file for easier readability and compatibility.

3. **JavaScript Rendering**
    - Offers an option to render pages using a headless browser, which ensures dynamic content (e.g., JavaScript-rendered pages) is included in the output.
    - Supports the html rendering option or skipping rendering entirely.

## Examples on how to query Claude or other LLM
- Could you scrape https://oxylabs.io page?
- Scrape https://www.amazon.de/-/en/Smartphone-Contract-Function-Manufacturer-Exclusive/dp/B0CNKD651V with parse enabled.
- Scrape https://www.amazon.de/-/en/gp/bestsellers/beauty/ref=zg_bs_nav_beauty_0 with parse and render enabled.

## Prerequisites
### Install uv first.
https://docs.astral.sh/uv/getting-started/installation/#installation-methods

## Setup Intructions

### Installing via Smithery

To install Oxylabs MCP server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@oxylabs/oxylabs-mcp):

```bash
npx -y @smithery/cli install @oxylabs/oxylabs-mcp --client claude
```


### Setup with Claude Desktop
```json
# claude_desktop_config.json
# Can find location through:
# Claude -> Settings -> Developer -> Edit Config
{
  "mcpServers": {
    "oxylabs_scraper": {
      "command": "uvx",
      "args": ["oxylabs-mcp"],
      "env": {
        "OXYLABS_USERNAME": "YOUR_USERNAME_HERE",
        "OXYLABS_PASSWORD": "YOUR_PASSWORD_HERE",
      }
    }
  }
}
```

## Local/Dev Setup Instructions
### Clone repo
`git clone <git:url>`
### Install dependencies
Install MCP server dependencies:
```bash
cd mcp-server-oxylabs

# Create virtual environment and activate it
uv venv

source .venv/bin/activate # MacOS/Linux
# OR
.venv/Scripts/activate # Windows

# Install dependencies
uv sync
```
### Setup with Claude Desktop
```json
# claude_desktop_config.json
# Can find location through:
# Claude -> Settings -> Developer -> Edit Config
{
  "mcpServers": {
    "oxylabs_scraper": {
      "command": "uv",
      "args": [
        "--directory",
        "/<Absolute-path-to-folder>/oxylabs-mcp",
        "run",
        "oxylabs-mcp"
      ],
      "env": {
        "OXYLABS_USERNAME": "YOUR_USERNAME_HERE",
        "OXYLABS_PASSWORD": "YOUR_PASSWORD_HERE"
      }
    }
  }
}
```

### Debugging
Run:
```bash
make run
```
Then access MCP Inspector at `http://localhost:5173`. You may need to add your username and password in the environment variables in the inspector under `OXYLABS_USERNAME` and `OXYLABS_PASSWORD`.

---
**NOTE**

Usage with the MCP inspector is affected by an ongoing issue with the Python SDK for MCP, see: https://github.com/modelcontextprotocol/python-sdk/pull/85. For Claude, a forked version of the SDK is used as a temporary fix.

---