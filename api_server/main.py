from fastapi import FastAPI, HTTPException, Depends, status, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
import os
from core import analytics
from models.schemas import EODReportSubmit

app = FastAPI(
    title="Live ERP Analytics API", 
    description="REST API Server for company ERP data",
    docs_url=None, 
    redoc_url=None, 
    openapi_url=None
)

# Authentication logic (No DB, using .env)
class LoginRequest(BaseModel):
    username: str
    password: str

SESSION_TOKEN = "erp_auth_secure_token_2024"

def is_authenticated(request: Request):
    return request.cookies.get("session_token") == SESSION_TOKEN

def require_auth_api(request: Request):
    if not is_authenticated(request):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@app.get("/login", include_in_schema=False)
async def login_page():
    static_path = os.path.join(os.path.dirname(__file__), "static")
    return FileResponse(os.path.join(static_path, "login.html"))

@app.post("/login", include_in_schema=False)
async def login(data: LoginRequest, response: Response):
    correct_user = os.getenv("ADMIN_USER", "admin")
    correct_pass = os.getenv("ADMIN_PASSWORD", "password123")
    
    if data.username == correct_user and data.password == correct_pass:
        response.set_cookie(key="session_token", value=SESSION_TOKEN, httponly=True)
        return {"success": True}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("session_token")
    return response

# Protected Docs
@app.get("/docs", include_in_schema=False)
async def get_documentation(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")
    return get_swagger_ui_html(openapi_url="/openapi.json", title=app.title + " - Docs")

@app.get("/openapi.json", include_in_schema=False)
async def openapi(request: Request):
    if not is_authenticated(request):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_path):
    os.makedirs(static_path)

app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
def read_root(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")
    response = FileResponse(os.path.join(static_path, "index.html"))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

@app.post("/submit-eod")
def submit_eod(report: EODReportSubmit, auth=Depends(require_auth_api)):
    res = analytics.submit_eod_report(report.model_dump())
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@app.get("/eod-reports")
def get_eod_reports(employee_name: str = None, date_filter: str = None, limit: int = 50, auth=Depends(require_auth_api)):
    res = analytics.analyze_eod_reports(employee_name, date_filter, limit)
    if res and isinstance(res[0], dict) and "error" in res[0]:
        raise HTTPException(status_code=400, detail=res[0]["error"])
    return res

@app.get("/leave-history")
def get_leave_history(employee_name: str = None, limit: int = 50, auth=Depends(require_auth_api)):
    res = analytics.analyze_leave_history(employee_name, limit)
    if res and isinstance(res[0], dict) and "error" in res[0]:
        raise HTTPException(status_code=400, detail=res[0]["error"])
    return res

@app.get("/attendance-records")
def get_attendance_records(employee_name: str = None, limit: int = 50, auth=Depends(require_auth_api)):
    res = analytics.analyze_attendance_records(employee_name, limit)
    if res and isinstance(res[0], dict) and "error" in res[0]:
        raise HTTPException(status_code=400, detail=res[0]["error"])
    return res

@app.get("/database-schema")
def database_schema(auth=Depends(require_auth_api)):
    res = analytics.get_database_schema()
    if "error" in res:
         raise HTTPException(status_code=400, detail=res["error"])
    return res

@app.get("/system-summary")
def system_summary(auth=Depends(require_auth_api)):
    res = analytics.get_system_summary()
    if "error" in res:
         raise HTTPException(status_code=400, detail=res["error"])
    return res

@app.get("/projects")
def get_projects(auth=Depends(require_auth_api)):
    res = analytics.run_select_query("SELECT name FROM tbl_project_master ORDER BY name ASC")
    if res and isinstance(res[0], dict) and "error" in res[0]:
        raise HTTPException(status_code=400, detail=res[0]["error"])
    return [r["name"] for r in res]

@app.get("/employees")
def get_employees(auth=Depends(require_auth_api)):
    res = analytics.run_select_query("SELECT employee_name FROM tbl_hr_master ORDER BY employee_name ASC")
    if res and isinstance(res[0], dict) and "error" in res[0]:
        raise HTTPException(status_code=400, detail=res[0]["error"])
    return [r["employee_name"] for r in res]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server.main:app", host="0.0.0.0", port=8000, reload=True)
