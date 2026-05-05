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

class EODReportSubmit(BaseModel):
    employee_name: str = Field(..., description="Name of the employee")
    date: str = Field(..., description="Date for the EOD report (YYYY-MM-DD)")
    description: str = Field(..., description="The EOD report content")
    project_name: Optional[str] = Field(default=None, description="Name of the project")
