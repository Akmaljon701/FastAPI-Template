from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from db import Base, engine
from routes import auth, users, wsmanager
from fastapi.middleware.cors import CORSMiddleware
from middlewares import unit_of_work_middleware, handle_integrity_errors
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.add_middleware(BaseHTTPMiddleware, dispatch=unit_of_work_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=handle_integrity_errors)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {"message": "Welcome"}


app.include_router(auth.login_router)
app.include_router(users.router_user)
app.include_router(wsmanager.notification_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI app by Akmaljon",
        version="3.11",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
