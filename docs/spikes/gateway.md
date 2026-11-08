# Gateway Spike — Class 6

I used Python 3.12.15 and MCP Python SDK 2.3.0 for both checks.

- **Small server:** The client listed and called the `hello` tool in memory and
  over stdio. Both calls returned `Hello, ToolRouter!`.
- **Filesystem server:** The client connected over stdio to the reference server
  (`@modelcontextprotocol/server-filesystem@2.2.0`) started with npx. It listed
  16 tools. Calling `list_directory` in the test folder returned
  `[FILE] example.txt`.

## Run the checks

From `spikes/gateway-class6`, install `requirements.txt` in a Python 3.12
environment. Run `python check.py hello` for the small server. With Node.js 24
or later, run `python check.py filesystem --npx-script <path-to-npx-cli.js>` for
the filesystem check. The npx script is in the `bin` directory of npm.

The filesystem server only receives the included `sandbox` directory.
