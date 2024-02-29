from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, accounts, categories, transactions
from app.dependencies import oauth2_scheme

from app.config import config
from app.services.database import sessionmanager


def init_app(init_db=True):
    lifespan = None

    if init_db:
        sessionmanager.init(config.DB_CONFIG)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    server = FastAPI(title="Expense Tracker", version="0.1.0", lifespan=lifespan)

    origins = [
        "*",
    ]

    server.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    server.include_router(auth.router)
    server.include_router(users.router)
    server.include_router(accounts.router, dependencies=[Depends(oauth2_scheme)])
    server.include_router(categories.router, dependencies=[Depends(oauth2_scheme)])
    server.include_router(transactions.router, dependencies=[Depends(oauth2_scheme)])

    return server
