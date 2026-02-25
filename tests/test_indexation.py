import httpx


async def test_trigger_indexation(client: httpx.AsyncClient):
    """
    Test that the indexation process triggers successfully.
    This tests the full E2E flow from embedding generation to
    feeding Elasticsearch and Vespa.
    """
    response = await client.post("/index")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Indexing completed" in data["message"]
