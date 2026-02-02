from fastapi import FastAPI, Request, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import select
from pathlib import Path

from src.models.coche import Coche
from src.data.db import get_session, init_db

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")



@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/coches", response_class=HTMLResponse)
async def ver_coches(request: Request, session=Depends(get_session)):
    coches = session.exec(select(Coche)).all()
    return templates.TemplateResponse("coches.html", {"request": request, "coches": coches})


@app.get("/coches/crear", response_class=HTMLResponse)
async def crear_coche_form(request: Request):
    return templates.TemplateResponse("crear_coche.html", {"request": request, "mensaje": None})


@app.post("/coches/crear", response_class=HTMLResponse)
async def crear_coche_post(
    request: Request,
    session=Depends(get_session),
    modelo: str = Form(...),
    anio: int = Form(...),
    precio: float = Form(...)
):
    nuevo_coche = Coche(modelo=modelo, anio=anio, precio=precio)
    session.add(nuevo_coche)
    session.commit()
    session.refresh(nuevo_coche)

    mensaje = f"Coche {modelo} creado correctamente."

    return templates.TemplateResponse("crear_coche.html", {"request": request, "mensaje": mensaje})


@app.get("/coches/editar/{coche_id}", response_class=HTMLResponse)
async def editar_coche_form(coche_id: int, request: Request, session=Depends(get_session)):
    coche = session.get(Coche, coche_id)
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    return templates.TemplateResponse("editar_coche.html", {"request": request, "coche": coche})


@app.post("/coches/editar/{coche_id}", response_class=HTMLResponse)
async def editar_coche_post(
    coche_id: int,
    request: Request,
    session=Depends(get_session),
    modelo: str = Form(...),
    anio: int = Form(...),
    precio: float = Form(...)
):
    coche = session.get(Coche, coche_id)
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    coche.modelo = modelo
    coche.anio = anio
    coche.precio = precio

    session.add(coche)
    session.commit()
    session.refresh(coche)

    return templates.TemplateResponse(
        "editar_coche.html",
        {
            "request": request,
            "coche": coche,
            "mensaje": f"Coche {modelo} actualizado correctamente."
        }
    )


@app.get("/coches/eliminar/{coche_id}", response_class=HTMLResponse)
async def eliminar_coche_form(coche_id: int, request: Request, session=Depends(get_session)):
    coche = session.get(Coche, coche_id)
    return templates.TemplateResponse("eliminar_coche.html", {"request": request, "coche": coche})


@app.post("/coches/eliminar/{coche_id}")
async def eliminar_coche_post(coche_id: int, session=Depends(get_session)):
    coche = session.get(Coche, coche_id)
    if coche:
        session.delete(coche)
        session.commit()
    return RedirectResponse(url="/coches", status_code=303)


@app.get("/coches/{coche_id}", response_class=HTMLResponse)
async def detalle_coche(coche_id: int, request: Request, session=Depends(get_session)):
    coche = session.get(Coche, coche_id)
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    return templates.TemplateResponse("coche_detalle.html", {"request": request, "coche": coche})


@app.get("/api/coches", response_model=list[Coche])
async def api_coches(session=Depends(get_session)):
    coches = session.exec(select(Coche)).all()
    return coches
