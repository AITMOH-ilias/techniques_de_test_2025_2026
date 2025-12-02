import pytest
from unittest.mock import MagicMock

# from triangulator.app import create_app

@pytest.fixture
def app():

    # Création de l'app à implémenter
    # app = create_app()
    

    # app.config.update({
    #     "TESTING": True,
    # })
    
    # yield app
    
    # pour l'instant, on renvoie un objet vide pour ne pas faire planter pytest
    yield MagicMock()


@pytest.fixture
def client(app):
    #
    # Ce client permet d'envoyer des requêtes HTTP (GET, POST) à votre application
    # sans lancer un vrai serveur.
    # Utilisé dans : tests/integration/test_api.py
    #
    # return app.test_client()
    
    return MagicMock()


@pytest.fixture
def mock_point_set_manager(mocker):
    
    # mock_get = mocker.patch('triangulator.services.fetch_point_set') 
    
    # configuration par défaut du mock :
    # On crée une fausse réponse HTTP avec un statut 200 
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'' # Contenu vide par défaut
    
    # quand on appellera notre fonction mockée, elle renverra cette réponse
    # mock_get.return_value = mock_response
    
    # return mock_get

    return MagicMock()