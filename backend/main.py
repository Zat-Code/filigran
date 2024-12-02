from routes.aggregator import router as aggregator_router
from contextlib import asynccontextmanager
from db.database import connect_to_mongo, close_mongo_connection
from fastapi import FastAPI
from jobs.pdf_extractor import extract_pdfs_to_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    
    from db.database import db
    if db is None:
        raise RuntimeError("Database connection not initialized.")
    
    await extract_pdfs_to_db("data/pdfs/", process_all=False)
    yield
    await close_mongo_connection()


app = FastAPI(lifespan=lifespan)

# Inclure les routes de comparaison
app.include_router(aggregator_router, prefix="/api")
