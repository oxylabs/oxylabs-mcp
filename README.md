<p align="center">
  <img src="img/oxylabs_mcp.svg" alt="Oxylabs + MCP">
</p>
<h1 align="center" style="border-bottom: none;">
  Oxylabs MCP Server
</h1>
<p align="center">
  <p align="center">Access web data seamlessly with Oxylabs via the Model Context Protocol</p>
</p>

[![smithery badge](https://smithery.ai/badge/@oxylabs/oxylabs-mcp)](https://smithery.ai/server/@oxylabs/oxylabs-mcp)
[![pypi package](https://img.shields.io/pypi/v/oxylabs-mcp?color=%2334D058&label=pypi%20package)](https://pypi.org/project/oxylabs-mcp/)
[![](https://dcbadge.vercel.app/api/server/eWsVUJrnG5?style=flat)](https://discord.gg/Pds3gBmKMH)
<br/>
<a href="https://glama.ai/mcp/servers/@oxylabs/oxylabs-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@oxylabs/oxylabs-mcp/badge" alt="Oxylabs Server MCP server" />
</a>

## 📖 Overview

The Oxylabs MCP server provides a bridge between AI models and the web. It enables them to scrape any URL, render JavaScript-heavy pages, extract and format content for AI use, bypass anti-scraping measures, and access geo-restricted web data from 195+ countries.

This implementation leverages the Model Context Protocol (MCP) to create a secure, standardized way for AI assistants to interact with web content.

## ✨ Key Features

<details>
<summary><strong> Scrape content from any site</strong></summary>
<br>

- Extract data from any URL, including complex single-page applications
- Fully render dynamic websites using headless browser support
- Choose full JavaScript rendering, HTML-only, or none
- Emulate Mobile and Desktop viewports for realistic rendering

</details>

<details>
<summary><strong> Automatically get AI-ready data</strong></summary>
<br>

- Automatically clean and convert HTML to Markdown for improved readability
- Use automated parsers for popular targets like Google, Amazon, and etc.

</details>

<details>
<summary><strong> Bypass blocks & geo-restrictions</strong></summary>
<br>

- Bypass sophisticated bot protection systems with high success rate
- Reliably scrape even the most complex websites
- Get automatically rotating IPs from a proxy pool covering 195+ countries

</details>

<details>
<summary><strong> Flexible setup & cross-platform support</strong></summary>
<br>

- Set rendering and parsing options if needed
- Feed data directly into AI models or analytics tools
- Works on macOS, Windows, and Linux

</details>

<details>
<summary><strong> Built-in error handling and request management</strong></summary>
<br>

- Comprehensive error handling and reporting
- Smart rate limiting and request management

</details>

## 💡 Example Queries
When you've set up the MCP server with **Claude**, you can make requests like:

- Could you scrape `https://www.google.com/search?q=ai` page?
- Scrape `https://www.amazon.de/-/en/Smartphone-Contract-Function-Manufacturer-Exclusive/dp/B0CNKD651V` with **parse** enabled
- Scrape `https://www.amazon.de/-/en/gp/bestsellers/beauty/ref=zg_bs_nav_beauty_0` with **parse** and **render** enabled
- Use web unblocker with **render** to scrape `https://www.bestbuy.com/site/top-deals/all-electronics-on-sale/pcmcat1674241939957.c`

## ✅ Prerequisites

Before you begin, make sure you have:

- **Oxylabs Account**: Obtain your username and password from [Oxylabs](https://dashboard.oxylabs.io/) (1-week free trial available)

### Basic Usage
Via Smithery CLI:
- **Node.js** (v16+)
- `npx` command-line tool

Via uv:
- `uv` package manager – install it using [this guide](https://docs.astral.sh/uv/getting-started/installation/)

### Local/Dev Setup
- **Python 3.12+**
- `uv` package manager – install it using [this guide](https://docs.astral.sh/uv/getting-started/installation/)

## 🧩 API Parameters

The Oxylabs MCP server supports these parameters:

| Parameter | Description | Values |
|-----------|-------------|--------|
| `url` | The URL to scrape | Any valid URL |
| `parse` | Enable structured data extraction | `True` or `False` |
| `render` | Use headless browser rendering | `html` or `None` |

## ⚙️ Basic Setup Instructions

### Install via Smithery

Automatically install Oxylabs MCP server via [Smithery](https://smithery.ai/server/@oxylabs/oxylabs-mcp):

```bash
npx -y @smithery/cli install @oxylabs/oxylabs-mcp --client <client>
```

List of clients supported by Oxylabs at the moment:
  - claude
  - cursor

### Manual MCP configuration options

1. Config with `uvx`. Will install the CLI client and Oxylabs MCP server that performs calls directly to the Oxylabs API. Recommended and the most stable option at the moment.
    ```json
    {
      "mcpServers": {
        "oxylabs_scraper_uvx": {
          "command": "uvx",
          "args": [
            "oxylabs-mcp"
          ],
          "env": {
            "OXYLABS_USERNAME": "OXYLABS_USERNAME",
            "OXYLABS_PASSWORD": "OXYLABS_PASSWORD"
          }
        }
      }
    }
    ```

2. Config with `npx`. Will install the Smithery CLI client that performs calls to the Oxylabs MCP server hosted in Smithery.
    ```json
    {
      "mcpServers": {
        "oxylabs-mcp": {
          "command": "npx",
          "args": [
            "-y",
            "@smithery/cli@latest",
            "run",
            "@oxylabs/oxylabs-mcp",
            "--config",
            "\"{\\\"oxylabsUsername\\\":\\\"OXYLABS_USERNAME\\\",\\\"oxylabsPassword\\\":\\\"OXYLABS_PASSWORD\\\"}\""
          ]
        }
      }
    }
    ```

3. Config with `uv`. Will install CLI client and Oxylabs MCP server that references the local code. For the local development.
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
            "OXYLABS_USERNAME": "OXYLABS_USERNAME",
            "OXYLABS_PASSWORD": "OXYLABS_PASSWORD"
          }
        }
      }
    }
    ```

> [!NOTE]
> If you don't have `uvx` utility you need to install it first with `brew install uv`

> [!TIP]
> If you run into errors with `uvx`, try using the full path to `uvx` in the `command` field. For example, `/Users/my-user/.local/bin/uvx`.
> If you are using Windows and experiencing issues with Cursor, refer to the guidelines described [here](https://smithery.ai/docs/faq/users).


### Manual Setup with Claude Desktop

Navigate to **Claude → Settings → Developer → Edit Config** and add one of the configurations above to the `claude_desktop_config.json` file.

### Manual Setup with Cursor AI

Navigate to **Cursor → Settings → Cursor Settings → MCP**. Click **Add new global MCP server** and add one of the configurations above.

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

---
### 🐞 Debugging

```bash
make run
```
Then access MCP Inspector at `http://localhost:5173`. You may need to add your username and password as environment variables in the inspector under `OXYLABS_USERNAME` and `OXYLABS_PASSWORD`.


## 🛠️ Technical Details

This server provides two main tools:

1. **oxylabs_scraper**: Uses Oxylabs Web Scraper API for general website scraping
2. **oxylabs_web_unblocker**: Uses Oxylabs Web Unblocker for hard-to-access websites

[Web Scraper API](https://oxylabs.io/products/scraper-api/web) supports JavaScript rendering, parsed structured data, and cleaned HTML in Markdown format. [Web Unblocker](https://oxylabs.io/products/web-unblocker) offers JavaScript rendering and cleaned HTML, but doesn’t return parsed data.

---

## License

This project is licensed under the [MIT License](LICENSE).

## About Oxylabs

Established in 2015, Oxylabs is a market-leading web intelligence collection
platform, driven by the highest business, ethics, and compliance standards,
enabling companies worldwide to unlock data-driven insights.

[![image](https://oxylabs.io/images/og-image.png)](https://oxylabs.io/)
