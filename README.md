# MCP Server for Oxylabs Scraper
[![smithery badge](https://smithery.ai/badge/@oxylabs/oxylabs-mcp)](https://smithery.ai/server/@oxylabs/oxylabs-mcp)

A Model Context Protocol (MCP) server that enables AI assistants like Claude to seamlessly access web data through Oxylabs' powerful web scraping technology.

<a href="https://glama.ai/mcp/servers/@oxylabs/oxylabs-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@oxylabs/oxylabs-mcp/badge" alt="Oxylabs Server MCP server" />
</a>

## 📖 Overview

The Oxylabs MCP server provides a bridge between AI models and the web. It enables them to scrape any URL, render JavaScript-heavy pages, extract and format content for AI use, bypass anti-scraping measures, and access geo-restricted data from 195+ countries.

This implementation leverages the Model Context Protocol (MCP) to create a secure, standardized way for AI assistants to interact with web content.

## ✨ Key Features

<details>
<summary><strong> Scrape content from any site</strong></summary>
<br>

- Extract data from any URL, including complex single-page applications
- Fully render dynamic websites using headless browser support
- Handle JavaScript-heavy and client-rendered content
- Choose full JavaScript rendering, HTML-only, or none
- Emulate Mobile and Desktop viewports for realistic rendering

</details>

<details>
<summary><strong> Automatically get AI-ready data</strong></summary>
<br>

- Automatically clean and convert HTML to Markdown for improved readability
- Use dedicated parsers extract structured data from popular targets like Google, Amazon, and etc.
- Define your custom parsing logic for any target

</details>

<details>
<summary><strong> Bypass blocks & geo-restrictions</strong></summary>
<br>

- Bypass sophisticated bot protection systems with high success rate
- Reliably scrape even the most complex websites
- Access geo-specific content from 195+ countries
- Automatically rotate IPs and target specific regions

</details>

<details>
<summary><strong> Flexible setup, batch scraping & cross-platform support</strong></summary>
<br>

- Customize rendering and parsing options per request
- Handle multiple URLs in a single job using Batch requests
- Feed data directly into AI models or analytics tools
- Works on macOS, Windows, and Linux

</details>

<details>
<summary><strong> Built-in error handling and smart request management</strong></summary>
<br>

- Comprehensive error handling and reporting
- Intelligent rate limiting and request management

</details>

## 💡 Example Queries

When you've set up the MCP server with Claude or another AI assistant, you can make requests like:

<pre>Could you scrape <i>https://www.google.com/search?q=ai</i> page?</pre>

<pre>Scrape <i>https://www.amazon.de/-/en/Smartphone-Contract-Function-Manufacturer-Exclusive/dp/B0CNKD651V</i> with parse enabled.</pre>

<pre>Scrape <i>https://www.amazon.de/-/en/gp/bestsellers/beauty/ref=zg_bs_nav_beauty_0</i> with parse and render enabled.</pre>

<pre>Use web unblocker with render to scrape <i>https://www.bestbuy.com/site/top-deals/all-electronics-on-sale/pcmcat1674241939957.c</i></pre>

## ✅ Prerequisites

Before you begin, make sure you have:

- **Oxylabs Account**: Obtain your username and password from [Oxylabs](https://dashboard.oxylabs.io/) (1-week free trial available)

### Basic Usage (via Smithery CLI or Cursor)
- **Node.js** (v16+)
- `npx` command-line tool

### Local/Dev Setup
- **Python 3.12+**
- `uv` package manager – install it using [this guide](https://docs.astral.sh/uv/getting-started/installation/)

## ⚙️ Basic Setup Instructions

### Install via Smithery (Recommended)

Automatically install Oxylabs MCP server for Claude Desktop via [Smithery](https://smithery.ai/server/@oxylabs/oxylabs-mcp):

```bash
npx -y @smithery/cli install @oxylabs/oxylabs-mcp --client claude
```
---
### Run on Cursor

> [!IMPORTANT]
> Requires Cursor version `0.45.6+`

To configure Oxylabs in Cursor:

1. Open Cursor **Settings**
2. Go to **Features > MCP Servers** 
3. Click "**+ Add New MCP Server**"
4. Enter the following:
   - **Name**: `oxylabs` (or your preferred name)
   - **Type**: `command`
   - **Command**:`npx -y @smithery/cli@latest run @oxylabs/oxylabs-mcp --config "{\"oxylabsUsername\":\"YOUR_USERNAME\",\"oxylabsPassword\":\"YOUR_PASSWORD\"}"`
  
Replace `your-username` and `your-password` with your Oxylabs credentials.

> [!TIP]
> If you're using Windows and run into issues, try this:
> 
> `cmd /c "set OXYLABS_USERNAME=your-username && set OXYLABS_PASSWORD=your-password && npx -y oxylabs-mcp"`

After that, refresh the MCP server list to see the new tools. The Composer Agent will automatically use Oxylabs when appropriate, but you can explicitly request it by describing your web scraping needs. Access the Composer via `Command+L` (Mac), select "Agent" next to the submit button, and enter your query.

---
### Set up with Claude Desktop

Enable **Developer Mode** and then navigate to **Claude → Settings → Developer → Edit Config** and edit your `claude_desktop_config.json` file as follows:

```json
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
---

## 💻 Local/Dev Setup Instructions

### Clone repository

```
git clone <git:url>
```

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

Enable **Developer Mode** and then navigate to **Claude → Settings → Developer → Edit Config** and edit your `claude_desktop_config.json` file as follows:

```json
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
---
### 🐞 Debugging

```bash
make run
```
Then access MCP Inspector at `http://localhost:5173`. You may need to add your username and password as environment variables in the inspector under `OXYLABS_USERNAME` and `OXYLABS_PASSWORD`.

## 🧩 API Parameters

The Oxylabs MCP server supports these parameters:

| Parameter | Description | Values |
|-----------|-------------|--------|
| `url` | The URL to scrape | Any valid URL |
| `parse` | Enable structured data extraction | `True` or `False` |
| `render` | Use headless browser rendering | `html` or `None` |

## 🛠️ Technical Details

This server provides two main tools:

1. **oxylabs_scraper**: Uses Oxylabs Web Scraper API for general website scraping
2. **oxylabs_web_unblocker**: Uses Oxylabs Web Unblocker for hard-to-access websites

[Web Scraper API](https://oxylabs.io/products/scraper-api/web) supports JavaScript rendering, parsed structured data, and cleaned HTML in Markdown format. [Web Unblocker](https://oxylabs.io/products/web-unblocker) offers JavaScript rendering and cleaned HTML, but doesn’t return parsed data.

---

> [!WARNING]
> Usage with the MCP Inspector is affected by an ongoing issue with the Python SDK for MCP, see: https://github.com/modelcontextprotocol/python-sdk/pull/85. For Claude, a forked version of the SDK is used as a temporary fix.

## License

This project is licensed under the [MIT License](LICENSE).

## About Oxylabs

Established in 2015, Oxylabs is a market-leading web intelligence collection
platform, driven by the highest business, ethics, and compliance standards,
enabling companies worldwide to unlock data-driven insights.

[![image](https://oxylabs.io/images/og-image.png)](https://oxylabs.io/)