# Class 6: First MCP Tests

I used Python 3.12 and the MCP Python SDK (version 2.3.0).

1. I made a small server with one tool called `hello`. The client found and
   called the tool in the same Python process and then in a separate process
   using stdio. Both calls returned `Hello, ToolRouter!`.
2. I started the MCP filesystem server (version 2.2.0) with npx and gave it
   access to the test folder. The client listed 16 tools. I called
   `list_directory` and got `[FILE] example.txt`.

## How to run it

Open `spikes/gateway-class6` and install the dependency with
`python -m pip install -r requirements.txt` in a Python 3.12 environment.
Run `python check.py` for the small server. To also run the filesystem test,
use Node.js 24 or later and run `python check.py "path/to/npx-cli.js"`.
The script `npx-cli.js` is in npm's `bin` folder.
