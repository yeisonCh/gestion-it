from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import settings


DATABASE_URL = (
    f"mssql+pyodbc://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_SERVER}/{settings.DB_NAME}"
    f"?driver=ODBC+Driver+17+for+SQL+Server"
)


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def crear_base_de_datos_si_no_existe():

    engine_master = create_engine(
        f"mssql+pyodbc://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_SERVER}/master"
        f"?driver=ODBC+Driver+17+for+SQL+Server"
    )

    with engine_master.connect() as conn:

        conn = conn.execution_options(
            isolation_level="AUTOCOMMIT"
        )

        resultado = conn.execute(
            text(
                f"SELECT name FROM sys.databases "
                f"WHERE name = '{settings.DB_NAME}'"
            )
        )

        if not resultado.fetchone():

            conn.execute(
                text(
                    f"CREATE DATABASE {settings.DB_NAME}"
                )
            )

            print(
                f"✅ Base de datos '{settings.DB_NAME}' creada."
            )

        else:
            print(
                f"✅ Base de datos '{settings.DB_NAME}' ya existe."
            )