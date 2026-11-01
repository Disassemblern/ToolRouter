# Gateway Functional Requirements

## 2.1 Functional Requirements

Prepared by: Buğra Kemal Korkut

The gateway connects the AI assistant to MCP servers. It collects the available
tools, asks the search engine to find suitable tools, and sends tool calls to
the correct server.

### FR-GW-01: Read server settings

The gateway must read the server list from a JSON file using the `mcpServers`
format. Each server must have a description.

### FR-GW-02: Connect to servers

The gateway must connect to MCP servers using stdio or Streamable HTTP.

### FR-GW-03: Create a tool catalog

The gateway must collect the servers' tools in one catalog. Each tool must have
an ID in the format `server__tool`, such as `github__create_issue`.

### FR-GW-04: Provide router mode

In router mode, the gateway must provide only two tools to the assistant:
`search_tools` and `call_tool`.

### FR-GW-05: Return search results

The `search_tools` tool must return suitable tools from the search engine.
It must return no more than the requested limit, which is 5 by default.
Each result must include the tool name, description, and input schema.

### FR-GW-06: Run a selected tool

The `call_tool` tool must send the selected tool's name and arguments to the
correct server. It must return the server's result to the assistant.

### FR-GW-07: Provide passthrough mode

In passthrough mode, the gateway must show all catalog tools directly to the
assistant. The assistant must be able to call them without using `search_tools`.

### FR-GW-08: Update the tool catalog

The gateway must update its catalog when a server reports that its tool list
has changed.

### FR-GW-09: Handle server failures

If a server fails, the gateway must leave out that server's tools and continue
working with the other servers.

### FR-GW-10: Save the catalog

The `toolrouter catalog dump` command must save the current tool catalog to a
JSON file.

### FR-GW-11: Send context to the search engine

The `search_tools` tool must take the assistant's query, goal, reason, and expected
result. The gateway must send these to the search engine with the setup
information from the configuration file.

### FR-GW-12: Leave out disabled tools

The gateway must leave out tools listed in a server's `disabledTools` setting.

### FR-GW-13: Keep request logs

When `--log-file` is used, the gateway must record each search and tool call in
a JSON-lines file. Tool argument values must not be written to the log.
