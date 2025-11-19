# Clearcom-MCP-Server

The Clearcom MCP server

## Installation

Begin my installing UV:

### Linux or Mac:

- `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Windows

- `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

If you have any issues check the [UV documentation](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1)

## Running the server

1. First download the python packages required

   - `uv sync`

2. Run the MCP server
   - `uv run fastmcp run src/main.py:mcp`
