from xmlschema import XMLSchema
from sqlalchemy.schema import CreateTable
from sqlalchemy import (
    Column,
    Integer,
    String,
    MetaData,
    Table,
) # Importar los tipos de datos necesarios de SQLAlchemy
import re
import glob # Para obtener la lista de archivos XSD
import os


def parse_xsd(xsd_path: str):
    try:
        # Obtener la lista de todos los archivos XSD en el directorio 'schemas'
        schemas_dir = os.path.join(os.path.dirname(__file__), "../../schemas")
        # No necesitas glob aquí, ya que sabes qué archivos necesitas.

        locations = {
            "e3l://eterproject.org/3.0/e3l": os.path.join(schemas_dir, "e3l.xsd"),
            "e3l://eterproject.org/3.0/air": os.path.join(schemas_dir, "e3l-airQuality.xsd"),    
            "e3l://eterproject.org/3.0/common": os.path.join(schemas_dir, "e3l-common.xsd"),
            "e3l://eterproject.org/3.0/documentation": os.path.join(schemas_dir, "e3l-documentation.xsd"),
            "e3l://eterproject.org/3.0/master": os.path.join(schemas_dir, "e3l-environmentalMasterData.xsd"),            
            "e3l://eterproject.org/3.0/eprtr": os.path.join(schemas_dir, "e3l-eprtr.xsd"),
            "e3l://eterproject.org/3.0/soils": os.path.join(schemas_dir, "e3l-soils.xsd"),
            "e3l://eterproject.org/3.0/soilsSupport": os.path.join(schemas_dir, "e3l-soilsSupport.xsd"),
            "e3l://eterproject.org/3.0/waste": os.path.join(schemas_dir, "e3l-waste.xsd"),            
            "e3l://eterproject.org/3.0/wasteSupport": os.path.join(schemas_dir, "e3l-wasteSupport.xsd"),
            "e3l://eterproject.org/3.0/water": os.path.join(schemas_dir, "e3l-water.xsd"),
            "e3s://eterproject.org/e3s/common": os.path.join(schemas_dir, "e3s-common.xsd"),
            "e3s://eterproject.org/e3s/waste": os.path.join(schemas_dir, "e3s-waste.xsd"),
            "http://www.w3.org/2001/XMLSchema": os.path.join(schemas_dir, "xml.xsd"),
            # Añade los demás namespaces y archivos XSD que necesites de la misma manera
        }
        

        schema = XMLSchema(xsd_path, locations=locations) # Quitar namespaces de aquí


        elements = {} # Inicializar el diccionario aquí
        for name, element in schema.elements.items():
            elements[name] = {
                "type": str(element.type),
                "restrictions": {}
            }
            if hasattr(element.type, 'facets'):
                for facet_name, facet in element.type.facets.items():
                    elements[name]["restrictions"][facet_name] = str(facet.value)

        return elements # Devolver el diccionario


    except Exception as e:
        print(f"Error al parsear el archivo XSD: {e}")  # Imprimir el traceback completo en la consola
        import traceback
        error_message = traceback.format_exc() # Obtener el traceback completo
        return {"error": error_message} # Devolver el error como parte de la respuesta JSON
    
def generate_sql(schema_data: dict, table_name_prefix="e3l_"):
    #"""Genera sentencias SQL CREATE TABLE a partir de los datos del esquema XSD."""

    sql_statements = []
    metadata = MetaData() # Crear una instancia de MetaData

    for element_name, element_data in schema_data.items():
        table_name = table_name_prefix + element_name
        columns = [
            Column("id", Integer, primary_key=True, autoincrement=True) # Agregar una columna id como primary key
        ]
        for attr_name, attr_data in element_data.get("elements", {}).items(): # Obtener elementos anidados si existen
            column_type = String  # Tipo de columna por defecto: String
            # Ajustar el tipo de columna según el tipo XSD (puedes ampliar esto)
            xsd_type = attr_data["type"].lower()
            if "int" in xsd_type or "integer" in xsd_type:
                column_type = Integer
            # Añadir la columna a la lista de columnas
            columns.append(Column(attr_name, column_type))
        table = Table(table_name, metadata, *columns) # Crear objeto Table de SQLAlchemy
        sql_statements.append(str(CreateTable(table))) # Generar sentencia CREATE TABLE y agregarla a la lista

    return sql_statements