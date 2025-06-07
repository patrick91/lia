from lia import Response


def test_redirect():
    response = Response.redirect("https://example.com")
    assert response.status_code == 302
    assert response.headers["Location"] == "https://example.com"


def test_redirect_with_query_params():
    response = Response.redirect("https://example.com", {"a": "1", "b": "2"})
    assert response.status_code == 302
    assert response.headers["Location"] == "https://example.com?a=1&b=2"


def test_redirect_with_headers():
    response = Response.redirect("https://example.com", headers={"X-Test": "test"})
    assert response.status_code == 302
    assert response.headers["Location"] == "https://example.com"
    assert response.headers["X-Test"] == "test"
