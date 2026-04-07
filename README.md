# Live ERP Analytics Server

This is a **dual-setup project** that provides both an **MCP server** for Claude Desktop and a **FastAPI server** for traditional REST API interactions, pointing to a live MySQL database.

## 📂 Project Structure

```text
.
├── core/                  # Shared Business Logic and Database connection
│   ├── analytics.py
│   ├── db.py
│   └── utils.py
├── mcp_server/            # MCP server implementation (for Claude Desktop)
│   └── server.py
├── api_server/            # FastAPI implementation (REST API)
│   └── main.py
├── models/                # Pydantic schemas for data validation
│   └── schemas.py
├── requirements.txt       # Project dependencies
└── pyproject.toml         # UV packaging
```

## 🚀 Setting Up

1. Ensure you have Python 3.13 or newer.
2. If using `uv`, run:
   ```bash
   uv sync
   ```
   Or install via `pip`:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your environment variables in `.env`:
   ```env
   DB_HOST=your_host
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_NAME=your_db
   ```

## 💻 Running the FastAPI Server

To run the REST API server:
```bash
uv run uvicorn api_server.main:app --host 0.0.0.0 --port 8000 --reload
```

### Examples
Test the endpoints using `curl` or Postman:

**Get system summary:**
```bash
curl -X GET "http://localhost:8000/system-summary"
```

**Get EOD reports:**
```bash
curl -X GET "http://localhost:8000/eod-reports?limit=10"
```

**Run a generic SELECT query:**
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"sql_query": "SELECT * FROM tbl_hr_master LIMIT 5"}'
```

## 🔧 Running the MCP Server

The MCP server is specifically designed for local integration with Claude Desktop.

```bash
uv run mcp_server/server.py
```
*(Note: It uses stdio directly so you might not see terminal logs after startup unless connected.)*

### Claude Desktop Configuration

Update your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "live-erp": {
      "command": "uv",
      "args": [
        "run",
        "absolute/path/to/imaginet-mcp-server/mcp_server/server.py"
      ],
      "env": {
        "DB_HOST": "165.22.223.56",
        "DB_USER": "root",
        "DB_PASSWORD": "your_actual_password",
        "DB_NAME": "employees_db"
      }
    }
  }
}
```
*(Ensure to map `absolute/path/to` correctly to your project location)*
