import os

import pymongo
from bson import ObjectId
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from models.evento import (Evento, EventoList, EventoNew, EventoQuery,
                           EventoUpdate)

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

eventos_bp = APIRouter(prefix="/eventos", tags=["eventos"])

client = pymongo.MongoClient(MONGO_URL)
db = client.parcialFront
eventos = db.eventos

@eventos_bp.get("/")
def get_eventos(query: EventoQuery = Depends()):
    try:
        print(query)
        eventData = eventos.find(query.model_dump(exclude_none=True))
        if eventData is None:
            raise HTTPException(status_code=404, detail="No se encontraron eventos")
        eventosList = EventoList(eventos=[Evento(**evento) for evento in eventData])
        return eventosList

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los eventos, {e}")

@eventos_bp.get("/{id}")
def get_evento(id: str):
    try:
        evento = eventos.find_one({"_id": ObjectId(id)})
        if evento is None:
            raise HTTPException(status_code=404, detail="Evento no encontrado")
        return Evento(**evento)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el evento, {e}")

@eventos_bp.post("/")
def create_evento(evento: EventoNew):
    try:
        evento_res = eventos.insert_one(evento.to_mongo_dict(exclude_none=True))
        raise HTTPException(status_code=201, detail=f"Evento creado exitosamente con el id {evento_res.inserted_id}")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el evento, {e}")

@eventos_bp.put("/{id}")
def update_evento(id: str, evento: EventoUpdate):
    try:
        evento_res = eventos.update_one({"_id": ObjectId(id)}, {"$set": evento.to_mongo_dict(exclude_none=True)})
        if evento_res.modified_count == 0:
            raise HTTPException(status_code=404, detail="Evento no encontrado")
        return {"message": "Evento actualizado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el evento, {e}")

@eventos_bp.delete("/{id}")
def delete_evento(id: str):
    try:
        evento_res = eventos.delete_one({"_id": ObjectId(id)})
        if evento_res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Evento no encontrado")
        return {"message": "Evento eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el evento, {e}")
