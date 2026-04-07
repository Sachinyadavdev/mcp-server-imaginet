from mcp.server.fastmcp import FastMCP
from core import analytics

# Initialize FastMCP Server
mcp = FastMCP("Live ERP Analytics Engine")

@mcp.tool()
def analyze_eod_reports(employee_name: str = None, date_filter: str = None, limit: int = 50) -> list:
    """
    Analyze End of Day (EOD) reports. Automatically maps employee ID to their Name 
    and brings in the associated project information for context.
    """
    return analytics.analyze_eod_reports(employee_name, date_filter, limit)

@mcp.tool()
def analyze_leave_history(employee_name: str = None, limit: int = 50) -> list:
    """
    Get Employee Leave Records heavily joined with Employee Name.
    Retrieves the actual reason, subject, and timeframe.
    """
    return analytics.analyze_leave_history(employee_name, limit)

@mcp.tool()
def analyze_attendance_records(employee_name: str = None, limit: int = 50) -> list:
    """
    Get daily attendance data joined with Employee Name and shift working hours.
    """
    return analytics.analyze_attendance_records(employee_name, limit)

@mcp.tool()
def get_database_schema() -> dict:
    """
    Get the full database schema (all tables and columns) from the live server.
    """
    return analytics.get_database_schema()

@mcp.tool()
def run_select_query(sql_query: str) -> list:
    """
    Run a custom SQL SELECT query for advanced, dynamic analytics.
    """
    return analytics.run_select_query(sql_query)

@mcp.tool()
def get_system_summary() -> dict:
    """Get a quick high-level summary of the company ERP data."""
    return analytics.get_system_summary()

if __name__ == "__main__":
    mcp.run(transport="stdio")
