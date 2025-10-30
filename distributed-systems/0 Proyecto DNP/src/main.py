from fastapi import FastAPI, Depends
from api.routes import router
from observability.logging import setup_logging
from observability.metrics import setup_metrics
from observability.tracing import setup_tracing
from api.jwt import JWTBearer
from db.init_db import ProyectosDatabaseCreator
import os

app = FastAPI(title="MS Proyectos")

setup_logging()
setup_metrics(app)
setup_tracing(app)

# Configuración de la base de datos
db_path = os.getenv("DATABASE_PATH", "dnp_proyectos.db")
db_creator = ProyectosDatabaseCreator(db_type="sqlite", connection_params={'database': db_path})
db_creator.connect()
db_creator.create_tables()
db_creator.insert_sample_data()

app.include_router(router, dependencies=[Depends(JWTBearer())])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)