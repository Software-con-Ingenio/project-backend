
from fastapi import FastAPI
from database import Base, engine
from controllers.genre_controller import router as genre_router
from controllers.juego_controller import router as juego_router
from controllers.platform_controller import router as platform_router
from controllers.sale_controller import router as sale_router
from controllers.usuario_controller import router as usuario_router
from controllers.auth_controller import router as auth_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


@app.on_event("startup")
def on_startup():
	import domain.models  # noqa: F401
	Base.metadata.create_all(bind=engine)

# Incluimos el router de géneros
app.include_router(genre_router)
app.include_router(juego_router)
app.include_router(platform_router)
app.include_router(sale_router)
app.include_router(usuario_router)
app.include_router(auth_router)

app.mount("/static", StaticFiles(directory="project-frontend"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los verbos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)