from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db, Base, engine
from models import Personas, TipoId, Generos
from schemas import personasCreate, personasResponse, tipoIdCreate, tipoIdResponse, generosCreate, generosResponse
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de usuarios!"}

@app.post("/tipoid/", response_model=tipoIdResponse, status_code=status.HTTP_201_CREATED)
def crear_tipoid(tipoid: tipoIdCreate, db: Session = Depends(get_db)):
    db_tipoid = db.query(TipoId).filter(TipoId.i_id_tipoid == tipoid.i_id_tipoid).first()
    if db_tipoid:
        raise HTTPException(status_code=400, detail="Tipo ID ya existe")
    nuevo_tipoid = TipoId(**tipoid.dict())
    db.add(nuevo_tipoid)
    db.commit()
    db.refresh(nuevo_tipoid)
    return nuevo_tipoid

@app.get("/tipoid/", response_model=List[tipoIdResponse])
def obtener_tiposid(db: Session = Depends(get_db)):
    tiposid = db.query(TipoId).all()
    return tiposid
    
@app.delete("/tipoid/{tipoid_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tipoid(tipoid_id: str, db: Session = Depends(get_db)):
    db_tipoid = db.query(TipoId).filter(TipoId.i_id_tipoid == tipoid_id).first()
    if db_tipoid is None:
        raise HTTPException(status_code=404, detail="Tipo ID no encontrado")
    db.delete(db_tipoid)
    db.commit()
    return

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=3000)


@app.put("/tipoid/{tipoid_id}", response_model=tipoIdResponse)
def actualizar_tipoid(tipoid_id: str, tipoid: tipoIdCreate, db: Session = Depends(get_db)):
    db_tipoid = db.query(TipoId).filter(TipoId.i_id_tipoid == tipoid_id).first()
    if db_tipoid is None:
        raise HTTPException(status_code=404, detail="Tipo ID no encontrado")
    
    # Actualizar los atributos del objeto de la base de datos
    db_tipoid.i_id_tipoid = tipoid.i_id_tipoid
    db_tipoid.v_descripcion = tipoid.v_descripcion
    
    # Guardar los cambios
    db.commit()
    db.refresh(db_tipoid)
    
    return db_tipoid
    
