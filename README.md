# MCP Server for Oxylabs Scraper
[![smithery badge](https://smithery.ai/badge/@oxylabs/oxylabs-mcp)](https://smithery.ai/server/@oxylabs/oxylabs-mcp)

The scraper tool is an asynchronous utility that leverages the Oxylabs Web Scraper API to fetch and process content from a given URL. This tool is designed to handle various scraping scenarios efficiently, with flexible options for parsing and rendering web pages.

## Key Features

- Web scraping with advanced HTML parsing and conversion
- JavaScript rendering with headless browser support
- Dynamic content extraction from JS-heavy websites
- URL-specific content targeting and extraction
- Automated HTML cleaning and markdown conversion
- Smart content parsing for LLM compatibility
- Flexible rendering options (full JS, HTML-only, or none)
- Mobile/Desktop viewport emulation
- High success rate on complex and protected websites
- Proxy rotation and IP geolocation capabilities
- Comprehensive error handling and reporting
- Cross-platform compatibility with customizable options
- Support for batch processing of multiple URLs
- Intelligent rate limiting and request management
- Seamless integration with AI models and analytics tools

## Examples on how to query Claude or other LLM
- Could you scrape https://oxylabs.io page?
- Scrape https://www.amazon.de/-/en/Smartphone-Contract-Function-Manufacturer-Exclusive/dp/B0CNKD651V with parse enabled.
- Scrape https://www.amazon.de/-/en/gp/bestsellers/beauty/ref=zg_bs_nav_beauty_0 with parse and render enabled.
- Use web unblocker with render to scrape https://oxylabs.io/

## Prerequisites
### Install uv first.
https://docs.astral.sh/uv/getting-started/installation/#installation-methods

## Setup Intructions

### Installing via Smithery

To install Oxylabs MCP server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@oxylabs/oxylabs-mcp):

```bash
npx -y @smithery/cli install @oxylabs/oxylabs-mcp --client claude
```

### Running on Cursor

Configuring Cursor 🖥️
Note: Requires Cursor version 0.45.6+

To configure Oxylabs in Cursor:

1. Open Cursor Settings
2. Go to Features > MCP Servers 
3. Click "+ Add New MCP Server"
4. Enter the following:
   - Name: "oxylabs" (or your preferred name)
   - Type: "command"
   - Command: `env OXYLABS_USERNAME=your-username OXYLABS_PASSWORD=your-password npx -y oxylabs-mcp`

> If you are using Windows and are running into issues, try `cmd /c "set OXYLABS_USERNAME=your-username && set OXYLABS_PASSWORD=your-password && npx -y oxylabs-mcp"`

Replace `your-username` and `your-password` with your Oxylabs credentials.

After adding, refresh the MCP server list to see the new tools. The Composer Agent will automatically use Oxylabs when appropriate, but you can explicitly request it by describing your web scraping needs. Access the Composer via Command+L (Mac), select "Agent" next to the submit button, and enter your query.


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
        "OXYLABS_PASSWORD": "YOUR_PASSWORD_HERE"
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

## License

This project is licensed under the [MIT License](LICENSE).

## About Oxylabs

Established in 2015, Oxylabs are a market-leading web intelligence collection
platform, driven by the highest business, ethics, and compliance standards,
enabling companies worldwide to unlock data-driven insights.

[![image](https://oxylabs.io/images/og-image.png)](https://oxylabs.io/)
