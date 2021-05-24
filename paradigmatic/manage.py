import uvicorn
from app.v1.auth.routes import auth_router
from paradigmatic.app.v1.core import config
from paradigmatic.app.v1.core.auth import get_current_active_user
from paradigmatic.app.v1.core.config import API_PREFIX
from paradigmatic.app.v1.graphs.routes import graphs_router
from paradigmatic.app.v1.users.routes import users_router
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect

app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)

origins = [
    "http://localhost",
    "http://localhost:1112",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


connect('paradigmatic', host='mongo', port=27017, username="paradigmatic", password="password", authentication_source='admin')


@app.get("/api/v1")
async def root():
    return {"message": "Hello World"}



# Routers
app.include_router(
    users_router,
    prefix=API_PREFIX,
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(auth_router, prefix=API_PREFIX, tags=["auth"])


app.include_router(
    graphs_router,
    prefix=API_PREFIX,
    tags=["graphs"],
    dependencies=[Depends(get_current_active_user)],
)

if __name__ == "__main__":
    uvicorn.run("manage:app", host="0.0.0.0", reload=True, port=8888)
