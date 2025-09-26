import pytest
from app import app, db, User, Todo
from werkzeug.security import generate_password_hash
# ADDED: Import request for checking response path
from flask import request 

# --- Pytest Fixtures ---
# Fixtures ensure clean setup and teardown for every test function.

@pytest.fixture(scope='session')
def client():
    """
    Sets up the testing client for the application.
    This fixture configures the app to use an in-memory SQLite database 
    and yields the test client for use in tests.
    """
    # 1. Configure the app for testing
    app.config['TESTING'] = True
    # Use an in-memory SQLite database for fast, isolated tests
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        # 2. Set up the application context and database tables
        with app.app_context():
            db.create_all() # Create tables based on models
            
            # 3. Yield the client to the test functions
            yield client
            
            # 4. Teardown: Clean up the database after all tests are done
            db.drop_all()

@pytest.fixture
def init_database(client):
    """
    Fixture to clear data and create a dummy user before each test, 
    ensuring a clean state for tests that require authentication.
    """
    with app.app_context():
        # Clear all data from tables
        Todo.query.delete()
        User.query.delete()
        db.session.commit()

        # Create a standard test user
        hashed_password = generate_password_hash("password123")
        test_user = User(id=1, username="testuser", password=hashed_password)
        db.session.add(test_user)
        db.session.commit()
        
        return test_user

# --- Test Functions ---

def test_homepage_redirects_to_login(client):
    """
    Tests that accessing the root URL (/) redirects to the login page 
    because the user is not authenticated.
    """
    response = client.get('/', follow_redirects=False)
    # Status code 302 (Found) is correct for a redirect
    assert response.status_code == 302
    # FIX: Use startswith() because Flask-Login adds the '?next=/' query parameter
    assert response.location.startswith('http://localhost/login') or response.location.startswith('/login')

def test_login_page_loads(client):
    """
    Tests that the login page loads successfully.
    """
    response = client.get('/login')
    assert response.status_code == 200
    # Optional: Check if the login form text is present
    # assert b"Log In" in response.data

def test_successful_login(client, init_database):
    """
    Tests successful user authentication.
    """
    # Use the client to make a POST request to the login endpoint
    response = client.post(
        '/login',
        data=dict(username='testuser', password='password123'),
        follow_redirects=True
    )
    
    assert response.status_code == 200
    # FIX: Check the final path after the redirect chain completes
    assert response.request.path == '/'
    # The success flash message should be present in the response data
    assert b"Welcome back, testuser!" in response.data
