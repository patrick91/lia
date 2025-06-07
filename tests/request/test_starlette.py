import pytest
from inline_snapshot import snapshot
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse
from starlette.testclient import TestClient
from starlette.types import Receive, Scope, Send

from lia.request import AsyncHTTPRequest

pytestmark = pytest.mark.asyncio


async def test_basic_get_request():
    async def app(scope: Scope, receive: Receive, send: Send) -> None:
        request = AsyncHTTPRequest.from_starlette(StarletteRequest(scope, receive))

        response = JSONResponse(
            {
                "headers": dict(request.headers),
                "query_params": dict(request.query_params),
                "body": (await request.get_body()).decode("utf-8"),
                "url": str(request.url),
                "method": request.method,
            }
        )
        await response(scope, receive, send)

    client = TestClient(app)

    response = client.get("/?a=1&b=2")

    assert response.json() == snapshot(
        {
            "headers": {
                "host": "testserver",
                "accept": "*/*",
                "accept-encoding": "gzip, deflate",
                "connection": "keep-alive",
                "user-agent": "testclient",
            },
            "query_params": {"a": "1", "b": "2"},
            "body": "",
            "url": "http://testserver/?a=1&b=2",
            "method": "GET",
        }
    )


async def test_basic_post_form_data():
    async def app(scope: Scope, receive: Receive, send: Send) -> None:
        request = AsyncHTTPRequest.from_starlette(StarletteRequest(scope, receive))

        response = JSONResponse(
            {
                "headers": dict(request.headers),
                "query_params": dict(request.query_params),
                "body": (await request.get_body()).decode("utf-8"),
                "url": str(request.url),
                "method": request.method,
            }
        )
        await response(scope, receive, send)

    client = TestClient(app)

    response = client.post("/", data={"a": "1", "b": "2"})

    assert response.json() == snapshot(
        {
            "headers": {
                "host": "testserver",
                "accept": "*/*",
                "accept-encoding": "gzip, deflate",
                "connection": "keep-alive",
                "user-agent": "testclient",
                "content-length": "7",
                "content-type": "application/x-www-form-urlencoded",
            },
            "query_params": {},
            "body": "a=1&b=2",
            "url": "http://testserver/",
            "method": "POST",
        }
    )


async def test_basic_post_json():
    async def app(scope: Scope, receive: Receive, send: Send) -> None:
        request = AsyncHTTPRequest.from_starlette(StarletteRequest(scope, receive))

        response = JSONResponse(
            {
                "headers": dict(request.headers),
                "query_params": dict(request.query_params),
                "body": (await request.get_body()).decode("utf-8"),
                "url": str(request.url),
                "method": request.method,
            }
        )

        await response(scope, receive, send)

    client = TestClient(app)

    response = client.post("/", json={"a": "1", "b": "2"})

    assert response.json() == snapshot(
        {
            "headers": {
                "host": "testserver",
                "accept": "*/*",
                "accept-encoding": "gzip, deflate",
                "connection": "keep-alive",
                "user-agent": "testclient",
                "content-length": "17",
                "content-type": "application/json",
            },
            "query_params": {},
            "body": '{"a":"1","b":"2"}',
            "url": "http://testserver/",
            "method": "POST",
        }
    )


async def test_get_with_cookies():
    async def app(scope: Scope, receive: Receive, send: Send) -> None:
        request = AsyncHTTPRequest.from_starlette(StarletteRequest(scope, receive))

        response = JSONResponse(
            {
                "headers": dict(request.headers),
                "cookies": dict(request.cookies),
                "url": str(request.url),
                "method": request.method,
            }
        )

        await response(scope, receive, send)

    client = TestClient(app, cookies={"a": "1", "b": "2"})

    response = client.get("/")

    assert response.json() == snapshot(
        {
            "headers": {
                "host": "testserver",
                "accept": "*/*",
                "accept-encoding": "gzip, deflate",
                "connection": "keep-alive",
                "user-agent": "testclient",
                "cookie": "a=1; b=2",
            },
            "cookies": {"a": "1", "b": "2"},
            "url": "http://testserver/",
            "method": "GET",
        }
    )
