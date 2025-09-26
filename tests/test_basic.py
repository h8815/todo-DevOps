import app as myapp


def test_homepage():
    # Create a test client to interact with the app
    client = myapp.app.test_client()

    # Make a GET request to the homepage, telling the client to follow any redirects.
    # This is necessary because the app is likely redirecting from the homepage,
    # for example, to a login page or another route.
    response = client.get("/", follow_redirects=True)

    # Now, we assert that the final status code after the redirect is 200,
    # meaning the page loaded successfully.
    assert response.status_code == 200
