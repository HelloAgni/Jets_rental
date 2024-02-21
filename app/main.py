from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import main_router
from app.data._data_ import router as data_router
from contextlib import asynccontextmanager
from datetime import datetime
from app.core.init_db import create_first_superuser


# new style @app.on_event('startup') / ('shutdown')
@asynccontextmanager
async def lifespan(app):
    # print("Run at startup!")
    # yield
    # print("Run on shutdown!")
    await create_first_superuser()
    yield
    shutdown_and_log()


def shutdown_and_log():
    with open("log_shutdown.txt", mode="a") as log:
        log.write(
            "---Application shutdown---\n"
            f"{datetime.now().strftime('%d %b %Y %H:%M:%S')}\n\n"
            )


app = FastAPI(
    lifespan=lifespan,
    title=settings.app_title,
    description=settings.description)


@app.get('/', tags=['Home'])
def hello():
    return {
        'Hello': 'User!',
        'Docs': 'http://127.0.0.1:8000/docs'
        }


app.include_router(main_router)
app.include_router(data_router, tags=['Load_data'])
