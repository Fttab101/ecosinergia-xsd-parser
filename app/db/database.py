from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import config
from sqlalchemy.exc import ProgrammingError # Importar para manejo de errores SQL


engine = create_engine(config.DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Prueba de conexión (ejecutar solo una vez para verificar)
try:
    with engine.connect() as connection:
        print("Conexión a la base de datos exitosa!")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")


def execute_sql(sql_statements: list):
    """Ejecuta una lista de sentencias SQL en la base de datos."""
    try:
        with engine.connect() as connection:
            for statement in sql_statements:
                connection.execute(statement)
        return {"message": "Sentencias SQL ejecutadas correctamente"}
    except ProgrammingError as e: # Capturar errores de SQL
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Error al ejecutar las sentencias SQL: {e}"}    

    