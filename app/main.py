from fastapi import FastAPI, status
from datetime import datetime
from fastapi.responses import JSONResponse
import psutil

app = FastAPI()


@app.get("/")
def health_check():
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Health API service is running"}
    )


@app.get("/health")
def resource_health_check():
    health_status = "healthy"
    CPU_THRESHOLD = 80
    MEMORY_THRESHOLD = 80
    DISK_THRESHOLD = 90

    current_time = datetime.now()
    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    disk = psutil.disk_usage("/")

    if cpu_percent > CPU_THRESHOLD:
        health_status = "unhealthy"
    if memory.percent > MEMORY_THRESHOLD:
        health_status = "unhealthy"
    if disk.percent > DISK_THRESHOLD:
        health_status = "unhealthy"

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": health_status,
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "disk_percent": disk.percent,
            "timestamp": current_time.isoformat(),
        },
    )


@app.get("/metrics")
def resource_metrics():
    load_averages = psutil.getloadavg()
    cpu_count = psutil.cpu_count() or 1
    load_percentages = [x / cpu_count * 100 for x in load_averages]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "cpu": {
                "percent": psutil.cpu_percent(interval=1),
                "cores": psutil.cpu_count(logical=True),
                "load_avg": load_averages,
                "load_avg_percent": load_percentages,
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent,
            },
            "disk": {
                "total": psutil.disk_usage("/").total,
                "used": psutil.disk_usage("/").used,
                "free": psutil.disk_usage("/").free,
                "percent": psutil.disk_usage("/").percent,
            },
        },
    )
