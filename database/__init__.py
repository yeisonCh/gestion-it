from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
    f"?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def crear_base_de_datos_si_no_existe():
    engine_master = create_engine(
        f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/master"
        f"?driver=ODBC+Driver+17+for+SQL+Server"
    )
    with engine_master.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        resultado = conn.execute(
            text(f"SELECT name FROM sys.databases WHERE name = '{DB_NAME}'")
        )
        if not resultado.fetchone():
            conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
            print(f"✅ Base de datos '{DB_NAME}' creada.")
        else:
            print(f"✅ Base de datos '{DB_NAME}' ya existe.")