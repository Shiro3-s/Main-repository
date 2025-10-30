from prometheus_client import Counter, generate_latest
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

REQUEST_COUNT = Counter('request_count', 'Total HTTP requests')

def setup_metrics(app: FastAPI):
    @app.middleware("http")
    async def count_requests(request, call_next):
        REQUEST_COUNT.inc()
        response = await call_next(request)
        return response

    @app.get("/metrics")
    def metrics():
        return PlainTextResponse(generate_latest())  # CORREGIR: debe retornar PlainTextResponse