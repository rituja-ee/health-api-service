from fastapi import FastAPI
import psutil

app = FastAPI()

@app.get("/")
def health_check():
    return {"Health API service is running"}

@app.get("/metrics")
def resource_metrics():
    load_averages = psutil.getloadavg()  
    cpu_count = psutil.cpu_count() or 1
    load_percentages = [x / cpu_count * 100 for x in load_averages]

    return {
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
        }
    }

@app.get("/health")
def resource_health_check():
    status = "healthy"
    errors = []
    CPU_THRESHOLD = 80
    MEMORY_THRESHOLD = 80
    DISK_THRESHOLD = 90

    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    disk = psutil.disk_usage('/')

    if cpu_percent > CPU_THRESHOLD:
        status = "unhealthy"
        errors.append(f"High CPU utilization: {cpu_percent}%")
    if memory.percent > MEMORY_THRESHOLD:
        status = "unhealthy"
        errors.append(f"High memory utilization: {memory.percent}")
    if disk.percent > DISK_THRESHOLD:
        status = "unhealthy"
        errors.append(f"High disk utilization: {disk.percent}%")
    
    return {
        "status": status,
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "disk_percent": disk.percent,
        "errors": errors,
    }
