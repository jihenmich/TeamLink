from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.endpoints.employees import router as employees_router
from app.api.endpoints.leave import router as leave_router
from app.api.endpoints.payroll import router as payroll_router
from app.api.endpoints.time_tracking import router as time_tracking_router

app = FastAPI(title="TeamLink API")

# Statische Dateien (z.B. für das Favicon) bereitstellen
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Favicon bereitstellen
@app.get("/favicon.ico")
def favicon():
    return FileResponse("app/static/favicon.ico")

# Endpoints einbinden
app.include_router(employees_router, prefix="/api/employees", tags=["employees"])
app.include_router(leave_router, prefix="/api/leave", tags=["leave"])
app.include_router(payroll_router, prefix="/api/payroll", tags=["payroll"])
app.include_router(time_tracking_router, prefix="/api/time_tracking", tags=["time_tracking"])

@app.get("/")
def root():
    return {"message": "Welcome to TeamLink API!"}
