---
title: "https://github.com/ChromeDevTools/chrome-devtools-mcp"
type: url
captured: 2026-04-13T13:30:02.023885+00:00
source: android-share
url: "https://github.com/ChromeDevTools/chrome-devtools-mcp"
content_hash: "sha256:379642deb53f3714eb4d3fd4bf685ddf06e1f2efdb0931fbf030395fd0d38ada"
tags: []
status: ingested
---

https://github.com/ChromeDevTools/chrome-devtools-mcp

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T00:01:02+00:00
- source_url: https://github.com/ChromeDevTools/chrome-devtools-mcp
- resolved_url: https://github.com/ChromeDevTools/chrome-devtools-mcp
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: ChromeDevTools/chrome-devtools-mcp
Description: Chrome DevTools for coding agents
Stars: 36414
Language: TypeScript
Topics: browser, chrome, chrome-devtools, debugging, devtools, mcp, mcp-server, puppeteer

## README

# Chrome DevTools for Agents

[![npm chrome-devtools-mcp package](https://img.shields.io/npm/v/chrome-devtools-mcp.svg)](https://npmjs.org/package/chrome-devtools-mcp)

Chrome DevTools for Agents (`chrome-devtools-mcp`) lets your coding agent (such as Gemini, Claude, Cursor or Copilot)
control and inspect a live Chrome browser. It acts as a Model-Context-Protocol
(MCP) server, giving your AI coding assistant access to the full power of
Chrome DevTools for reliable automation, in-depth debugging, and performance analysis.
A [CLI](docs/cli.md) is also provided for use without MCP.

## [Tool reference](./docs/tool-reference.md) | [Changelog](./CHANGELOG.md) | [Contributing](./CONTRIBUTING.md) | [Troubleshooting](./docs/troubleshooting.md) | [Design Principles](./docs/design-principles.md)

## Key features

- **Get performance insights**: Uses [Chrome
  DevTools](https://github.com/ChromeDevTools/devtools-frontend) to record
  traces and extract actionable performance insights.
- **Advanced browser debugging**: Analyze network requests, take screenshots and
  check browser console messages (with source-mapped stack traces).
- **Reliable automation**. Uses
  [puppeteer](https://github.com/puppeteer/puppeteer) to automate actions in
  Chrome and automatically wait for action results.

## Disclaimers

`chrome-devtools-mcp` exposes content of the browser instance to the MCP clients
allowing them to inspect, debug, and modify any data in the browser or DevTools.
Avoid sharing sensitive or personal information that you don't want to share with
MCP clients.

`chrome-devtools-mcp` officially supports Google Chrome and [Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing/) only.
Other Chromium-based browsers may work, but this is not guaranteed, and you may encounter unexpected behavior. Use at your own discretion.
We are committed to providing fixes and support for the latest version of [Extended Stable Chrome](https://chromiumdash.appspot.com/schedule).

Performance tools may send trace URLs to the Google CrUX API to fetch real-user
experience data. This helps provide a holistic performance picture by
presenting field data alongside lab data. This data is collected by the [Chrome
User Experience Report (CrUX)](https://developer.chrome.com/docs/crux). To disable
this, run with the `--no-performance-crux` flag.

## **Usage statistics**

Google collects usage statistics (such as tool invocation success rates, latency, and environment information) to improve the reliability and performance of Chrome DevTools MCP.

Data collection is **enabled by default**. You can opt-out by passing the `--no-usage-statistics` flag when starting the server:

```json
"args": ["-y", "chrome-devtools-mcp@latest", "--no-usage-statistics"]
```

Google handles this data in accordance with the [Google Privacy Policy](https://policies.google.com/privacy).

Google's collection of usage statistics for Chrome DevTools MCP is independent from the Chrome browser's usage statistics. Opting out of Chrome metrics does not automatically opt you out of this tool, and vice-versa.

Collection is disabled if `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS` or `CI` env variables are set.

## Update checks

By default, the server periodically checks the npm registry for updates and logs a notification when a newer version is available.
You can disable these update checks by setting the `CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS` environment variable.

## Requirements

- [Node.js](https://nodejs.org/) v20.19 or a newer [latest maintenance LTS](https://github.com/nodejs/Release#release-schedule) version.
- [Chrome](https://www.google.com/chrome/) current stable version or newer.
- [npm](https://www.npmjs.com/)

## Getting started

Add the following config to your MCP client:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

> [!NOTE]
> Using `chrome-devtools-mcp@latest` ensures that your MCP client will always use the latest version of the Chrome DevTools MCP server.

If you are interested in doing only basic browser tasks, use the `--slim` mode:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--slim", "--headless"]
    }
  }
}
```

See [Slim tool reference](./docs/slim-tool-reference.md).

### MCP Client configuration

<details>
  <summary>Amp</summary>
  Follow https://ampcode.com/manual#mcp and use the config provided above. You can also install the Chrome DevTools MCP server using the CLI:

```bash
amp mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

</details>

<details>
  <summary>Antigravity</summary>

To use the Chrome DevTools MCP server follow the instructions from <a href="https://antigravity.google/docs/mcp">Antigravity's docs</a> to install a custom MCP server. Add the following config to the MCP servers config:

```bash
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--browser-url=http://127.0.0.1:9222",
        "-y"
      ]
    }
  }
}
```

This will make the Chrome DevTools MCP server automatically connect to the browser that Antigravity is using. If you are not using port 9222, make sure to adjust accordingly.

Chrome DevTools MCP will not start the browser instance automatically using this approach because the Chrome DevTools MCP server connects to Antigravity's built-in browser. If the browser is not already running, you have to start it first by clicking the Chrome icon at the top right corner.

</details>

<details>
  <summary>Claude Code</summary>

**Install via CLI (MCP only)**

Use the Claude Code CLI to add the Chrome DevTools MCP server (<a href="https://code.claude.com/docs/en/mcp">guide</a>):

```bash
claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest
```

**Install as a Plugin (MCP + Skills)**

> [!NOTE]
> If you already had Chrome DevTools MCP installed previously for Claude Code, make sure to remove it first from your installation and configuration files.

To install Chrome DevTools MCP with skills, add the marketplace registry in Claude Code:

```sh
/plugin marketplace add ChromeDevTools/chrome-devtools-mcp
```

Then, install the plugin:

```sh
/plugin install chrome-devtools-mcp
```

Restart Claude Code to have the MCP server and skills load (check with `/skills`).

> [!TIP]
> If the plugin installation fails with a `Failed to clone repository` error (e.g., HTTPS connectivity issues behind a corporate firewall), see the [troubleshooting guide](./docs/troubleshooting.md#claude-code-plugin-installation-fails-with-failed-to-clone-repository) for workarounds, or use the CLI installation method above instead.

</details>

<details>
  <summary>Cline</summary>
  Follow https://docs.cline.bot/mcp/configuring-mcp-servers and use the config provided above.
</details>

<details>
  <summary>Codex</summary>
  Follow the <a href="https://developers.openai.com/codex/mcp/#configure-with-the-cli">configure MCP guide</a>
  using the standard config from above. You can also install the Chrome DevTools MCP server using the Codex CLI:

```bash
codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

**On Windows 11**

Configure the Chrome install location and increase the startup timeout by updating `.codex/config.toml` and adding the following `env` and `startup_timeout_ms` parameters:

```
[mcp_servers.chrome-devtools]
command = "cmd"
args = [
    "/c",
    "npx",
    "-y",
    "chrome-devtools-mcp@latest",
]
env = { SystemRoot="C:\\Windows", PROGRAMFILES="C:\\Program Files" }
startup_timeout_ms = 20_000
```

</details>

<details>
  <summary>Command Code</summary>

Use the Command Code CLI to add the Chrome DevTools MCP server (<a href="https://commandcode.ai/docs/mcp">MCP guide</a>):

```bash
cmd mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest
```

</details>

<details>
  <summary>Copilot CLI</summary>

Start Copilot CLI:

```
copilot
```

Start the dialog to add a new MCP server by running:

```
/mcp add
```

Configure the following fields and press `CTRL+S` to save the configuration:

- **Server name:** `chrome-devtools`
- **Server Type:** `[1] Local`
- **Command:** `npx -y chrome-devtools-mcp@latest`

</details>

<details>
  <summary>Copilot / VS Code</summary>

**Install as a Plugin (Recommended)**

The easiest way to get up and running is to install `chrome-devtools-mcp` as an agent plugin.
This bundles the **MCP server** and all **skills** together, so your agent gets both the tools
and the expert guidance it needs to use them effectively.

1.  Open the **Command Palette** (`Cmd+Shift+P` on macOS or `Ctrl+Shift+P` on Windows/Linux).
2.  Search for and run the **Chat: Install Plugin From Source** command.
3.  Paste in our repository URL: `https://github.com/ChromeDevTools/chrome-devtools-mcp`

That's it! Your agent is now supercharged with Chrome DevTools capabilities.

---

**Install as an MCP Server (MCP only)**

**Click the button to install:**

[<img src="https://img.shields.io/badge/VS_Code-VS_Code?style=flat-square&label=Install%20Server&color=0098FF" alt="Install in VS Code">](https://vscode.dev/redirect/mcp/install?name=io.github.ChromeDevTools%2Fchrome-devtools-mcp&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22chrome-devtools-mcp%22%5D%2C%22env%22%3A%7B%7D%7D)

[<img src="https://img.shields.io/badge/VS_Code_Insiders-VS_Code_Insiders?style=flat-square&label=Install%20Server&color=24bfa5" alt="Install in VS Code Insiders">](https://insiders.vscode.dev/redirect?url=vscode-insiders%3Amcp%2Finstall%3F%257B%2522name%2522%253A%2522io.github.ChromeDevTools%252Fchrome-devtools-mcp%2522%252C%2522config%2522%253A%257B%2522command%2522%253A%2522npx%2522%252C%2522args%2522%253A%255B%2522-y%2522%252C%2522chrome-devtools-mcp%2522%255D%252C%2522env%2522%253A%257B%257D%257D%257D)

**Or install manually:**

Follow the VS Code [MCP configuration guide](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server) using the standard config from above, or use the CLI:

For macOS and Linux:

```bash
code --add-mcp '{"name":"io.github.ChromeDevTools/chrome-devtools-mcp","command":"npx","args":["-y","chrome-devtools-mcp"],"env":{}}'
```

For Windows (PowerShell):

```powershell
code --add-mcp '{"""name""":"""io.github.ChromeDevTools/chrome-devtools-mcp""","""command""":"""npx""","""args""":["""-y""","""chrome-devtools-mcp"""]}'
```

</details>

<details>
  <summary>Cursor</summary>

**Click the button to install:**

[<img src="https://cursor.com/deeplink/mcp-install-dark.svg" alt="Install in Cursor">](https://cursor.com/en/install-mcp?name=chrome-devtools&config=eyJjb21tYW5kIjoibnB4IC15IGNocm9tZS1kZXZ0b29scy1tY3BAbGF0ZXN0In0%3D)

**Or install manually:**

Go to `Cursor Settings` -> `MCP` -> `New MCP Server`. Use the config provided above.

</details>

<details>
  <summary>Factory CLI</summary>
Use the Factory CLI to add the Chrome DevTools MCP server (<a href="https://docs.factory.ai/cli/configuration/mcp">guide</a>):

```bash
droid mcp add chrome-devtools "npx -y chrome-devtools-mcp@latest"
```

</details>

<details>
  <summary>Gemini CLI</summary>
Install the Chrome DevTools MCP server using the Gemini CLI.

**Project wide:**

```bash
# Either MCP only:
gemini mcp add chrome-devtools npx chrome-devtools-mcp@latest
# Or as a Gemini extension (MCP+Skills):
gemini extensions install --auto-update https://github.com/ChromeDevTools/chrome-devtools-mcp
```

**Globally:**

```bash
gemini mcp add -s user chrome-devtools npx chrome-devtools-mcp@latest
```

Alternatively, follow the <a href="https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md#how-to-set-up-your-mcp-server">MCP guide</a> and use the standard config from above.

</details>

<details>
  <summary>Gemini Code Assist</summary>
  Follow the <a href="https://cloud.google.com/gemini/docs/codeassist/use-agentic-chat-pair-programmer#configure-mcp-servers">configure MCP guide</a>
  using the standard config from above.
</details>

<details>
  <summary>JetBrains AI Assistant & Junie</summary>

Go to `Settings | Tools | AI Assistant | Model Context Protocol (MCP)` -> `Add`. Use the config provided above.
The same way chrome-devtools-mcp can be configured for JetBrains Junie in `Settings | Tools | Junie | MCP Settings` -> `Add`. Use the config provided above.

</details>

<details>
  <summary>Kiro</summary>

In **Kiro Settings**, go to `Configure MCP` > `Open Workspace or User MCP Config` > Use the configuration snippet provided above.

Or, from the IDE **Activity Bar** > `Kiro` > `MCP Servers` > `Click Open MCP Config`. Use the configuration snippet provided above.

</details>

<details>
  <summary>Katalon Studio</summary>

The Chrome DevTools MCP server can be used with <a href="https://docs.katalon.com/katalon-studio/studioassist/mcp-servers/setting-up-chrome-devtools-mcp-server-for-studioassist">Katalon StudioAssist</a> via an MCP proxy.

**Step 1:** Install the MCP proxy by following the <a href="https://docs.katalon.com/katalon-studio/studioassist/mcp-servers/setting-up-mcp-proxy-for-stdio-mcp-servers">MCP proxy setup guide</a>.

**Step 2:** Start the Chrome DevTools MCP server with the proxy:

```bash
mcp-proxy --transport streamablehttp --port 8080 -- npx -y chrome-devtools-mcp@latest
```

**Note:** You may need to pick another port if 8080 is already in use.

**Step 3:** In Katalon Studio, add the server to StudioAssist with the following settings:

- **Connection URL:** `http://127.0.0.1:8080/mcp`
- **Transport type:** `HTTP`

Once connected, the Chrome DevTools MCP tools will be available in StudioAssist.

</details>

<details>
  <summary>Mistral Vibe</summary>

Add in ~/.vibe/config.toml:

```toml
[[mcp_servers]]
name = "chrome-devtools"
transport = "stdio"
command = "npx"
args = ["chrome-devtools-mcp@latest"]
```

</details>

<details>
  <summary>OpenCode</summary>

Add the following configuration to your `opencode.json` file. If you don't have one, create it at `~/.config/opencode/opencode.json` (<a href="https://opencode.ai/docs/mcp-servers">guide</a>):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "chrome-devtools": {
      "type": "local",
      "command": ["npx", "-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

</details>

<details>
  <summary>Qoder</summary>

In **Qoder Settings**, go to `MCP Server` > `+ Add` > Use the configuration snippet provided above.

Alternatively, follow the <a href="https://docs.qoder.com/user-guide/chat/model-context-protocol">MCP guide</a> and use the standard config from above.

</details>

<details>
  <summary>Qoder CLI</summary>

Install the Chrome DevTools MCP server using the Qoder CLI (<a href="https://docs.qoder.com/cli/using-cli#mcp-servers">guide</a>):

**Project wide:**

```bash
qodercli mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

**Globally:**

```bash
qodercli mcp add -s user chrome-devtools -- npx chrome-devtools-mcp@latest
```

</details>

<details>
  <summary>Visual Studio</summary>

**Click the button to install:**

[<img src="https://img.shields.io/badge/Visual_Studio-Install-C16FDE?logo=visualstudio&logoColor=white" alt="Install in Visual Studio">](https://vs-open.link/mcp-install?%7B%22name%22%3A%22chrome-devtools%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22chrome-devtools-mcp%40latest%22%5D%7D)

</details>

<details>
  <summary>Warp</summary>

Go to `Settings | AI | Manage MCP Servers` -> `+ Add` to [add an MCP Server](https://docs.warp.dev/knowledge-and-collaboration/mcp#adding-an-mcp-server). Use the config provided above.

</details>

<details>
  <summary>Windsurf</summary>
  Follow the <a href="https://docs.windsurf.com/windsurf/cascade/mcp#mcp-config-json">configure MCP guide</a>
  using the standard config from above.
</details>

### Your first prompt

Enter the following prompt in your MCP Client to check if everything is working:

```
Check the performance of https://developers.chrome.com
```

Your MCP client should open the browser and record a performance trace.

> [!NOTE]
> The MCP server will start the browser automatically once the MCP client uses a tool that requires a running browser instance. Connecting to the Chrome DevTools MCP server on its own will not automatically start the browser.

## Tools

If you run into any issues, checkout our [troubleshooting guide](./docs/troubleshooting.md).

<!-- BEGIN AUTO GENERATED TOOLS -->

- **Input automation** (9 tools)
  - [`click`](docs/tool-reference.md#click)
  - [`drag`](docs/tool-reference.md#drag)
  - [`fill`](docs/tool-reference.md#fill)
  - [`fill_form`](docs/tool-reference.md#fill_form)
  - [`handle_dialog`](docs/tool-reference.md#handle_dialog)
  - [`hover`](docs/tool-reference.md#hover)
  - [`press_key`](docs/tool-reference.md#press_key)
  - [`type_text`](docs/tool-reference.md#type_text)
  - [`upload_file`](docs/tool-reference.md#upload_file)
- **Navigation automation** (6 tools)
  - [`close_page`](docs/tool-reference.md#close_page)
  - [`list_pages`](docs/tool-reference.md#list_pages)
  - [`navigate_page`](docs/tool-reference.md#navigate_page)
  - [`new_page`](docs/tool-reference.md#new_page)
  - [`select_page`](docs/tool-reference.md#select_page)
  - [`wait_for`](docs/tool-reference.md#wait_for)
- **Emulation** (2 tools)
  - [`emulate`](docs/tool-reference.md#emulate)
  - [`resize_page`](docs/tool-reference.md#resize_page)
- **Performance** (3 tools)
  - [`performance_analyze_insight`](docs/tool-reference.md#performance_analyze_insight)
  - [`performance_start_trace`](docs/tool-reference.md#performance_start_trace)
  - [`performance_stop_trace`](docs/tool-reference.md#performance_stop_trace)
- **Network** (2 tools)
  - [`get_network_request`](docs/tool-reference.md#get_network_request)
  - [`list_network_requests`](docs/tool-reference.md#list_network_requests)
- **Debugging** (6 tools)
  - [`evaluate_script`](docs/tool-reference.md#evaluate_script)
  - [`get_console_message`](docs/tool-reference.md#get_console_message)
  - [`lighthouse_audit`](docs/tool-reference.md#lighthouse_audit)
  - [`list_console_messages`](docs/tool-reference.md#list_console_messages)
  - [`take_screenshot`](docs/tool-reference.md#take_screenshot)
  - [`take_snapshot`](docs/tool-reference.md#take_snapshot)
- **Memory** (1 tools)
  - [`take_memory_snapshot`](docs/tool-reference.md#take_memory_snapshot)

<!-- END AUTO GENERATED TOOLS -->

## Configuration

The Chrome DevTools MCP server supports the following configuration option:

<!-- BEGIN AUTO GENERATED OPTIONS -->

- **`--autoConnect`/ `--auto-connect`**
  If specified, automatically connects to a browser (Chrome 144+) running locally from the user data directory identified by the channel param (default channel is stable). Requires the remote debugging server to be started in the Chrome instance via chrome://inspect/#remote-debugging.
  - **Type:** boolean
  - **Default:** `false`

- **`--browserUrl`/ `--browser-url`, `-u`**
  Connect to a running, debuggable Chrome instance (e.g. `http://127.0.0.1:9222`). For more details see: https://github.com/ChromeDevTools/chrome-devtools-mcp#connecting-to-a-running-chrome-instance.
  - **Type:** string

- **`--wsEndpoint`/ `--ws-endpoint`, `-w`**
  WebSocket endpoint to connect to a running Chrome instance (e.g., ws://127.0.0.1:9222/devtools/browser/<id>). Alternative to --browserUrl.
  - **Type:** string

- **`--wsHeaders`/ `--ws-headers`**
  Custom headers for WebSocket connection in JSON format (e.g., '{"Authorization":"Bearer token"}'). Only works with --wsEndpoint.
  - **Type:** string

- **`--headless`**
  Whether to run in headless (no UI) mode.
  - **Type:** boolean
  - **Default:** `false`

- **`--executablePath`/ `--executable-path`, `-e`**
  Path to custom Chrome executable.
  - **Type:** string

- **`--isolated`**
  If specified, creates a tempor

## File: docs/cli.md

```
# Chrome DevTools CLI

The `chrome-devtools-mcp` package includes an **experimental** CLI interface that allows you to interact with the browser directly from your terminal. This is particularly useful for debugging or when you want an agent to generate scripts that automate browser actions.

## Getting started

Install the package globally to make the `chrome-devtools` command available:

```sh
npm i chrome-devtools-mcp@latest -g
chrome-devtools status # check if install worked.
```

## How it works

The CLI acts as a client to a background `chrome-devtools-mcp` daemon (uses Unix sockets on Linux/Mac and named pipes on Windows).

- **Automatic Start**: The first time you call a tool (e.g., `list_pages`), the CLI automatically starts the MCP server and the browser in the background if they aren't already running.
- **Persistence**: The same background instance is reused for subsequent commands, preserving the browser state (open pages, cookies, etc.).
- **Manual Control**: You can explicitly manage the background process using `start`, `stop`, and `status`. The `start` command forwards all subsequent arguments to the underlying MCP server (e.g., `--headless`, `--userDataDir`) but not all args are supported. Run `chrome-devtools start --help` for supported args. Headless is enabled by default. Isolated is enabled by default unless `--userDataDir` is provided.

```sh
# Check if the daemon is running
chrome-devtools status

# Navigate the current page to a URL
chrome-devtools navigate_page "https://google.com"

# Take a screenshot and save it to a file
chrome-devtools take_screenshot --filePath screenshot.png

# Stop the background daemon when finished
chrome-devtools stop
```

## Command Usage

The CLI supports all tools available in the [Tool reference](./tool-reference.md).

```sh
chrome-devtools <tool> [arguments] [flags]
```

- **Required Arguments**: Passed as positional arguments.
- **Optional Arguments**: Passed as flags (e.g., `--filePath`, `--fullPage`).

### Examples

**New Page and Navigation:**

```sh
chrome-devtools new_page "https://example.com"
chrome-devtools navigate_page "https://web.dev" --type url
```

**Interaction:**

```sh
# Click an element by its UID from a snapshot
chrome-devtools click "element-uid-123"

# Fill a form field
chrome-devtools fill "input-uid-456" "search query"
```

**Analysis:**

```sh
# Run a Lighthouse audit (defaults to navigation mode)
chrome-devtools lighthouse_audit --mode snapshot
```

## Output format

By default, the CLI outputs a human-readable summary of the tool's result. For programmatic use, you can request raw JSON:

```sh
chrome-devtools list_pages --output-format=json
```

## Troubleshooting

If the CLI hangs or fails to connect, try stopping the background process:

```sh
chrome-devtools stop
```

For more verbose logs, set the `DEBUG` environment variable:

```sh
DEBUG=* chrome-devtools list_pages
```

## CLI generation

Implemented in `scripts/generate-cli.ts`. Some commands are excluded from CLI
generation such as `wait_for` and `fill_form`.

`chrome-devtools-mcp` args are also filtered in `src/bin/chrome-devtools.ts`
because not all args make sense in a CLI interface.

```


## File: docs/debugging-android.md

```
# Experimental: Debugging Chrome on Android

This is an experimental feature as Puppeteer does not officially support Chrome on Android as a target.

The workflow below works for most users. See [Troubleshooting: DevTools is not detecting the Android device for more help](https://developer.chrome.com/docs/devtools/remote-debugging#troubleshooting) for more help.

1. Open the Developer Options screen on your Android. See [Configure on-device developer Options](https://developer.android.com/studio/debug/dev-options.html).
2. Select Enable USB Debugging.
3. Connect your Android device directly to your development machine using a USB cable.
4. On your development machine setup port forwarding from your development machine to your android device:
   ```shell
   adb forward tcp:9222 localabstract:chrome_devtools_remote
   ```
5. Configure your MCP server to connect to the Chrome
   ```json
   "chrome-devtools": {
     "command": "npx",
     "args": [
       "chrome-devtools-mcp@latest",
       "--wsEndpoint=ws://127.0.0.1:9222/devtools/browser/"
     ],
     "trust": true
   }
   ```
6. Test your setup by running the following prompt in your coding agent:
   ```none
   Check the performance of developers.chrome.com
   ```

The Chrome DevTools MCP server should now control Chrome on your Android device.

```


## File: docs/design-principles.md

```
# Design Principles

These are rough guidelines to follow when shipping features for the MCP server.
Apply them with nuance.

- **Agent-Agnostic API**: Use standards like MCP. Don't lock in to one LLM. Interoperability is key.
- **Token-Optimized**: Return semantic summaries. "LCP was 3.2s" is better than 50k lines of JSON. Files are the right location for large amounts of data.
- **Small, Deterministic Blocks**: Give agents composable tools (Click, Screenshot), not magic buttons.
- **Self-Healing Errors**: Return actionable errors that include context and potential fixes.
- **Human-Agent Collaboration**: Output must be readable by machines (structured) AND humans (summaries).
- **Progressive Complexity**: Tools should be simple by default (high-level actions) but offer advanced optional arguments for power users.
- **Reference over Value**: for heavy assets (screenshots, traces, videos), return a file path or resource URI, never the raw data stream. Some MCP clients support a built-in handling of heavy assets e.g. directly displaying images. This _could_ be an exception.

```


## File: docs/slim-tool-reference.md

```
<!-- AUTO GENERATED DO NOT EDIT - run 'npm run gen' to update-->

# Chrome DevTools MCP Slim Tool Reference (~359 cl100k_base tokens)

- **[Navigation automation](#navigation-automation)** (1 tools)
  - [`navigate`](#navigate)
- **[Debugging](#debugging)** (2 tools)
  - [`evaluate`](#evaluate)
  - [`screenshot`](#screenshot)

## Navigation automation

### `navigate`

**Description:** Loads a URL

**Parameters:**

- **url** (string) **(required)**: URL to [`navigate`](#navigate) to

---

## Debugging

### `evaluate`

**Description:** Evaluates a JavaScript script

**Parameters:**

- **script** (string) **(required)**: JS script to run on the page

---

### `screenshot`

**Description:** Takes a [`screenshot`](#screenshot)

**Parameters:** None

---

```


## File: docs/tool-reference.md

```
<!-- AUTO GENERATED DO NOT EDIT - run 'npm run gen' to update-->

# Chrome DevTools MCP Tool Reference (~7005 cl100k_base tokens)

- **[Input automation](#input-automation)** (9 tools)
  - [`click`](#click)
  - [`drag`](#drag)
  - [`fill`](#fill)
  - [`fill_form`](#fill_form)
  - [`handle_dialog`](#handle_dialog)
  - [`hover`](#hover)
  - [`press_key`](#press_key)
  - [`type_text`](#type_text)
  - [`upload_file`](#upload_file)
- **[Navigation automation](#navigation-automation)** (6 tools)
  - [`close_page`](#close_page)
  - [`list_pages`](#list_pages)
  - [`navigate_page`](#navigate_page)
  - [`new_page`](#new_page)
  - [`select_page`](#select_page)
  - [`wait_for`](#wait_for)
- **[Emulation](#emulation)** (2 tools)
  - [`emulate`](#emulate)
  - [`resize_page`](#resize_page)
- **[Performance](#performance)** (3 tools)
  - [`performance_analyze_insight`](#performance_analyze_insight)
  - [`performance_start_trace`](#performance_start_trace)
  - [`performance_stop_trace`](#performance_stop_trace)
- **[Network](#network)** (2 tools)
  - [`get_network_request`](#get_network_request)
  - [`list_network_requests`](#list_network_requests)
- **[Debugging](#debugging)** (6 tools)
  - [`evaluate_script`](#evaluate_script)
  - [`get_console_message`](#get_console_message)
  - [`lighthouse_audit`](#lighthouse_audit)
  - [`list_console_messages`](#list_console_messages)
  - [`take_screenshot`](#take_screenshot)
  - [`take_snapshot`](#take_snapshot)
- **[Memory](#memory)** (1 tools)
  - [`take_memory_snapshot`](#take_memory_snapshot)

## Input automation

### `click`

**Description:** Clicks on the provided element

**Parameters:**

- **uid** (string) **(required)**: The uid of an element on the page from the page content snapshot
- **dblClick** (boolean) _(optional)_: Set to true for double clicks. Default is false.
- **includeSnapshot** (boolean) _(optional)_: Whether to include a snapshot in the response. Default is false.

---

### `drag`

**Description:** [`Drag`](#drag) an element onto another element

**Parameters:**

- **from_uid** (string) **(required)**: The uid of the element to [`drag`](#drag)
- **to_uid** (string) **(required)**: The uid of the element to drop into
- **includeSnapshot** (boolean) _(optional)_: Whether to include a snapshot in the response. Default is false.

---

### `fill`

**Description:** Type text into an input, text area or select an option from a &lt;select&gt; element.

**Parameters:**

- **uid** (string) **(required)**: The uid of an element on the page from the page content snapshot
- **value** (string) **(required)**: The value to [`fill`](#fill) in
- **includeSnapshot** (boolean) _(optional)_: Whether to include a snapshot in the response. Default is false.

---

### `fill_form`

**Description:** [`Fill`](#fill) out multiple form elements at once

**Parameters:**

- **elements** (array) **(required)**: Elements from snapshot to [`fill`](#fill) out.
- **includeSnapshot** (boolean) _(optional)_: Whether to include a snapshot in the response. Default is false.

---

### `handle_dialog`

**Description:** If a browser dialog was opened, use this command to handle it

**Parameters:**

- **action** (enum: "accept", "dismiss") **(required)**: Whether to dismiss or accept the dialog
- **promptText** (string) _(optional)_: Optional prompt text to enter into the dialog.

---

### `hover`

**Description:** [`Hover`](#hover) over the provided element

**Parameters:**

- **uid** (string) **(required)**: The uid of an element on the page from the page content snapshot
- **includeSnapshot** (boolean) _(optional)_: Whether to include a snapshot in the response. Default is false.

---

### `press_key`

**Description:** Press a key or key combination. Use this when other input methods like [`fill`](#fill)() cannot be used (e.g., keyboard shortcuts, navigation keys, or special key combinations).

**Parameters:**

- **key** (string) **(required)**: A key or a combination (e.g., "Enter", "Control+A", "Control++", "Control+Shift+R"). Modifiers: Control, Shift, Alt, Meta
- **includeSnapshot** (boolean) _(optional)_: Whether to include a snapshot in the response. Default is false.

---

### `type_text`

**Description:** Type text using keyboard into a previously focused input

**Parameters:**

- **text** (string) **(required)**: The text to type
- **submitKey** (string) _(optional)_: Optional key to press after typing. E.g., "Enter", "Tab", "Escape"

---

### `upload_file`

**Description:** Upload a file through a provided element.

**Parameters:**

- **filePath** (string) **(required)**: The local path of the file to upload
- **uid** (string) **(required)**: The uid of the file input element or an element that will open file chooser on the page from the page content snapshot
- **includeSnapshot** (boolean) _(optional)_: Whether to include a snapshot in the response. Default is false.

---

## Navigation automation

### `close_page`

**Description:** Closes the page by its index. The last open page cannot be closed.

**Parameters:**

- **pageId** (number) **(required)**: The ID of the page to close. Call [`list_pages`](#list_pages) to list pages.

---

### `list_pages`

**Description:** Get a list of pages open in the browser.

**Parameters:** None

---

### `navigate_page`

**Description:** Go to a URL, or back, forward, or reload. Use project URL if not specified otherwise.

**Parameters:**

- **handleBeforeUnload** (enum: "accept", "decline") _(optional)_: Whether to auto accept or beforeunload dialogs triggered by this navigation. Default is accept.
- **ignoreCache** (boolean) _(optional)_: Whether to ignore cache on reload.
- **initScript** (string) _(optional)_: A JavaScript script to be executed on each new document before any other scripts for the next navigation.
- **timeout** (integer) _(optional)_: Maximum wait time in milliseconds. If set to 0, the default timeout will be used.
- **type** (enum: "url", "back", "forward", "reload") _(optional)_: Navigate the page by URL, back or forward in history, or reload.
- **url** (string) _(optional)_: Target URL (only type=url)

---

### `new_page`

**Description:** Open a new tab and load a URL. Use project URL if not specified otherwise.

**Parameters:**

- **url** (string) **(required)**: URL to load in a new page.
- **background** (boolean) _(optional)_: Whether to open the page in the background without bringing it to the front. Default is false (foreground).
- **isolatedContext** (string) _(optional)_: If specified, the page is created in an isolated browser context with the given name. Pages in the same browser context share cookies and storage. Pages in different browser contexts are fully isolated.
- **timeout** (integer) _(optional)_: Maximum wait time in milliseconds. If set to 0, the default timeout will be used.

---

### `select_page`

**Description:** Select a page as a context for future tool calls.

**Parameters:**

- **pageId** (number) **(required)**: The ID of the page to select. Call [`list_pages`](#list_pages) to get available pages.
- **bringToFront** (boolean) _(optional)_: Whether to focus the page and bring it to the top.

---

### `wait_for`

**Description:** Wait for the specified text to appear on the selected page.

**Parameters:**

- **text** (array) **(required)**: Non-empty list of texts. Resolves when any value appears on the page.
- **timeout** (integer) _(optional)_: Maximum wait time in milliseconds. If set to 0, the default timeout will be used.

---

## Emulation

### `emulate`

**Description:** Emulates various features on the selected page.

**Parameters:**

- **colorScheme** (enum: "dark", "light", "auto") _(optional)_: [`Emulate`](#emulate) the dark or the light mode. Set to "auto" to reset to the default.
- **cpuThrottlingRate** (number) _(optional)_: Represents the CPU slowdown factor. Omit or set the rate to 1 to disable throttling
- **geolocation** (string) _(optional)_: Geolocation (`&lt;latitude&gt;x&lt;longitude&gt;`) to [`emulate`](#emulate). L
```


## File: docs/troubleshooting.md

```
# Troubleshooting

## General tips

- Run `npx chrome-devtools-mcp@latest --help` to test if the MCP server runs on your machine.
- Make sure that your MCP client uses the same npm and node version as your terminal.
- When configuring your MCP client, try using the `--yes` argument to `npx` to
  auto-accept installation prompt.
- Find a specific error in the output of the `chrome-devtools-mcp` server.
  Usually, if your client is an IDE, logs would be in the Output pane.
- Search the [GitHub repository issues and discussions](https://github.com/ChromeDevTools/chrome-devtools-mcp) for help or existing similar problems.

## Debugging

Start the MCP server with debugging enabled and a log file:

- `DEBUG=* npx chrome-devtools-mcp@latest --log-file=/path/to/chrome-devtools-mcp.log`

Using `.mcp.json` to debug while using a client:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--log-file",
        "/path/to/chrome-devtools-mcp.log"
      ],
      "env": {
        "DEBUG": "*"
      }
    }
  }
}
```

## Specific problems

### `Error [ERR_MODULE_NOT_FOUND]: Cannot find module ...`

This usually indicates either a non-supported Node version is in use or that the
`npm`/`npx` cache is corrupted. Try clearing the cache, uninstalling
`chrome-devtools-mcp` and installing it again. Clear the cache by running:

```sh
rm -rf ~/.npm/_npx # NOTE: this might remove other installed npx executables.
npm cache clean --force
```

### `Target closed` error

This indicates that the browser could not be started. Make sure that no Chrome
instances are running or close them. Make sure you have the latest stable Chrome
installed and that [your system is able to run Chrome](https://support.google.com/chrome/a/answer/7100626?hl=en).

### Chrome crashes on macOS when using Web Bluetooth

On macOS, Chrome launched by an MCP client application (such as Claude Desktop) may crash when a Web Bluetooth prompt appears. This is caused by a macOS privacy permission violation (TCC).

To resolve this, grant Bluetooth permission to the MCP client application in `System Settings > Privacy & Security > Bluetooth`. After granting permission, restart the client application and start a new MCP session.

### Remote debugging between virtual machine (VM) and host fails

When attempting to connect to Chrome running on a host machine from within a virtual machine (VM), Chrome may reject the connection due to 'Host' header validation. You can bypass this restriction by creating an SSH tunnel from the VM to the host. In the VM, run:

```sh
ssh -N -L 127.0.0.1:9222:127.0.0.1:9222 <user>@<host-ip>
```

Point the MCP connection inside the VM to `http://127.0.0.1:9222`. This allows DevTools to reach the host browser without triggering the Host validation error.

### Operating system sandboxes

Some MCP clients allow sandboxing the MCP server using macOS Seatbelt or Linux
containers. If sandboxes are enabled, `chrome-devtools-mcp` is not able to start
Chrome that requires permissions to create its own sandboxes. As a workaround,
either disable sandboxing for `chrome-devtools-mcp` in your MCP client or use
`--browser-url` to connect to a Chrome instance that you start manually outside
of the MCP client sandbox.

### WSL

By default, `chrome-devtools-mcp` in WSL requires Chrome to be installed within the Linux environment. While it normally attempts to launch Chrome on the Windows side, this currently fails due to a [known WSL issue](https://github.com/microsoft/WSL/issues/14201). Ensure you are using a [Linux distribution compatible with Chrome](https://support.google.com/chrome/a/answer/7100626).

Possible workarounds include:

- **Install Google Chrome in WSL:**
  - `wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb`
  - `sudo dpkg -i google-chrome-stable_current_amd64.deb`

- **Use Mirrored networking:**
  1. Configure [Mirrored networking for WSL](https://learn.microsoft.com/en-us/windows/wsl/networking).
  2. Start Chrome on the Windows side with:
     `chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\path\to\dir`
  3. Start `chrome-devtools-mcp` with:
     `npx chrome-devtools-mcp --browser-url http://127.0.0.1:9222`

- **Use PowerShell or Git Bash** instead of WSL.

### Windows 10: Error during discovery for MCP server 'chrome-devtools': MCP error -32000: Connection closed

- **Solution 1** Call using `cmd` (For more info https://github.com/modelcontextprotocol/servers/issues/1082#issuecomment-2791786310)

  ```json
  "mcpServers": {
      "chrome-devtools": {
        "command": "cmd",
        "args": ["/c", "npx", "-y", "chrome-devtools-mcp@latest"]
      }
    }
  ```

  > **The Key Change:** On Windows, running a Node.js package via `npx` often requires the `cmd /c` prefix to be executed correctly from within another process like VSCode's extension host. Therefore, `"command": "npx"` was replaced with `"command": "cmd"`, and the actual `npx` command was moved into the `"args"` array, preceded by `"/c"`. This fix allows Windows to interpret the command correctly and launch the server.

- **Solution 2** Instead of another layer of shell you can write the absolute path to `npx`:
  > Note: The path below is an example. You must adjust it to match the actual location of `npx` on your machine. Depending on your setup, the file extension might be `.cmd`, `.bat`, or `.exe` rather than `.ps1`. Also, ensure you use double backslashes (`\\`) as path delimiters, as required by the JSON format.
  ```json
  "mcpServers": {
      "chrome-devtools": {
        "command": "C:\\nvm4w\\nodejs\\npx.ps1",
        "args": ["-y", "chrome-devtools-mcp@latest"]
      }
    }
  ```

### Claude Code plugin installation fails with `Failed to clone repository`

When installing `chrome-devtools-mcp` as a Claude Code plugin (either from the
official marketplace or via `/plugin marketplace add`), the installation may fail
with a timeout error if your environment cannot reach `github.com` on port 443
(HTTPS):

```
Failed to download/cache plugin chrome-devtools-mcp: Failed to clone repository:
  Cloning into '...'...
  fatal: unable to access 'https://github.com/ChromeDevTools/chrome-devtools-mcp.git/':
  Failed to connect to github.com port 443
```

This can happen in environments with restricted outbound HTTPS connectivity,
corporate firewalls, or proxy configurations that block HTTPS git operations.

**Workaround 1: Use SSH instead of HTTPS**

If you have SSH access to GitHub configured, you can redirect all GitHub HTTPS
URLs to use SSH by running:

```sh
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

Then retry the plugin installation. This tells git to use your SSH key for all
GitHub operations instead of HTTPS.

**Workaround 2: Install via CLI instead**

If the plugin marketplace approach fails, you can install `chrome-devtools-mcp`
as an MCP server directly without cloning the repository:

```sh
claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest
```

This bypasses the git clone entirely and uses npm/npx to fetch the package. Note
that this method installs only the MCP server without the bundled skills.

### Connection timeouts with `--autoConnect`

If you are using the `--autoConnect` flag and tools like `list_pages`, `new_page`, or `navigate_page` fail with a timeout (e.g., `ProtocolError: Network.enable timed out` or `The socket connection was closed unexpectedly`), this usually means the MCP server cannot handshake with the running Chrome instance correctly. Ensure:

1. Chrome 144+ is **already** running.
2. Remote debugging is enabled in Chrome via `chrome://inspect/#remote-debugging`.
3. You have allowed the remote debugging connection prompt in the browser.
4. There is no other MCP server or tool trying to connect to the same debugging port.

```


## File: .gitignore

```
# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*
.pnpm-debug.log*

trace.json
trace.json.gz

# Diagnostic reports (https://nodejs.org/api/report.html)
report.[0-9]*.[0-9]*.[0-9]*.[0-9]*.json

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Directory for instrumented libs generated by jscoverage/JSCover
lib-cov

# Coverage directory used by tools like istanbul
coverage
*.lcov

# nyc test coverage
.nyc_output

# Grunt intermediate storage (https://gruntjs.com/creating-plugins#storing-task-files)
.grunt

# Bower dependency directory (https://bower.io/)
bower_components

# node-waf configuration
.lock-wscript

# Compiled binary addons (https://nodejs.org/api/addons.html)
build/Release

# Dependency directories
node_modules/
jspm_packages/

# Snowpack dependency directory (https://snowpack.dev/)
web_modules/

# TypeScript cache
*.tsbuildinfo

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Optional stylelint cache
.stylelintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variable files
.env
.env.development.local
.env.test.local
.env.production.local
.env.local

# parcel-bundler cache (https://parceljs.org/)
.cache
.parcel-cache

# Next.js build output
.next
out

# Nuxt.js build / generate output
.nuxt
dist

# Gatsby files
.cache/
# Comment in the public line in if your project uses Gatsby and not Next.js
# https://nextjs.org/blog/next-9-1#public-directory-support
# public

# vuepress build output
.vuepress/dist

# vuepress v2.x temp and cache directory
.temp
.cache

# vitepress build output
**/.vitepress/dist

# vitepress cache directory
**/.vitepress/cache

# Docusaurus cache and generated files
.docusaurus

# Serverless directories
.serverless/

# FuseBox cache
.fusebox/

# DynamoDB Local files
.dynamodb/

# TernJS port file
.tern-port

# Stores VSCode versions used for testing VSCode extensions
.vscode-test

# Stores VSCode specific settings
.vscode
!.vscode/*.template.json
!.vscode/extensions.json

# yarn v2
.yarn/cache
.yarn/unplugged
.yarn/build-state.yml
.yarn/install-state.gz
.pnp.*

# Build output directory
build/

log.txt

.DS_Store
```


## File: .mcp.json

```
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"]
    }
  }
}

```


## File: .release-please-manifest.json

```
{
  ".": "0.21.0"
}

```


## File: CHANGELOG.md

```
# Changelog

## [0.21.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/compare/chrome-devtools-mcp-v0.20.3...chrome-devtools-mcp-v0.21.0) (2026-04-01)


### 🎉 Features

* add a skill for detecting memory leaks using take_memory_snapshot tool ([#1162](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1162)) ([d19a235](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/d19a2350f975ec2fbf8ee61b35163a48c0146c32))


### 🛠️ Fixes

* **cli:** avoid defaulting to isolated when userDataDir is provided ([#1258](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1258)) ([73e1e24](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/73e1e24b26f9e42a83116b586e34d47276a6a2fa))
* list_pages should work after selected page is closed ([#1145](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1145)) ([2664455](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/26644553028d8404fd65a005ea9c19a278671f4d))
* mark lighthouse and memory as non-read-only ([#1769](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1769)) ([bec9dae](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/bec9dae2d26b728feedcd660189f386e6228f3ae))
* **telemetry:** record client name ([9a47b65](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/9a47b657d7b17b9bc64508530c93d55e8033e2a6))
* versioning for Claude Code plugin ([#1233](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1233)) ([966b86f](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/966b86f3aaa9f87c2599b954c4e7f990c2a697ea))
* wrap .mcp.json config in mcpServers key ([#1246](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1246)) ([c7948cf](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/c7948cf0621d80b080220d4cfd36b62bef2790b9))


### 📄 Documentation

* Command Code CLI instructions for MCP server ([0a7c0a7](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/0a7c0a74b471935a3e2f5ca0fd93556e8e5165ec))
* provide disclaimer about supported browsers ([#1237](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1237)) ([8676b72](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/8676b7216c66dfd323c2f6c272544a75dbab4dba))


### 🏗️ Refactor

* set process titles for easier debugging ([#1770](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1770)) ([0fe3896](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/0fe3896d85c74ce8b2dc189fe8a310727f795344))

## [0.20.3](https://github.com/ChromeDevTools/chrome-devtools-mcp/compare/chrome-devtools-mcp-v0.20.2...chrome-devtools-mcp-v0.20.3) (2026-03-20)


### 🛠️ Fixes

* mark categoryExtensions flag mutually exclusive with autoConnect ([#1202](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1202)) ([8c2a7fc](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/8c2a7fc21ead6091567e85608f7916c001ccc7db)), closes [#1072](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1072)


### ⚡ Performance

* **memory:** release old navigation request in NetworkCollector ([#1200](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1200)) ([1e6456c](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/1e6456ce222a8f392341a530b2340336c7a1ab02))
* use CDP to find open DevTools pages (reland) ([#1210](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1210)) ([53483bc](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/53483bc637566658754d781d88f4353ad47f44a7))

## [0.20.2](https://github.com/ChromeDevTools/chrome-devtools-mcp/compare/chrome-devtools-mcp-v0.20.1...chrome-devtools-mcp-v0.20.2) (2026-03-18)


### 📄 Documentation

* add troubleshooting for Claude Code plugin HTTPS clone failures ([#1195](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1195)) ([d082ca4](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/d082ca4ecd35a023d09f9c1ff949d5fb0c3fb069))

## [0.20.1](https://github.com/ChromeDevTools/chrome-devtools-mcp/compare/chrome-devtools-mcp-v0.20.0...chrome-devtools-mcp-v0.20.1) (2026-03-16)


### 🛠️ Fixes

* update VS Code manual installation powershell command ([#1151](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1151)) ([6c64a5b](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/6c64a5b543714796b25a12dc6f2be7a1e683e8bd))


### ⚡ Performance

* use CDP to find open DevTools pages. ([#1150](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1150)) ([94de19c](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/94de19cdcdae9e31d0962b273ce352dc248eb5a8))

## [0.20.0](h
<!-- fetched-content:end -->
