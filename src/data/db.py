from sqlmodel import create_engine, SQLModel, Session
from src.models.coche import Coche
import os

DATABASE_URL = os.getenv(
    "DB_URL",
    "postgresql+psycopg2://quevedo:1234@localhost:5432/cochesdb"
)

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        coches_existentes = session.query(Coche).count()
        if coches_existentes == 0:
            session.add_all([
                Coche(modelo="Audi A1", anio=2021, precio=22000),
                Coche(modelo="Audi A3", anio=2022, precio=28000),
                Coche(modelo="Audi A4", anio=2023, precio=39000),
                Coche(modelo="Audi A5", anio=2023, precio=45000),
                Coche(modelo="Audi A6", anio=2021, precio=52000),
                Coche(modelo="Audi A7", anio=2022, precio=68000),
                Coche(modelo="Audi A8", anio=2023, precio=89000),
                Coche(modelo="Audi Q3", anio=2022, precio=35000),
                Coche(modelo="Audi Q5", anio=2024, precio=61000),
                Coche(modelo="Audi e-tron", anio=2023, precio=72000),
            ])
            session.commit()
