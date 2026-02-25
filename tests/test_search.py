import httpx


async def test_lexical_search(client: httpx.AsyncClient):
    """
    Test lexical (keyword-based) search on both Elasticsearch and Vespa.
    Query 'Elasticsearch' should return the Elasticsearch document.
    """
    # Ensure index is populated (optional if running in order)
    # await client.post("/index")

    # 1. Test Elasticsearch Lexical
    response = await client.get(
        "/search", params={"query": "Elasticsearch", "source": "ELASTICSEARCH", "type": "LEXICAL"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # The document with id 2 contains 'Elasticsearch'
    assert any("Elasticsearch Fundamentals" in hit["title"] for hit in data)

    # 2. Test Vespa Lexical
    response = await client.get(
        "/search", params={"query": "Vespa", "source": "VESPA", "type": "LEXICAL"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # The document with id 3 contains 'Vespa'
    assert any("Vespa: The Big Data Serving Engine" in hit["title"] for hit in data)


async def test_semantic_search(client: httpx.AsyncClient):
    """
    Test semantic search on both engines.
    Query 'building intelligent systems' should find 'AI Engineering' doc
    even if keywords don't match exactly.
    """
    # 1. Test Elasticsearch Semantic
    response = await client.get(
        "/search",
        params={
            "query": "building intelligent systems",
            "source": "ELASTICSEARCH",
            "type": "SEMANTIC",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # The 'AI Engineering' doc is about 'systems engineering' and 'software engineering'
    assert any("Introduction to AI Engineering" in hit["title"] for hit in data)

    # 2. Test Vespa Semantic
    response = await client.get(
        "/search",
        params={"query": "data processing at scale", "source": "VESPA", "type": "SEMANTIC"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # Vespa doc is about 'large data sets' and 'low-latency computation'
    assert any("Vespa: The Big Data Serving Engine" in hit["title"] for hit in data)
