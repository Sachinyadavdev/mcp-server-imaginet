from pydantic import BaseModel, Field
from typing import Optional

class EODReportQuery(BaseModel):
    employee_name: Optional[str] = Field(default=None, description="Filter by employee name")
    date_filter: Optional[str] = Field(default=None, description="Filter by specific date (YYYY-MM-DD)")
    limit: int = Field(default=50, description="Max number of records to return")

class LeaveHistoryQuery(BaseModel):
    employee_name: Optional[str] = Field(default=None, description="Filter by employee name")
    limit: int = Field(default=50, description="Max number of records to return")

class AttendanceQuery(BaseModel):
    employee_name: Optional[str] = Field(default=None, description="Filter by employee name")
    limit: int = Field(default=50, description="Max number of records to return")

class SqlQueryRequest(BaseModel):
    sql_query: str = Field(..., description="The SQL SELECT query to execute")
