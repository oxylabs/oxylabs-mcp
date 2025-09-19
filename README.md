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

[![smithery badge](https://smithery.ai/badge/@oxylabs/oxylabs-mcp)](https://smithery.ai/server/@oxylabs/oxylabs-mcp)
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

The Oxylabs MCP server provides a bridge between AI models and the web. It enables them to scrape any URL, render JavaScript-heavy pages, extract and format content for AI use, bypass anti-scraping measures, and access geo-restricted web data from 195+ countries.


## 🛠️ MCP Tools

Oxylabs MCP provides two sets of tools that can be used together or independently:

### Oxylabs Web Scraper API Tools
1. **universal_scraper**: Uses Oxylabs Web Scraper API for general website scraping;
2. **google_search_scraper**: Uses Oxylabs Web Scraper API to extract results from Google Search;
3. **amazon_search_scraper**: Uses Oxylabs Web Scraper API to scrape Amazon search result pages;
4. **amazon_product_scraper**: Uses Oxylabs Web Scraper API to extract data from individual Amazon product pages.

### Oxylabs AI Studio Tools

5. **ai_scraper**: Scrape content from any URL in JSON or Markdown format with AI-powered data extraction;
6. **ai_crawler**: Based on a prompt, crawls a website and collects data in Markdown or JSON format across multiple pages;
7. **ai_browser_agent**: Based on prompt, controls a browser and returns data in Markdown, JSON, HTML, or screenshot formats;
8. **ai_search**: Search the web for URLs and their contents with AI-powered content extraction.


## ✅ Prerequisites

Before you begin, make sure you have **at least one** of the following:

- **Oxylabs Web Scraper API Account**: Obtain your username and password from [Oxylabs](https://dashboard.oxylabs.io/) (1-week free trial available);
- **Oxylabs AI Studio API Key**: Obtain your API key from [Oxylabs AI Studio](https://aistudio.oxylabs.io/settings/api-key). (1000 credits free).

## 📦 Configuration

### Environment variables

Oxylabs MCP server supports the following environment variables:
| Name                       | Description                                   | Default |
|----------------------------|-----------------------------------------------|---------|
| `OXYLABS_USERNAME`         | Your Oxylabs Web Scraper API username         |         |
| `OXYLABS_PASSWORD`         | Your Oxylabs Web Scraper API password         |         |
| `OXYLABS_AI_STUDIO_API_KEY`| Your Oxylabs AI Studio API key                |         |
| `LOG_LEVEL`                | Log level for the logs returned to the client | `INFO`  |

Based on provided credentials, the server will automatically expose the corresponding tools:
- If only `OXYLABS_USERNAME` and `OXYLABS_PASSWORD` are provided, the server will expose the Web Scraper API tools;
- If only `OXYLABS_AI_STUDIO_API_KEY` is provided, the server will expose the AI Studio tools;
- If both `OXYLABS_USERNAME` and `OXYLABS_PASSWORD` and `OXYLABS_AI_STUDIO_API_KEY` are provided, the server will expose all tools.

❗❗❗ **Important note: if you don't have Web Scraper API or Oxylabs AI studio credentials, delete the corresponding environment variables placeholders.
Leaving placeholder values will result in exposed tools that do not work.**



### Configure with uvx

- Install the uvx package manager:
  ```bash
  # macOS and Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  OR:
  ```bash
  # Windows
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- Use the following config:
  ```json
  {
    "mcpServers": {
      "oxylabs": {
        "command": "uvx",
        "args": ["oxylabs-mcp"],
        "env": {
          "OXYLABS_USERNAME": "OXYLABS_USERNAME",
          "OXYLABS_PASSWORD": "OXYLABS_PASSWORD",
          "OXYLABS_AI_STUDIO_API_KEY": "OXYLABS_AI_STUDIO_API_KEY"
        }
      }
    }
  }
  ```

### Configure with uv

- Install the uv package manager:
  ```bash
  # macOS and Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  OR:
  ```bash
  # Windows
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

- Use the following config:
  ```json
  {
    "mcpServers": {
      "oxylabs": {
        "command": "uv",
        "args": [
          "--directory",
          "/<Absolute-path-to-folder>/oxylabs-mcp",
          "run",
          "oxylabs-mcp"
        ],
        "env": {
          "OXYLABS_USERNAME": "OXYLABS_USERNAME",
          "OXYLABS_PASSWORD": "OXYLABS_PASSWORD",
          "OXYLABS_AI_STUDIO_API_KEY": "OXYLABS_AI_STUDIO_API_KEY"
        }
      }
    }
  }
  ```

### Configure with Smithery Oauth2

- Go to https://smithery.ai/server/@oxylabs/oxylabs-mcp;
- Click _Auto_ to install the Oxylabs MCP configuration for the respective client;
- OR use the following config:
```json
  {
    "mcpServers": {
      "oxylabs": {
        "url": "https://server.smithery.ai/@oxylabs/oxylabs-mcp/mcp"
      }
    }
  }
```
- Follow the instructions to authenticate Oxylabs MCP with Oauth2 flow

### Configure with Smithery query parameters

In case your client does not support the Oauth2 authentication, you can pass the Oxylabs authentication parameters directly in url
```json
  {
    "mcpServers": {
      "oxylabs": {
        "url": "https://server.smithery.ai/@oxylabs/oxylabs-mcp/mcp?oxylabsUsername=OXYLABS_USERNAME&oxylabsPassword=OXYLABS_PASSWORD&oxylabsAiStudioApiKey=OXYLABS_AI_STUDIO_API_KEY"
      }
    }
  }
```

### Manual Setup with Claude Desktop

Navigate to **Claude → Settings → Developer → Edit Config** and add one of the configurations above to the `claude_desktop_config.json` file.

### Manual Setup with Cursor AI

Navigate to **Cursor → Settings → Cursor Settings → MCP**. Click **Add new global MCP server** and add one of the configurations above.



## 📝 Logging

Server provides additional information about the tool calls in `notification/message` events

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

---


## Why Oxylabs MCP? &nbsp;🕸️ ➜ 📦 ➜ 🤖

Imagine telling your LLM *"Summarise the latest Hacker News discussion about GPT‑5"* – and it simply answers.  
MCP (Multi‑Client Proxy) makes that happen by doing the boring parts for you:

| What Oxylabs MCP does                                             | Why it matters to you                    |
|-------------------------------------------------------------------|------------------------------------------|
| **Bypasses anti‑bot walls** with the Oxylabs global proxy network | Keeps you unblocked and anonymous        |
| **Renders JavaScript** in headless Chrome                         | Single‑page apps, sorted                 |
| **Cleans HTML → JSON**                                            | Drop straight into vector DBs or prompts |
| **Optional structured parsers** (Google, Amazon, etc.)            | One‑line access to popular targets       |

