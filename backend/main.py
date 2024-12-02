from routes.aggregator import router as aggregator_router
from contextlib import asynccontextmanager
from db.database import connect_to_mongo, close_mongo_connection
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(lifespan=lifespan)

# Inclure les routes de comparaison
app.include_router(aggregator_router, prefix="/api")
