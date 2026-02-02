from typing import Optional
from sqlmodel import SQLModel, Field

class Coche(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    modelo: str
    anio: int
    precio: float
