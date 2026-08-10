<p align="center">
  <img src="https://storage.googleapis.com/oxylabs-public-assets/oxylabs_mcp.svg" alt="Oxylabs + MCP">
</p>
<h1 align="center" style="border-bottom: none;">
  Oxylabs MCP Server
</h1>

<p align="center">
  <em>The missing link between AI models and the real‑world web: one API that delivers clean, structured data from any site.</em>
</p>

<div align="center">

[![pypi package](https://img.shields.io/pypi/v/oxylabs-mcp?color=%2334D058&label=pypi%20package)](https://pypi.org/project/oxylabs-mcp/)
[![](https://dcbadge.vercel.app/api/server/eWsVUJrnG5?style=flat)](https://discord.gg/Pds3gBmKMH)
[![Licence](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Verified on MseeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/f6a9c0bc-83a6-4f78-89d9-f2cec4ece98d)
![Coverage badge](https://raw.githubusercontent.com/oxylabs/oxylabs-mcp/coverage/coverage-badge.svg)

<br/>
<a href="https://glama.ai/mcp/servers/@oxylabs/oxylabs-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@oxylabs/oxylabs-mcp/badge" alt="Oxylabs Server MCP server" />
</a>

</div>

---

## 📖 Overview

The Oxylabs MCP server provides a bridge between AI models and the web. It enables them to scrape any URL, render JavaScript-heavy pages, extract and format content for AI use, manage CAPTCHA, and access geo-restricted web data from 195+ countries.

It is built on the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), the open standard for connecting AI assistants to external tools and data.


## 🛠️ MCP Tools

Oxylabs MCP provides two sets of tools that can be used together or independently:

### Oxylabs Web Scraper API tools

1. **universal_scraper**: scrapes any URL, with optional JavaScript rendering, geo-targeting, and Markdown/HTML/links output;
2. **google_search_scraper**: extracts results from Google Search, with optional parsing into structured JSON;
3. **amazon_search_scraper**: scrapes Amazon search result pages, with optional parsing into structured JSON;
4. **amazon_product_scraper**: extracts data from individual Amazon product pages.

### Oxylabs AI Studio tools

5. **ai_scraper**: scrapes content from any URL with AI-powered extraction, in JSON, CSV, Markdown, or TOON format;
6. **ai_crawler**: crawls a website from a starting URL based on a prompt and collects data across multiple pages;
7. **ai_browser_agent**: controls a real browser based on a prompt — navigates, clicks, fills forms — and returns the result;
8. **ai_search**: searches the web and optionally returns Markdown content of each result;
9. **ai_map**: maps a website's URLs, filtered by keywords or a prompt;
10. **generate_schema**: generates an OpenAPI-format JSON schema for structured extraction with the AI tools above.


## ✅ Prerequisites

Before you begin, make sure you have **at least one** of the following:

- **Oxylabs Web Scraper API account**: obtain your username and password from [Oxylabs](https://dashboard.oxylabs.io/) (1-week free trial available);
- **Oxylabs AI Studio API key**: obtain your API key from [Oxylabs AI Studio](https://aistudio.oxylabs.io/settings/api-key) (1000 credits free).

You will also need the [uv](https://docs.astral.sh/uv/) package manager to run the server:

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 📦 Configuration

### Environment variables

Oxylabs MCP server supports the following environment variables:

| Name                        | Description                                   | Default |
|-----------------------------|-----------------------------------------------|---------|
| `OXYLABS_USERNAME`          | Your Oxylabs Web Scraper API username         |         |
| `OXYLABS_PASSWORD`          | Your Oxylabs Web Scraper API password         |         |
| `OXYLABS_AI_STUDIO_API_KEY` | Your Oxylabs AI Studio API key                |         |
| `LOG_LEVEL`                 | Log level for the logs returned to the client | `INFO`  |

Based on the provided credentials, the server automatically exposes the corresponding tools:
- If only `OXYLABS_USERNAME` and `OXYLABS_PASSWORD` are provided, the server exposes the Web Scraper API tools;
- If only `OXYLABS_AI_STUDIO_API_KEY` is provided, the server exposes the AI Studio tools;
- If all three are provided, the server exposes all tools.

❗ **Important: only set the environment variables you have real credentials for.
Leaving placeholder values will result in exposed tools that do not work.**

### Configure with uvx

Installs the [package from PyPI](https://pypi.org/project/oxylabs-mcp/) and runs it automatically:

```json
{
  "mcpServers": {
    "oxylabs": {
      "command": "uvx",
      "args": ["oxylabs-mcp"],
      "env": {
        "OXYLABS_USERNAME": "YOUR_USERNAME",
        "OXYLABS_PASSWORD": "YOUR_PASSWORD",
        "OXYLABS_AI_STUDIO_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### Configure with a local checkout

Useful for development — runs the server from a local clone of this repository:

```json
{
  "mcpServers": {
    "oxylabs": {
      "command": "uv",
      "args": [
        "--directory",
        "/<absolute-path-to-folder>/oxylabs-mcp",
        "run",
        "oxylabs-mcp"
      ],
      "env": {
        "OXYLABS_USERNAME": "YOUR_USERNAME",
        "OXYLABS_PASSWORD": "YOUR_PASSWORD",
        "OXYLABS_AI_STUDIO_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### Running as a remote HTTP server (self-hosting)

The server also supports the MCP streamable-HTTP transport. Start it with:

```bash
MCP_TRANSPORT=streamable-http MCP_HOST=0.0.0.0 MCP_PORT=8000 uvx oxylabs-mcp
```

With the HTTP transport, credentials are passed per request instead of environment variables:

| Credential                | How to pass it                                                                                         |
|---------------------------|--------------------------------------------------------------------------------------------------------|
| Web Scraper API           | `Authorization: Basic <base64(username:password)>` (standard HTTP Basic auth)                            |
| Web Scraper API (alternative) | `X-Oxylabs-Username` and `X-Oxylabs-Password` headers                                                |
| AI Studio                 | `X-Oxylabs-AI-Studio-Api-Key` header                                                                     |

Example client configuration:

```json
{
  "mcpServers": {
    "oxylabs": {
      "url": "https://your-host:8000/mcp",
      "headers": {
        "Authorization": "Basic <base64 of username:password>",
        "X-Oxylabs-AI-Studio-Api-Key": "YOUR_API_KEY"
      }
    }
  }
}
```

All tools are always listed regardless of provided credentials; calling a tool without the
credentials it needs returns an error message explaining exactly what to configure.

### Setup with Claude Desktop

Navigate to **Claude → Settings → Developer → Edit Config** and add one of the configurations above to the `claude_desktop_config.json` file.

### Setup with Cursor AI

Navigate to **Cursor → Settings → Cursor Settings → MCP**. Click **Add new global MCP server** and add one of the configurations above.


## 📝 Logging

The server provides additional information about the tool calls in `notification/message` events:

```json
{
  "method": "notifications/message",
  "params": {
    "level": "info",
    "data": "Create job with params: {\"url\": \"https://ip.oxylabs.io\"}"
  }
}
```

```json
{
  "method": "notifications/message",
  "params": {
    "level": "info",
    "data": "Job info: job_id=7333113830223918081 job_status=done"
  }
}
```

```json
{
  "method": "notifications/message",
  "params": {
    "level": "error",
    "data": "Error: request to Oxylabs API failed"
  }
}
```


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
- Use automated parsers for popular targets like Google, Amazon, and more

</details>

<details>
<summary><strong> Manage CAPTCHA & geo-restrictions</strong></summary>
<br>

- Navigate sophisticated automated request management systems with high success rate
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


## Why Oxylabs MCP? &nbsp;🕸️ ➜ 📦 ➜ 🤖

Imagine telling your LLM *"Summarise the latest Hacker News discussion about GPT‑5"* – and it simply answers.
The Oxylabs MCP server makes that happen by doing the boring parts for you:

| What Oxylabs MCP does                                                      | Why it matters to you                    |
|----------------------------------------------------------------------------|------------------------------------------|
| **Manages automated request walls** with the Oxylabs global proxy network  | Enables website access and anonymity     |
| **Renders JavaScript** in headless Chrome                                  | Single‑page apps, sorted                 |
| **Cleans HTML → Markdown**                                                 | Drop straight into vector DBs or prompts |
| **Optional structured parsers** (Google, Amazon, etc.)                     | One‑line access to popular targets       |

---

## 🛡️ License

Distributed under the MIT License – see [LICENSE](LICENSE) for details.

---

## About Oxylabs

Established in 2015, Oxylabs is a market-leading web intelligence collection
platform, driven by the highest business, ethics, and compliance standards,
enabling companies worldwide to unlock data-driven insights.

[![image](https://oxylabs.io/images/og-image.png)](https://oxylabs.io/)

<div align="center">
<sub>
  Made with ☕ by <a href="https://oxylabs.io">Oxylabs</a>.  Feel free to give us a ⭐ if MCP saved you a weekend.
</sub>
</div>

mcp-name: io.oxylabs/oxylabs-mcp
