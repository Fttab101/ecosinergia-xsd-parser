from fastapi import FastAPI

from app.api.endpoints import router as api_router
from app.db.database import engine

app = FastAPI()

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "API funcionando correctamente"}

# Importar la prueba de conexión *después* de definir la app de FastAPI
from app.db.database import engine # Solo importamos engine, no ejecutamos la prueba directamente

@app.on_event("startup")
async def startup():
    """Comprueba la conexión a la base de datos al iniciar la aplicación."""
    try:
        with engine.connect() as connection:
            print("Conexión a la base de datos exitosa!")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")


@app.on_event("shutdown")
async def shutdown():
    """Cierra la conexión al apagar la aplicación (opcional, pero buena práctica)."""
    await engine.dispose()