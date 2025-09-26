from myapp import app

def test_homepage_redirects_and_loads_login():
    client = app.test_client()
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data  # check login page content