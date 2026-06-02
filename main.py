from fastapi import FastAPI
from database import Base, engine
from controllers.genre_controller import router as genre_router
from controllers.juego_controller import router as juego_router
from controllers.platform_controller import router as platform_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
	import domain.models  # noqa: F401
	Base.metadata.create_all(bind=engine)

# Incluimos el router de géneros
app.include_router(genre_router)
app.include_router(juego_router)
app.include_router(platform_router)