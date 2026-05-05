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
Submit EOD: POST http://localhost:8000/submit-eod
JSON Body: {"employee_name": "sachin", "date": "2024-05-04", "description": "Worked on MCP server", "project_name": "Internal"}

http://127.0.0.1:8000/docs

http://localhost:8000/submit-eod

{
"employee_name": "sachin",
"date": "2024-05-04",
"description": "Worked on the new FastAPI EOD submission feature",
"project_name": "Imaginet"
}

http://localhost:8000/


Login User Id - admin
Login Password - password123