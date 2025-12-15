import pytest
from unittest.mock import MagicMock
from triangulator.app import create_app

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_point_set_manager(mocker):
    
    mock_urlopen = mocker.patch('triangulator.app.urllib.request.urlopen')
    
    # mock de l'objet réponse retourné par urlopen
    mock_response = MagicMock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = b''
    mock_response.headers = {'Content-Type': 'application/octet-stream'}
    
    # configuration du context manager
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    return mock_urlopen
