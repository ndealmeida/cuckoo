from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Query
from injector import Injector
from pydantic import BaseModel

from src.indexer import Indexer
from src.search_store import SearchSource, SearchStore, SearchType


# Graceful shutdown of FastAPI requires this logic
@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    try:
        from joblib.externals.loky import get_reusable_executor

        get_reusable_executor().shutdown(wait=True)
    except (ImportError, Exception):
        pass


app = FastAPI(
    title="Cuckoo Search API",
    docs_url="/",
    lifespan=lifespan,
)

container = Injector()


class SearchResult(BaseModel):
    score: float
    title: str


@app.post("/index")
def trigger_index():
    indexer = container.get(Indexer)
    return indexer.run_all()


@app.get("/search", response_model=List[SearchResult])
def search(
    query: str = Query(
        ...,
        examples=["how to build AI systems"],
        description="The search term. E.g: how to build AI systems",
    ),
    source: SearchSource = Query(...),
    search_type: SearchType = Query(..., alias="type"),
):
    store = container.get(SearchStore)
    return store.search(query=query, source=source, search_type=search_type)
