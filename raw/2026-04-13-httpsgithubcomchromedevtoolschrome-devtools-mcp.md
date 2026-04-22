---
title: https://github.com/ChromeDevTools/chrome-devtools-mcp
type: url
captured: 2026-04-13 13:30:02.023885+00:00
source: android-share
url: https://github.com/ChromeDevTools/chrome-devtools-mcp
content_hash: sha256:97cd1189cf5c5518fa51e91df8636c5a3b0dcf5cb13889497c80fbdb8eeedb99
tags: []
status: ingested
last_refreshed: '2026-04-22T02:45:04+00:00'
---

https://github.com/ChromeDevTools/chrome-devtools-mcp

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-22T02:45:04+00:00
- source_url: https://github.com/ChromeDevTools/chrome-devtools-mcp
- resolved_url: https://github.com/ChromeDevTools/chrome-devtools-mcp
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: ChromeDevTools/chrome-devtools-mcp
Description: Chrome DevTools for coding agents
Stars: 36605
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
- **Extensions** (5 tools)
  - [`install_extension`](docs/tool-reference.md#install_extension)
  - [`list_extensions`](docs/tool-reference.md#list_extensions)
  - [`reload_extension`](docs/tool-reference.md#reload_extension)
  - [`trigger_extension_action`](docs/tool-reference.md#trigger_extension_action)
  - [`uninstall_extension`](docs/tool-reference.md#uninstall_extension)
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
  Custom headers for WebSocket connection in 
Languages: TypeScript 95.0%, JavaScript 5.0%, HTML 0.0%

## Recent Releases

### chrome-devtools-mcp-v0.22.0 (2026-04-21)

## [0.22.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/compare/chrome-devtools-mcp-v0.21.0...chrome-devtools-mcp-v0.22.0) (2026-04-21)


### 🎉 Features

* add update notification to both binaries ([#1783](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1783)) ([e01e333](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/e01e33355e85c3b38e7aba6aceff57271b99a830))
* auto handle dialogs during script evaluation  ([#1839](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1839)) ([da33cb5](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/da33…

### chrome-devtools-mcp-v0.21.0 (2026-04-01)

## [0.21.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/compare/chrome-devtools-mcp-v0.20.3...chrome-devtools-mcp-v0.21.0) (2026-04-01)


### 🎉 Features

* add a skill for detecting memory leaks using take_memory_snapshot tool ([#1162](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1162)) ([d19a235](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/d19a2350f975ec2fbf8ee61b35163a48c0146c32))


### 🛠️ Fixes

* **cli:** avoid defaulting to isolated when userDataDir is provided ([#1258](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1258)) ([73e1e24…

### chrome-devtools-mcp-v0.20.3 (2026-03-20)

## [0.20.3](https://github.com/ChromeDevTools/chrome-devtools-mcp/compare/chrome-devtools-mcp-v0.20.2...chrome-devtools-mcp-v0.20.3) (2026-03-20)


### 🛠️ Fixes

* mark categoryExtensions flag mutually exclusive with autoConnect ([#1202](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1202)) ([8c2a7fc](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/8c2a7fc21ead6091567e85608f7916c001ccc7db)), closes [#1072](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1072)


### ⚡ Performance

* **memory:** release old navigation request in NetworkCollector ([#1200](h…

### chrome-devtools-mcp-v0.20.2 (2026-03-18)

## [0.20.2](https://github.com/ChromeDevTools/chrome-devtools-mcp/compare/chrome-devtools-mcp-v0.20.1...chrome-devtools-mcp-v0.20.2) (2026-03-18)


### 📄 Documentation

* add troubleshooting for Claude Code plugin HTTPS clone failures ([#1195](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1195)) ([d082ca4](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/d082ca4ecd35a023d09f9c1ff949d5fb0c3fb069))

### chrome-devtools-mcp-v0.20.1 (2026-03-17)

## [0.20.1](https://github.com/ChromeDevTools/chrome-devtools-mcp/compare/chrome-devtools-mcp-v0.20.0...chrome-devtools-mcp-v0.20.1) (2026-03-16)


### 🛠️ Fixes

* update VS Code manual installation powershell command ([#1151](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1151)) ([6c64a5b](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/6c64a5b543714796b25a12dc6f2be7a1e683e8bd))


### ⚡ Performance

* use CDP to find open DevTools pages. ([#1150](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1150)) ([94de19c](https://github.com/ChromeDevTools/chrome-d…

## Recent Commits

- 2026-04-21 a1612be Nicholas Roscino: test: refactor tests to reduce duplication (#1926)
- 2026-04-21 42be7c3 Alex Rudenko: docs: clarify resource limitations around the number of tabs (#1927)
- 2026-04-21 b53752d Wolfgang Beyer: chore: move resolveCdpElementId (#1923)
- 2026-04-21 f0da776 browser-automation-bot: chore(main): release chrome-devtools-mcp 0.22.0 (#1884)
- 2026-04-21 76ab9fa Alex Rudenko: docs: clarify tools included into CLI (#1925)
- 2026-04-21 3ff21cf Nicholas Roscino: feat: support Chrome extensions debugging (#1922)
- 2026-04-21 86ffd58 Nicholas Roscino: test: add test for console log from content script (#1920)
- 2026-04-20 57648b7 Alex Rudenko: chore(deps): update lh (#1913)
- 2026-04-20 9211c6b Nikolay Vitkov: chore(memory): expose a tool for getting the inital data. (#1909)
- 2026-04-20 ec895f1 Nicholas Roscino: refactor: use puppeteer Extension API (#1911)
- 2026-04-20 562c308 dependabot[bot]: chore(deps-dev): bump the dev-dependencies group with 2 updates (#1907)
- 2026-04-20 3a24d71 Mukunda Rao Katta: test: save WebP responses with the right extension (#1901)
- 2026-04-20 e3a5f6b Cocoon-Break: fix(cli): correct WebP MIME type check in handleResponse ('webp' → 'image/webp') (#1899)
- 2026-04-20 0f29acf Alex Rudenko: chore: fix viewport eval (#1888)
- 2026-04-20 da33cb5 Nikolay Vitkov: feat: auto handle dialogs during script evaluation  (#1839)
- 2026-04-20 0ed086e Nikolay Vitkov: chore: remove code around Audits setup (#1893)
- 2026-04-17 0a6aaa5 yulunz: chore: generate a json file for flag usage metrics (#1881)
- 2026-04-17 0331f6a Nikolay Vitkov: chore: implement memory snapshot information (#1874)
- 2026-04-17 ea57e86 Asish Kumar: fix: ignore unmapped PerformanceIssue events (#1852)
- 2026-04-17 2f458c1 Nikolay Vitkov: fix(network): trailing data in Network redirect chain (#1880)

## Open Issues (top 10)

- #1912 Unable to read the Google Sheet Web Page (by maxsxu)
- #1921 Browser hangs / crashes when MCP connects to Chrome with many tabs (by jabagawee)
- #1775 Feature: Add evaluate_script_file tool to evaluate JavaScript files from the local filesystem (by achideal)

## Recently Merged PRs (top 10)

- #1926 test: refactor tests to reduce duplication (merged 2026-04-21)
- #1927 docs: clarify resource limitations around the number of tabs (merged 2026-04-21)
- #1923 chore: move resolveCdpElementId (merged 2026-04-21)
- #1884 chore(main): release chrome-devtools-mcp 0.22.0 (merged 2026-04-21)
- #1925 docs: clarify tools included into CLI (merged 2026-04-21)
- #1922 feat: support Chrome extensions debugging (merged 2026-04-21)
- #1920 test: add test for console log from content script (merged 2026-04-21)
- #1913 chore(deps): update lh (merged 2026-04-20)
- #1909 chore(memory): expose a tool for getting the inital data. (merged 2026-04-20)
- #1022 feat: add pageId routing for parallel multi-agent workflows (merged 2026-02-26)


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


## File: LICENSE

```

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```


## File: package-lock.json

```
{
  "name": "chrome-devtools-mcp",
  "version": "0.22.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "chrome-devtools-mcp",
      "version": "0.22.0",
      "license": "Apache-2.0",
      "bin": {
        "chrome-devtools": "build/src/bin/chrome-devtools.js",
        "chrome-devtools-mcp": "build/src/bin/chrome-devtools-mcp.js"
      },
      "devDependencies": {
        "@eslint/js": "^9.35.0",
        "@google/genai": "^1.37.0",
        "@modelcontextprotocol/sdk": "1.29.0",
        "@rollup/plugin-commonjs": "^29.0.0",
        "@rollup/plugin-json": "^6.1.0",
        "@rollup/plugin-node-resolve": "^16.0.3",
        "@stylistic/eslint-plugin": "^5.4.0",
        "@types/debug": "^4.1.12",
        "@types/filesystem": "^0.0.36",
        "@types/node": "^25.0.0",
        "@types/semver": "^7.7.1",
        "@types/sinon": "^21.0.0",
        "@types/yargs": "^17.0.33",
        "@typescript-eslint/eslint-plugin": "^8.43.0",
        "@typescript-eslint/parser": "^8.43.0",
        "chrome-devtools-frontend": "1.0.1613625",
        "core-js": "3.49.0",
        "debug": "4.4.3",
        "eslint": "^9.35.0",
        "eslint-import-resolver-typescript": "^4.4.4",
        "eslint-plugin-import": "^2.32.0",
        "globals": "^17.0.0",
        "lighthouse": "13.1.0",
        "prettier": "^3.6.2",
        "puppeteer": "24.42.0",
        "rollup": "4.60.2",
        "rollup-plugin-cleanup": "^3.2.1",
        "rollup-plugin-license": "^3.6.0",
        "semver": "^7.7.4",
        "sinon": "^21.0.0",
        "tiktoken": "^1.0.22",
        "typescript": "^6.0.2",
        "typescript-eslint": "^8.43.0",
        "yargs": "18.0.0"
      },
      "engines": {
        "node": "^20.19.0 || ^22.12.0 || >=23"
      }
    },
    "node_modules/@babel/code-frame": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/code-frame/-/code-frame-7.27.1.tgz",
      "integrity": "sha512-cjQ7ZlQ0Mv3b47hABuTevyTuYN4i+loJKGeV9flcCgIK37cCXRh+L1bd3iBHlynerhQ7BhCkn2BPbQUL+rGqFg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-validator-identifier": "^7.27.1",
        "js-tokens": "^4.0.0",
        "picocolors": "^1.1.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-identifier": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-identifier/-/helper-validator-identifier-7.27.1.tgz",
      "integrity": "sha512-D2hP9eA+Sqx1kBZgzxZh0y1trbuU+JoDkiEwqhQ36nodYqJwyEIhPSdMNd7lOm/4io72luTPWH20Yda0xOuUow==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@emnapi/core": {
      "version": "1.5.0",
      "resolved": "https://registry.npmjs.org/@emnapi/core/-/core-1.5.0.tgz",
      "integrity": "sha512-sbP8GzB1WDzacS8fgNPpHlp6C9VZe+SJP3F90W9rLemaQj2PzIuTEl1qDOYQf58YIpyjViI24y9aPWCjEzY2cg==",
      "dev": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "@emnapi/wasi-threads": "1.1.0",
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@emnapi/runtime": {
      "version": "1.5.0",
      "resolved": "https://registry.npmjs.org/@emnapi/runtime/-/runtime-1.5.0.tgz",
      "integrity": "sha512-97/BJ3iXHww3djw6hYIfErCZFee7qCtrneuLa20UXFCOTCfBM2cvQHjWJ2EG0s0MtdNwInarqCTz35i4wWXHsQ==",
      "dev": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@emnapi/wasi-threads": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/@emnapi/wasi-threads/-/wasi-threads-1.1.0.tgz",
      "integrity": "sha512-WI0DdZ8xFSbgMjR1sFsKABJ/C5OnRrjT06JXbZKexJGrDuPTzZdDYfFlsgcCXCyf+suG5QU2e/y1Wo2V/OapLQ==",
      "dev": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@eslint-community/eslint-utils": {
      "version": "4.9.1",
      "resolved": "https://registry.npmjs.org/@eslint-community/eslint-utils/-/eslint-utils-4.9.1.tgz",
      "integrity": "sha512-phrYmNiYppR7znFEdqgfWHXR6NCkZEK7hwWDHZUjit/2/U0r6XvkDl0SYnoM51Hq7FhCGdLDT6zxCCOY1hexsQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "eslint-visitor-keys": "^3.4.3"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      },
      "peerDependencies": {
        "eslint": "^6.0.0 || ^7.0.0 || >=8.0.0"
      }
    },
    "node_modules/@eslint-community/eslint-utils/node_modules/eslint-visitor-keys": {
      "version": "3.4.3",
      "resolved": "https://registry.npmjs.org/eslint-visitor-keys/-/eslint-visitor-keys-3.4.3.tgz",
      "integrity": "sha512-wpc+LXeiyiisxPlEkUzU6svyS1frIO3Mgxj1fdy7Pm8Ygzguax2N3Fa/D/ag1WqbOprdI+uY6wMUl8/a2G+iag==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/@eslint-community/regexpp": {
      "version": "4.12.2",
      "resolved": "https://registry.npmjs.org/@eslint-community/regexpp/-/regexpp-4.12.2.tgz",
      "integrity": "sha512-EriSTlt5OC9/7SXkRSCAhfSxxoSUgBm33OH+IkwbdpgoqsSsUg7y3uh+IICI/Qg4BBWr3U2i39RpmycbxMq4ew==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "^12.0.0 || ^14.0.0 || >=16.0.0"
      }
    },
    "node_modules/@eslint/config-array": {
      "version": "0.21.2",
      "resolved": "https://registry.npmjs.org/@eslint/config-array/-/config-array-0.21.2.tgz",
      "integrity": "sha512-nJl2KGTlrf9GjLimgIru+V/mzgSK0ABCDQRvxw5BjURL7WfH5uoWmizbH7QB6MmnMBd8cIC9uceWnezL1VZWWw==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@eslint/object-schema": "^2.1.7",
        "debug": "^4.3.1",
        "minimatch": "^3.1.5"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      }
    },
    "node_modules/@eslint/config-array/node_modules/brace-expansion": {
      "version": "1.1.13",
      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-1.1.13.tgz",
      "integrity": "sha512-9ZLprWS6EENmhEOpjCYW2c8VkmOvckIJZfkr7rBW6dObmfgJ/L1GpSYW5Hpo9lDz4D1+n0Ckz8rU7FwHDQiG/w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "balanced-match": "^1.0.0",
        "concat-map": "0.0.1"
      }
    },
    "node_modules/@eslint/config-array/node_modules/minimatch": {
      "version": "3.1.5",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-3.1.5.tgz",
      "integrity": "sha512-VgjWUsnnT6n+NUk6eZq77zeFdpW2LWDzP6zFGrCbHXiYNul5Dzqk2HHQ5uFH2DNW5Xbp8+jVzaeNt94ssEEl4w==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "brace-expansion": "^1.1.7"
      },
      "engines": {
        "node": "*"
      }
    },
    "node_modules/@eslint/config-helpers": {
      "version": "0.4.2",
      "resolved": "https://registry.npmjs.org/@eslint/config-helpers/-/config-helpers-0.4.2.tgz",
      "integrity": "sha512-gBrxN88gOIf3R7ja5K9slwNayVcZgK6SOUORm2uBzTeIEfeVaIhOpCtTox3P6R7o2jLFwLFTLnC7kU/RGcYEgw==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@eslint/core": "^0.17.0"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      }
    },
    "node_modules/@eslint/core": {
      "version": "0.17.0",
      "resolved": "https://registry.npmjs.org/@eslint/core/-/core-0.17.0.tgz",
      "integrity": "sha512-yL/sLrpmtDaFEiUj1osRP4TI2MDz1AddJL+jZ7KSqvBuliN4xqYY54IfdN8qD8Toa6g1iloph1fxQNkjOxrrpQ==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@types/json-schema": "^7.0.15"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      }
    },
    "node_modules/@eslint/eslintrc": {
      "version": "3.3.5",
      "resolved": "https://registry.npmjs.org/@eslint/eslintrc/-/eslintrc-3.3.5.tgz",
      "integrity": "sha512-4IlJx0X0qftVsN5E+/vGujTRIFtwuLbNsVUe7TO6zYPDR1O6nFwvwhIKEKSrl6dZchmYBITazxKoUYOjdtjlRg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ajv": "^6.14.0",
        "debug": "^4.3.2",
        "espree": "^10.0.1",
        "globals": "^14.0.0",
        "ignore": "^5.2.0",
        "import-fresh": "^3.2.1",
        "js-yaml": "^4.1.1",
        "minimatch": "^3.1.5",
        "strip-json-comments": "^3.1.1"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/@eslint/eslintrc/node_modules/brace-expansion": {
      "version": "1.1.13",
      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-1.1.13.tgz",
      "integrity": "sha512-9ZLprWS6EENmhEOpjCYW2c8VkmOvckIJZfkr7rBW6dObmfgJ/L1GpSYW5Hpo9lDz4D1+n0Ckz8rU7FwHDQiG/w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "balanced-match": "^1.0.0",
        "concat-map": "0.0.1"
      }
    },
    "node_modules/@eslint/eslintrc/node_modules/globals": {
      "version": "14.0.0",
      "resolved": "https://registry.npmjs.org/globals/-/globals-14.0.0.tgz",
      "integrity": "sha512-oahGvuMGQlPw/ivIYBjVSrWAfWLBeku5tpPE2fOPLi+WHffIWbuh2tCjhyQhTBPMf5E9jDEH4FOmTYgYwbKwtQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/@eslint/eslintrc/node_modules/ignore": {
      "version": "5.3.2",
      "resolved": "https://registry.npmjs.org/ignore/-/ignore-5.3.2.tgz",
      "integrity": "sha512-hsBTNUqQTDwkWtcdYI2i06Y/nUBEsNEDJKjWdigLvegy8kDuJAS8uRlpkkcQpyEXL0Z/pjDy5HBmMjRCJ2gq+g==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 4"
      }
    },
    "node_modules/@eslint/eslintrc/node_modules/minimatch": {
      "version": "3.1.5",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-3.1.5.tgz",
      "integrity": "sha512-VgjWUsnnT6n+NUk6eZq77zeFdpW2LWDzP6zFGrCbHXiYNul5Dzqk2HHQ5uFH2DNW5Xbp8+jVzaeNt94ssEEl4w==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "brace-expansion": "^1.1.7"
      },
      "engines": {
        "node": "*"
      }
    },
    "node_modules/@eslint/js": {
      "version": "9.39.4",
      "resolved": "https://registry.npmjs.org/@eslint/js/-/js-9.39.4.tgz",
      "integrity": "sha512-nE7DEIchvtiFTwBw4Lfbu59PG+kCofhjsKaCWzxTpt4lfRjRMqG6uMBzKXuEcyXhOHoUp9riAm7/aWYGhXZ9cw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "url": "https://eslint.org/donate"
      }
    },
    "node_modules/@eslint/object-schema": {
      "version": "2.1.7",
      "resolved": "https://registry.npmjs.org/@eslint/object-schema/-/object-schema-2.1.7.tgz",
      "integrity": "sha512-VtAOaymWVfZcmZbp6E2mympDIHvyjXs/12LqWYjVw6qjrfF+VK+fyG33kChz3nnK+SU5/NeHOqrTEHS8sXO3OA==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      }
    },
    "node_modules/@eslint/plugin-kit": {
      "version": "0.4.1",
      "resolved": "https://registry.npmjs.org/@eslint/plugin-kit/-/plugin-kit-0.4.1.tgz",
      "integrity": "sha512-43/qtrDUokr7LJqoF2c3+RInu/t4zfrpYdoSDfYyhg52rwLV6TnOvdG4fXm7IkSB3wErkcmJS9iEhjVtOSEjjA==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@eslint/core": "^0.17.0",
        "levn": "^0.4.1"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      }
    },
    "node_modules/@formatjs/ecma402-abstract": {
      "version": "2.3.6",
      "resolved": "https://registry.npmjs.org/@formatjs/ecma402-abstract/-/ecma402-abstract-2.3.6.tgz",
      "integrity": "sha512-HJnTFeRM2kVFVr5gr5kH1XP6K0JcJtE7Lzvtr3FS/so5f1kpsqqqxy5JF+FRaO6H2qmcMfAUIox7AJteieRtVw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@formatjs/fast-memoize": "2.2.7",
        "@formatjs/intl-localematcher": "0.6.2",
        "decimal.js": "^10.4.3",
        "tslib": "^2.8.0"
      }
    },
    "node_modules/@formatjs/fast-memoize": {
      "version": "2.2.7",
      "resolved": "https://registry.npmjs.org/@formatjs/fast-memoize/-/fast-memoize-2.2.7.tgz",
      "integrity": "sha512-Yabmi9nSvyOMrlSeGGWDiH7rf3a7sIwplbvo/dlz9WCIjzIQAfy1RMf4S0X3yG724n5Ghu2GmEl5NJIV6O9sZQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "tslib": "^2.8.0"
      }
    },
    "node_modules/@formatjs/icu-messageformat-parser": {
      "version": "2.11.4",
      "resolved": "https://registry.npmjs.org/@formatjs/icu-messageformat-parser/-/icu-messageformat-parser-2.11.4.tgz",
      "integrity": "sha512-7kR78cRrPNB4fjGFZg3Rmj5aah8rQj9KPzuLsmcSn4ipLXQvC04keycTI1F7kJYDwIXtT2+7IDEto842CfZBtw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@formatjs/ecma402-abstract": "2.3.6",
        "@formatjs/icu-skeleton-parser": "1.8.16",
        "tslib": "^2.8.0"
      }
    },
    "node_modules/@formatjs/icu-skeleton-parser": {
      "version": "1.8.16",
      "resolved": "https://registry.npmjs.org/@formatjs/icu-skeleton-parser/-/icu-skeleton-parser-1.8.16.tgz",
      "integrity": "sha512-H13E9Xl+PxBd8D5/6TVUluSpxGNvFSlN/b3coUp0e0JpuWXXnQDiavIpY3NnvSp4xhEMoXyyBvVfdFX8jglOHQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@formatjs/ecma402-abstract": "2.3.6",
        "tslib": "^2.8.0"
      }
    },
    "node_modules/@formatjs/intl-localematcher": {
      "version": "0.6.2",
      "resolved": "https://registry.npmjs.org/@formatjs/intl-localematcher/-/intl-localematcher-0.6.2.tgz",
      "integrity": "sha512-XOMO2Hupl0wdd172Y06h6kLpBz6Dv+J4okPLl4LPtzbr8f66WbIoy4ev98EBuZ6ZK4h5ydTN6XneT4QVpD7cdA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "tslib": "^2.8.0"
      }
    },
    "node_modules/@google/genai": {
      "version": "1.50.1",
      "resolved": "https://registry.npmjs.org/@google/genai/-/genai-1.50.1.tgz",
      "integrity": "sha512-YbkX7H9+1Pt8wOt7DDREy8XSoiL6fRDzZQRyaVBarFf8MR3zHGqVdvM4cLbDXqPhxqvegZShgfxb8kw9C7YhAQ==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "google-auth-library": "^10.3.0",
        "p-retry": "^4.6.2",
        "protobufjs": "^7.5.4",
        "ws": "^8.18.0"
      },
      "engines": {
        "node": ">=20.0.0"
      },
      "peerDependencies": {
        "@modelcontextprotocol/sdk": "^1.25.2"
      },
      "peerDependenciesMeta": {
        "@modelcontextprotocol/sdk": {
          "optional": true
        }
      }
    },
    "node_modules/@hono/node-server": {
      "version": "1.19.13",
      "resolved": "https://registry.npmjs.org/@hono/node-server/-/node-server-1.19.13.tgz",
      "integrity": "sha512-TsQLe4i2gvoTtrHje625ngThGBySOgSK3Xo2XRYOdqGN1teR8+I7vchQC46uLJi8OF62YTYA3AhSpumtkhsaKQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18.14.1"
      },
      "peerDependencies": {
        "hono": "^4"
      }
    },
    "node_modules/@humanfs/core": {
      "version": "0.19.1",
      "resolved": "https://registry.npmjs.org/@humanfs/core/-/core-0.19.1.tgz",
      "integrity": "sha512-5DyQ4+1JEUzejeK1JGICcideyfUbGixgS9jNgex5nqkW+cY7WZhxBigmieN5Qnw9ZosSNVC9KQKyb+GUaGyKUA==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": ">=18.18.0"
      }
    },
    "node_modules/@humanfs/node": {
      "version": "0.16.7",
      "resolved": "https://registry.npmjs.org/@humanfs/node/-/node-0.16.7.tgz",
      "integrity": "sha512-/zUx+yOsIrG4Y43Eh2peDeKCxlRt/gET6aHfaKpu
```


## File: package.json

```
{
  "name": "chrome-devtools-mcp",
  "version": "0.22.0",
  "description": "MCP server for Chrome DevTools",
  "type": "module",
  "bin": {
    "chrome-devtools-mcp": "./build/src/bin/chrome-devtools-mcp.js",
    "chrome-devtools": "./build/src/bin/chrome-devtools.js"
  },
  "main": "./build/src/index.js",
  "scripts": {
    "cli:generate": "node --experimental-strip-types scripts/generate-cli.ts",
    "clean": "node -e \"require('fs').rmSync('build', {recursive: true, force: true})\"",
    "bundle": "npm run clean && npm run build && rollup -c rollup.config.mjs && node -e \"require('fs').rmSync('build/node_modules', {recursive: true, force: true})\" && node --experimental-strip-types scripts/append-lighthouse-notices.ts",
    "build": "tsc && node --experimental-strip-types --no-warnings=ExperimentalWarning scripts/post-build.ts",
    "typecheck": "tsc --noEmit",
    "format": "eslint --cache --fix . && prettier --write --cache .",
    "check-format": "eslint --cache . && prettier --check --cache .;",
    "gen": "npm run build && npm run docs:generate && npm run cli:generate && npm run update-tool-call-metrics && npm run update-flag-usage-metrics && npm run format",
    "docs:generate": "node --experimental-strip-types scripts/generate-docs.ts",
    "start": "npm run build && node build/src/index.js",
    "start-debug": "DEBUG=mcp:* DEBUG_COLORS=false npm run build && node build/src/index.js",
    "test": "npm run build && node scripts/test.mjs",
    "test:no-build": "node scripts/test.mjs",
    "test:only": "npm run build && node scripts/test.mjs --test-only",
    "test:update-snapshots": "npm run build && node scripts/test.mjs --test-update-snapshots",
    "prepare": "node --experimental-strip-types scripts/prepare.ts",
    "verify-server-json-version": "node --experimental-strip-types scripts/verify-server-json-version.ts",
    "update-lighthouse": "node --experimental-strip-types scripts/update-lighthouse.ts",
    "update-tool-call-metrics": "node --experimental-strip-types scripts/update_tool_call_metrics.ts",
    "update-flag-usage-metrics": "node --experimental-strip-types scripts/update_flag_usage_metrics.ts",
    "verify-npm-package": "node scripts/verify-npm-package.mjs",
    "eval": "npm run build && node --experimental-strip-types scripts/eval_gemini.ts",
    "count-tokens": "node --experimental-strip-types scripts/count_tokens.ts"
  },
  "files": [
    "build/src",
    "LICENSE",
    "!*.tsbuildinfo"
  ],
  "repository": "ChromeDevTools/chrome-devtools-mcp",
  "author": "Google LLC",
  "license": "Apache-2.0",
  "bugs": {
    "url": "https://github.com/ChromeDevTools/chrome-devtools-mcp/issues"
  },
  "homepage": "https://github.com/ChromeDevTools/chrome-devtools-mcp#readme",
  "mcpName": "io.github.ChromeDevTools/chrome-devtools-mcp",
  "devDependencies": {
    "@eslint/js": "^9.35.0",
    "@google/genai": "^1.37.0",
    "@modelcontextprotocol/sdk": "1.29.0",
    "@rollup/plugin-commonjs": "^29.0.0",
    "@rollup/plugin-json": "^6.1.0",
    "@rollup/plugin-node-resolve": "^16.0.3",
    "@stylistic/eslint-plugin": "^5.4.0",
    "@types/debug": "^4.1.12",
    "@types/filesystem": "^0.0.36",
    "@types/node": "^25.0.0",
    "@types/semver": "^7.7.1",
    "@types/sinon": "^21.0.0",
    "@types/yargs": "^17.0.33",
    "@typescript-eslint/eslint-plugin": "^8.43.0",
    "@typescript-eslint/parser": "^8.43.0",
    "chrome-devtools-frontend": "1.0.1613625",
    "core-js": "3.49.0",
    "debug": "4.4.3",
    "eslint": "^9.35.0",
    "eslint-import-resolver-typescript": "^4.4.4",
    "eslint-plugin-import": "^2.32.0",
    "globals": "^17.0.0",
    "lighthouse": "13.1.0",
    "prettier": "^3.6.2",
    "puppeteer": "24.42.0",
    "rollup": "4.60.2",
    "rollup-plugin-cleanup": "^3.2.1",
    "rollup-plugin-license": "^3.6.0",
    "semver": "^7.7.4",
    "sinon": "^21.0.0",
    "tiktoken": "^1.0.22",
    "typescript": "^6.0.2",
    "typescript-eslint": "^8.43.0",
    "yargs": "18.0.0"
  },
  "engines": {
    "node": "^20.19.0 || ^22.12.0 || >=23"
  }
}

```


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

The CLI only supports tools available in the MCP server without additional arguments (see [Tool reference](./tool-reference.md)).
Thus, `--categoryExtensions` tools are currently not available in the CLI.

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
- **[Extensions](#extensions)** (5 tools)
  - [`install_extension`](#install_extension)
  - [`list_extensions`](#list_extensions)
  - [`reload_extension`](#reload_extension)
  - [`trigger_extension_action`](#trigger_extension_action)
  - [`uninstall_extension`](#uninstall_extension)
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
- **geolocation** (string) _(optional)_: Geolocation (`&lt;latitude&gt;x&lt;longitude&gt;`) to [`emulate`](#emulate). Latitude between -90 and 90. Longitude between -180 and 180. Omit to clear the geolocation override.
- **networkConditions** (enum: "Offline", "Slow 3G", "Fast 3G", "Slow 4G", "Fast 4G") _(optional)_: Throttle network. Omit to disable throttling.
- **userAgent** (string) _(optional)_: User agent to [`emulate`](#emulate). Set to empty string to clear the user agent override.
- **viewport** (string) _(optional)_: [`Emulate`](#emulate) device viewports '&lt;width&gt;x&lt;height&gt;x&lt;devicePixelRatio&gt;[,mobile][,touch][,landscape]'. 'touch' and 'mobile' to [`emulate`](#emulate) mobile devices. 'landscape' to [`emulate`](#emulate) landscape mode.

---

### `resize_page`

**Description:** Resizes the selected page's window so that the page has specified dimension

**Parameters:**

- **height** (number) **(required)**: Page height
- **width** (number) **(required)**: Page width

---

## Performance

### `performance_analyze_insight`

**Description:** Provides more detailed information on a specific Performance Insight of an insight set that was highlighted in the results of a trace recording.

**Parameters:**

- **insightName** (string) **(required)**: The name of the Insight you want more information on. For example: "DocumentLatency" or "LCPBreakdown"
- **insightSetId** (string) **(required)**: The id for the specific insight set. Only use the ids given in the "Available insight sets" list.

---

### `performance_start_trace`

**Description:** Start a performance trace on the selected webpage. Use to find frontend performance issues, Core Web Vitals (LCP, INP, CLS), and improve page load speed.

**Parameters:**

- **autoStop** (boolean) _(optional)_: Determines if the trace recording should be automatically stopped.
- **filePath** (string) _(optional)_: The absolute file path, or a file path relative to the current working directory, to save the raw trace data. For example, trace.json.gz (compressed) or trace.json (uncompressed).
- **reload** (boolean) _(optional)_: Determines if, once tracing has started, the current selected page should be automatically reloaded. Navigate the page to the right URL using the [`navigate_page`](#navigate_page) tool BEFORE starting the trace if reload or autoStop is set to true.

---

### `performance_stop_trace`

**Description:** Stop the active performance trace recording on the selected webpage.

**Parameters:**

- **filePath** (string) _(optional)_: The absolute file path, or a file path relative to the current working directory, to save the raw trace data. For example, trace.json.gz (compressed) or trace.json (uncompressed).

---

## Network

### `get_network_request`

**Description:** Gets a network request by an optional reqid, if omitted returns the currently selected request in the DevTools Network panel.

**Parameters:**

- **reqid** (number) _(optional)_: The reqid of the network request. If omitted returns the currently selected request in the DevTools Network panel.
- **requestFilePath** (string) _(optional)_: The absolute or relative path to a .network-request file to save the request body to. If omitted, the body is returned inline.
- **responseFilePath** (string) _(optional)_: The absolute or relative path to a .network-response file to save the response body to. If omitted, the body is returned inline.

---

### `list_network_requests`

**Description:** List all requests for the currently selected page since the last navigation.

**Parameters:**

- **includePreservedRequests** (boolean) _(optional)_: Set to true to return the preserved requests over the last 3 navigations.
- **pageIdx** (integer) _(optional)_: Page number to return (0-based). When omitted, returns the first page.
- **pageSize** (integer) _(optional)_: Maximum number of requests to return. When omitted, returns all requests.
- **resourceTypes** (array) _(optional)_: Filter requests to only return requests of the specified resource types. When omitted or empty, returns all requests.

---

## Debugging

### `evaluate_script`

**Description:** Evaluate a JavaScript function inside the currently selected page. Returns the response as JSON,
so returned values have to be JSON-serializable.

**Parameters:**

- **function** (string) **(required)**: A JavaScript function declaration to be executed by the tool in the currently selected page.
  Example without arguments: `() => {
  return document.title
}` or `async () => {
  return await fetch("example.com")
}`.
  Example with arguments: `(el) => {
  return el.innerText;
}`

- **args** (array) _(optional)_: An optional list of arguments to pass to the function.
- **dialogAction** (string) _(optional)_: Handle dialogs while execution. "accept", "dismiss", or string for response of window.prompt. Defaults to accept.

---

### `get_console_message`

**Description:** Gets a console message by its ID. You can get all messages by calling [`list_console_messages`](#list_console_messages).

**Parameters:**

- **msgid** (number) **(required)**: The msgid of a console message on the page from the listed console messages

---

### `lighthouse_audit`

**Description:** Get Lighthouse score and reports for accessibility, SEO and best practices. This excludes performance. For performance audits, run [`performance_start_trace`](#performance_start_trace)

**Parameters:**

- **device** (enum: "desktop", "mobile") _(optional)_: Device to [`emulate`](#emulate).
- **mode** (enum: "navigation", "snapshot") _(optional)_: "navigation" reloads &amp; audits. "snapshot" analyzes current state.
- **outputDirPath** (string) _(optional)_: Directory for reports. If omitted, uses temporary files.

---

### `list_console_messages`

**Description:** List all console messages for the currently selected page since the last navigation.

**Parameters:**

- **includePreservedMessages** (boolean) _(optional)_: Set to true to return the preserved messages over the last 3 navigations.
- **pageIdx** (integer) _(optional)_: Page number to return (0-based). When omitted, returns the first page.
- **pageSize** (integer) _(optional)_: Maximum number of messages to return. When omitted, returns all messages.
- **types** (array) _(optional)_: Filter messages to only return messages of the specified resource types. When omitted or empty, returns all messages.

---

### `take_screenshot`

**Description:** Take a screenshot of the page or element.

**Parameters:**

- **filePath** (string) _(optional)_: The absolute path, or a path relative to the current working directory, to save the screenshot to instead of attaching it to the response.
- **format** (enum: "png", "jpeg", "webp") _(optional)_: Type of format to save the screenshot as. Default is "png"
- **fullPage** (boolean) _(optional)_: If set to true takes a screenshot of the full page instead of the currently visible viewport. Incompatible with uid.
- **quality** (number) _(optional)_: Compression quality for JPEG and WebP formats (0-100). Higher values mean better quality but larger file sizes. Ignored for PNG format.
- **uid** (string) _(optional)_: The uid of an element on the page from the page content snapshot. If omitted, takes a page screenshot.

---

### `take_snapshot`

**Description:** Take a text snapshot of the currently selected page based on the a11y tree. The snapshot lists page elements along with a unique
identifier (uid). Always use the latest snapshot. Prefer taking a snapshot over taking a screenshot. The snapshot indicates the element selected
in the DevTools Elements panel (if any).

**Parameters:**

- **filePath** (string) _(optional)_: The absolute path, or a path relative to the current working directory, to save the snapshot to instead of attaching it to the response.
- **verbose** (boo
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

> [!IMPORTANT]
> In Chrome versions up to 149, connection issues may be caused by frozen or unloaded tabs.
> Chrome DevTools MCP forces all tabs to be loaded, so ensure your system has sufficient resources.
> It is currently not recommended to use Chrome DevTools MCP with browser instances running hundreds of tabs.
> See [Issue #1921](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1921) for more details.

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
  ".": "0.22.0"
}

```


## File: CHANGELOG.md

```
# Changelog

## [0.22.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/compare/chrome-devtools-mcp-v0.21.0...chrome-devtools-mcp-v0.22.0) (2026-04-21)


### 🎉 Features

* add update notification to both binaries ([#1783](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1783)) ([e01e333](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/e01e33355e85c3b38e7aba6aceff57271b99a830))
* auto handle dialogs during script evaluation  ([#1839](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1839)) ([da33cb5](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/da33cb5b957fb87bbbab67e4c1521535065881f1))
* ensure extensions for file outputs ([#1867](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1867)) ([e7a0d50](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/e7a0d509778578ceb8ba357f5857a86f95cfb533))
* experimental click_at(x,y) tool ([#1788](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1788)) ([c4f5471](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/c4f54710d9d7c3d1167628e5135b4cf92beaec45))
* support Chrome extensions debugging ([#1922](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1922)) ([3ff21cf](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/3ff21cf30dae19a6af85d836b1b55314f53ff401))
* support DevTools header redactions as an option ([#1848](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1848)) ([5c398c4](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/5c398c4e7ce17facf62316fb1b617c39daa461ef))
* **webmcp:** Add experimental tool to execute WebMCP tool ([#1873](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1873)) ([0aff266](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/0aff266111408acfbce39e231c23ce866d0f26c0))
* **webmcp:** Add experimental tool to list WebMCP tools page exposes ([#1845](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1845)) ([f97b573](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/f97b573d70ec670df8bb2b42167e08681f3b488e))


### 🛠️ Fixes

* avoid showing update notification for local builds ([#1889](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1889)) ([3f0cf10](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/3f0cf1068ba35d81c800a81fc6272acaff715b41)), closes [#1886](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1886)
* **cli:** correct WebP MIME type check in handleResponse ('webp' → 'image/webp') ([#1899](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1899)) ([e3a5f6b](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/e3a5f6bb69f0dc4e626146d5b4165af97bad8fe4)), closes [#1898](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1898)
* ignore unmapped PerformanceIssue events ([#1852](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1852)) ([ea57e86](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/ea57e863f8b5b48a210c7a2fccd552f5824a7a96))
* **network:** trailing data in Network redirect chain ([#1880](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1880)) ([2f458c1](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/2f458c11ebbb4b8061e8e4375346e5449b222281))
* remove double space in navigate error message ([#1847](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1847)) ([429e0ca](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/429e0ca7b82568de1c0fab27dacb439b3898965c))


### 📄 Documentation

* clarify tools included into CLI ([#1925](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1925)) ([76ab9fa](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/76ab9fa5643dfa6eb93fcb50fe747a948e9a9d63))
* document network response and request extensions ([#1887](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1887)) ([796d6f2](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/796d6f2e242065de1e2cf27f729d66bc71676299))
* fix skill and reference documentation issues ([#1249](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1249)) ([9236834](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/92368345dd62fce0a65a1081f80c23790edbf7d1))
* Include Mistral Vibe setup in README ([#1801](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1801)) ([582c9e0](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/582c9e01e9a5ca1b9bb9e4b816662008430aaf2d))
* Rename project and enhance README content ([#1856](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1856)) ([c066488](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/c0664883a5eb6a3e23bb0a48ea348e5cdab052f2))
* update the README on installing as a VS code agent plugin  ([#1796](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1796)) ([1b5dcae](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/1b5dcae2a03a9de8c29c9f25a4d04cdfbad416a7))


### 🏗️ Refactor

* move waitForEventsAfterAction to McpPage ([#1780](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1780)) ([c7c8f50](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/c7c8f50f802643fd90bd9d0419acfb1bb8dd58ad))
* use puppeteer Extension API ([#1911](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1911)) ([ec895f1](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/ec895f195aa21b36c1bf4373184f281b181ea3e9))

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

## [0.20.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/compare/chrome-devtools-mcp-v0.19.0...chrome-devtools-mcp-v0.20.0) (2026-03-11)


### 🎉 Features

* experimental `chrome-devtools` CLI ([#1100](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1100)) ([1ac574e](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/1ac574e7154948e86e414e5149fb975a190d5bb0))


### 📄 Documentation

* fix typo ([#1155](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1155)) ([b59cabc](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/b59cabcc1d59802ffd7d9667040188e46192357d))
* fix typos and improve phrasing ([#1130](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1130)) ([70d4f36](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/70d4f365dc619a5743e697c30800f7065bc6227d))
* revise contribution process and add release process ([#1134](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1134)) ([d7d26a1](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/d7d26a103b840e2feb7cb9af6a242edda94f1ddf))
* **troubleshooting:** add symptom for missing tools due to read-only mode ([#1148](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1148)) ([57e7d51](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/57e7d51e8ca1e2ee325a9e7a9c64c033acbe6d6a))
* Update troubleshooting for MCP server connection errors ([#1017](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1017)) ([00f9c31](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/00f9c3108ab9caefca57998439052c728298920b))


### 🏗️ Refactor

* move main files ([#1120](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1120)) ([c2d8009](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/c2d8009ff75f76bce1ec4cf79c2467b50d81725e))

## [0.19.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/compare/chrome-devtools-mcp-v0.18.1...chrome-devtools-mcp-v0.19.0) (2026-03-05)


### 🎉 Features

* add pageId routing for parallel multi-agent workflows ([#1022](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1022)) ([caf601a](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/caf601a32832bb87cfac801a6bbeacb87508412f)), closes [#1019](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1019)
* Add skill which helps with onboarding of the mcp server ([#1083](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1083)) ([7273f16](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/7273f16ec08f6d5b46a2693b0ad4d559086ded89))
* integrate Lighthouse audits ([#831](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/831)) ([dfdac26](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/dfdac2648e560d756a8711ad3bb1fa470be8e7c9))


### 🛠️ Fixes

* improve error messages around --auto-connect ([#1075](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1075)) ([bcb852d](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/bcb852dd2e440b0005f4a9ad270a1a7998767907))
* improve tool descriptions ([#965](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/965)) ([bdbbc84](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/bdbbc84c125bdd48f4be48aa476bec0323de611c))
* repair broken markdown and extract snippets in a11y-debugging skill ([#1096](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1096)) ([adac7c5](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/adac7c537ee304f324c5e7284fb363396d1773f5))
* simplify emulation and script tools ([#1073](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1073)) ([e51ba47](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/e51ba4720338951e621585b77efc6a0e07678d99))
* simplify focus state management ([#1063](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1063)) ([f763da2](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/f763da24a10e27605c0a5069853ce7c92974eec2))
* tweak lighthouse description ([#1112](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1112)) ([5538180](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/55381804ae7ffa8a1e5933b621a9b8390b3000ff))


### 📄 Documentation

* Adapt a11y skill to utilize Lighthouse ([#1054](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1054)) ([21634e6](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/21634e660c346e469ae62116b1824538f51567dd))
* add feature release checklist to CONTRIBUTING.md ([#1118](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1118)) ([0378457](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/03784577ffb6e238bcb2d637bff9ad759723ea7b))
* fix typo in README regarding slim mode ([#1093](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1093)) ([92f2c7b](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/92f2c7b48b56a6b1d6ac7c9e2f2e92beb26bcf62))


### 🏗️ Refactor

* clean up more of the context getters ([#1062](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1062)) ([9628dab](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/9628dabcb4d39f0b94d152a0fc419e049246a29d))
* consistently use McpPage in tools ([#1057](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1057)) ([302e5a0](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/302e5a04191ba0558e3c79f1486d01d5eb0f6896))
* improve type safety for page scoped tools ([#1051](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1051)) ([5f694c6](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/5f694c60ffd21f8b022554c92b2ad4cbdb457375))
* make cdp resolvers use McpPage ([#1060](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1060)) ([d6c06c5](https://github.com/ChromeDevTools/chrome-devtools-mcp/commit/d6c06c56a7b8e4968318adc9fc7c820ace9f5bd9))
* move dialog handling to McpPage ([#1059](https://github.com/ChromeDevTools/
```


(… 204 more files omitted due to size limit)
<!-- fetched-content:end -->
