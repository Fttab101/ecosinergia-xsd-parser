from fastapi import APIRouter, HTTPException, Depends
from app.parser.xsd_parser import parse_xsd, generate_sql
from app.db.database import execute_sql, get_db  # Importar get_db y execute_sql
from sqlalchemy.orm import Session  # Importar la clase Session
import os


router = APIRouter()

@router.get("/parse_xsd", response_model_exclude_unset=True)
async def parse_xsd_endpoint(xsd_file: str = "e3l-wasteSupport.xsd"):
    """Parsea un archivo XSD y devuelve los elementos, tipos y restricciones."""

    # Construye la ruta completa al archivo XSD
    schemas_dir = os.path.join(os.path.dirname(__file__), "../../schemas")
    xsd_path = os.path.join(schemas_dir, xsd_file)

    # Asegúrate de que el archivo exista
    if not os.path.exists(xsd_path):
        raise HTTPException(status_code=404, detail=f"Archivo XSD '{xsd_file}' no encontrado")

    schema_data = parse_xsd(xsd_path)


    if isinstance(schema_data, dict) and "error" in schema_data: # Verificar si hay un error
        raise HTTPException(status_code=500, detail=schema_data["error"])

    return list(schema_data) # Convertir el generador a lista para la respuesta

@router.post("/create_tables") # Usamos POST para crear tablas
async def create_tables_endpoint(xsd_file: str = "e3l-wasteSupport.xsd", db: Session = Depends(get_db)):
    schemas_dir = os.path.join(os.path.dirname(__file__), "../../schemas")
    xsd_path = os.path.join(schemas_dir, xsd_file)

    if not os.path.exists(xsd_path):
        raise HTTPException(status_code=404, detail=f"Archivo XSD '{xsd_file}' no encontrado")

    schema_data = parse_xsd(xsd_path)

    if isinstance(schema_data, dict) and "error" in schema_data:
        raise HTTPException(status_code=500, detail=schema_data["error"])

    sql_statements = generate_sql(schema_data)
    result = execute_sql(sql_statements)  # Ejecutar las sentencias SQL

    if "error" in result:
         raise HTTPException(status_code=500, detail=result["error"])

    return result