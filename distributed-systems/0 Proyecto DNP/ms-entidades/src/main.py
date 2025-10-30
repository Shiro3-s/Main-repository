from fastapi import FastAPI
from api.routes import router
from observability.logging import setup_logging
from observability.metrics import setup_metrics
from observability.tracing import setup_tracing

app = FastAPI(title="MS Entidades")

setup_logging()
setup_metrics(app)
setup_tracing(app)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)