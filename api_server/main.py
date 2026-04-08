from fastapi import FastAPI, HTTPException
from core import analytics

app = FastAPI(title="Live ERP Analytics API", description="REST API Server for company ERP data")

@app.get("/eod-reports")
def get_eod_reports(employee_name: str = None, date_filter: str = None, limit: int = 50):
    res = analytics.analyze_eod_reports(employee_name, date_filter, limit)
    if res and isinstance(res[0], dict) and "error" in res[0]:
        raise HTTPException(status_code=400, detail=res[0]["error"])
    return res

@app.get("/leave-history")
def get_leave_history(employee_name: str = None, limit: int = 50):
    res = analytics.analyze_leave_history(employee_name, limit)
    if res and isinstance(res[0], dict) and "error" in res[0]:
        raise HTTPException(status_code=400, detail=res[0]["error"])
    return res

@app.get("/attendance-records")
def get_attendance_records(employee_name: str = None, limit: int = 50):
    res = analytics.analyze_attendance_records(employee_name, limit)
    if res and isinstance(res[0], dict) and "error" in res[0]:
        raise HTTPException(status_code=400, detail=res[0]["error"])
    return res

@app.get("/database-schema")
def database_schema():
    res = analytics.get_database_schema()
    if "error" in res:
         raise HTTPException(status_code=400, detail=res["error"])
    return res

@app.get("/system-summary")
def system_summary():
    res = analytics.get_system_summary()
    if "error" in res:
         raise HTTPException(status_code=400, detail=res["error"])
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server.main:app", host="0.0.0.0", port=8000, reload=True)
