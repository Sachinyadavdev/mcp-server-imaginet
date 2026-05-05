For Running the MCP Server:

1. uv run python mcp_client_example.py -> Command with Ollama

2. uv run mcp install mcp_server/server.py -> for running into the claude

3. uv run mcp list -> List all the installed MCP servers

4. uv run mcp uninstall mcp_server/server.py -> Uninstall the MCP server

5. uv run mcp uninstall all -> Uninstall all the MCP servers

6. uv run mcp uninstall all -> Uninstall all the MCP servers

uv run uvicorn api_server.main:app --host 0.0.0.0 --port 8000 --reload

System Summary: GET http://localhost:8000/system-summary
EOD Reports: GET http://localhost:8000/eod-reports?limit=10

http://127.0.0.1:8000/docs

