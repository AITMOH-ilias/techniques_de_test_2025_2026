import pytest
import struct
from unittest.mock import MagicMock

# Constantes pour les tests
VALID_UUID = "123e4567-e89b-12d3-a456-426614174000"
INVALID_UUID = "invalid-uuid-format"

def creer_binaire_pointset_simule():

    # créer un binaire PointSet valide (3 points, un triangle).

    # - 4 bytes (unsigned long) : Nombre de points (3)
    # - 3 * 8 bytes : (float X, float Y)

    nb_points = 3
    points = [0.0, 0.0, 1.0, 0.0, 0.0, 1.0]
    
    # Pack: >I (Big-endian unsigned int), >ffffff (6 floats big-endian)
    binary_data = struct.pack('>I', nb_points) + struct.pack('>ffffff', *points)
    return binary_data

def test_obtenir_triangulation(client, mock_point_set_manager):

    
    # 1. le client appelle GET /triangulation/{uuid}.
    # 2. le Triangulator appelle le PointSetManager.
    # 3. le PointSetManager retourne un binaire valide (mocké).
    # 4. le Triangulator retourne 200 OK et un binaire 'Triangles'.

    # le PointSetManager renvoie des données binaires valides
    mock_point_set_manager.return_value.status_code = 200
    mock_point_set_manager.return_value.content = creer_binaire_pointset_simule()
    
    # on appelle l'API du Triangulator
    response = client.get(f'/triangulation/{VALID_UUID}')
    

    assert response.status_code == 200
    
    assert response.headers['Content-Type'] == 'application/octet-stream'
    
    # le PointSetManager a bien été appelé avec le bon ID 
    mock_point_set_manager.assert_called_once()
    assert VALID_UUID in mock_point_set_manager.call_args
    assert len(response.data) > 0 


def test_triangulation_pointset_introuvable(client, mock_point_set_manager):

    
    # le PointSetManager renvoie 404, le Triangulator doit propager 404.
    mock_point_set_manager.return_value.status_code = 404
    
    # appel API
    response = client.get(f'/triangulation/{VALID_UUID}')
    
    # le Triangulator répond 404
    assert response.status_code == 404
    assert response.is_json
    assert "error" in response.json or "message" in response.json


def test_triangulation_manager_indisponible(client, mock_point_set_manager): 
    # la connexion au Manager échoue le Triangulator répond 503.


    mock_point_set_manager.side_effect = Exception("Connection Error")
    

    response = client.get(f'/triangulation/{VALID_UUID}')
    
    # Le trianglator répond 503 (Service Unavailable)
    assert response.status_code == 503
    assert response.is_json


def test_triangulation_uuid_invalide(client):

    # appel avec un ID malformé
    response = client.get(f'/triangulation/{INVALID_UUID}')
    
    # Erreur 404 (si route non matchée) ou 400 (Bad Request)
    assert response.status_code in (400, 404)

def test_triangulation_algorithme_echec(client, mock_point_set_manager):
    # si les données sont corrompues ou l'algo plante, on doit renvoyer 500.

    # Données corrompues (bytes aléatoires)
    mock_point_set_manager.return_value.status_code = 200
    mock_point_set_manager.return_value.content = b'\x00\x00\x00\x01' # Header incomplet/invalide
    
    # appel API
    response = client.get(f'/triangulation/{VALID_UUID}')
    
    # Le Triangulator gère l'exception interne et renvoie 500
    assert response.status_code == 500
    assert response.is_json
    # assert response.json['code'] == 'TRIANGULATION_FAILED' 