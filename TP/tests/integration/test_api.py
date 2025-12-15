import pytest
from unittest.mock import MagicMock, patch
import urllib.error

# UUID valide pour les tests
VALID_UUID = "123e4567-e89b-12d3-a456-426614174000"
INVALID_UUID = "invalid-uuid"

def creer_binaire_pointset_simule():
    from triangulator.models import PointSet
    # 3 points pour un triangle simple
    # On simule la sérialisation décrite dans PointSet.to_bytes
    import struct
    data = struct.pack('>I', 3)
    data += struct.pack('>ff', 0.0, 0.0)
    data += struct.pack('>ff', 1.0, 0.0)
    data += struct.pack('>ff', 0.0, 1.0)
    return data

def test_obtenir_triangulation(client, mock_point_set_manager):
    
    # 1. le client appelle GET /triangulation/{uuid}.
    # 2. le Triangulator appelle le PointSetManager.
    # 3. le PointSetManager retourne un binaire valide (mock?).
    # 4. le Triangulator retourne 200 OK et un binaire 'Triangles'.

    # le PointSetManager renvoie des données binaires valides
    # urllib response mock config
    mock_point_set_manager.return_value.__enter__.return_value.getcode.return_value = 200
    mock_point_set_manager.return_value.__enter__.return_value.read.return_value = creer_binaire_pointset_simule()
    mock_point_set_manager.return_value.__enter__.return_value.headers = {'Content-Type': 'application/octet-stream'}

    # on appelle l'API du Triangulator (avec Accept correct par défaut ou expliite)
    response = client.get(f'/triangulation/{VALID_UUID}', headers={'Accept': 'application/octet-stream'})

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/octet-stream'

    # le PointSetManager a bien été appelé avec le bon ID 
    mock_point_set_manager.assert_called_once()
    request_obj = mock_point_set_manager.call_args[0][0]
    assert VALID_UUID in request_obj.full_url
    assert len(response.data) > 0 


def test_triangulation_pointset_introuvable(client, mock_point_set_manager):

    # le PointSetManager renvoie 404 (via HTTPError pour urllib)
    err = urllib.error.HTTPError(
        url="http://mock", code=404, msg="Not Found", hdrs={}, fp=None
    )
    mock_point_set_manager.side_effect = err
    
    # appel API
    response = client.get(f'/triangulation/{VALID_UUID}')
    
    # le Triangulator répond 404
    assert response.status_code == 404
    assert response.is_json
    assert "error" in response.json or "message" in response.json


def test_triangulation_manager_indisponible(client, mock_point_set_manager): 
    # la connexion au Manager échoue (URLError => Timeout ou Connection Refused)
    
    mock_point_set_manager.side_effect = urllib.error.URLError("Connection refused")

    response = client.get(f'/triangulation/{VALID_UUID}')
    
    # Le trianglator répond 503 (Service Unavailable)
    assert response.status_code == 503
    assert response.is_json


def test_triangulation_uuid_invalide(client, mock_point_set_manager):

    # appel avec un ID malformé
    response = client.get(f'/triangulation/{INVALID_UUID}')
    
    # Erreur 400 ou 404 (idéalement 400 Bad Request pour UUID en path params)
    assert response.status_code in (400, 404)

def test_triangulation_algorithme_echec(client, mock_point_set_manager):
    # Données corrompues (MOCK 200 OK mais données invalides)
    mock_point_set_manager.return_value.__enter__.return_value.getcode.return_value = 200
    mock_point_set_manager.return_value.__enter__.return_value.read.return_value = b'\x00\x00\x00\x01' # Malformé
    mock_point_set_manager.return_value.__enter__.return_value.headers = {'Content-Type': 'application/octet-stream'}
    
    # appel API
    response = client.get(f'/triangulation/{VALID_UUID}')
    
    # Le Triangulator gère l'exception interne et renvoie 500
    assert response.status_code == 500
    assert response.json['code'] == 'INTERNAL_ERROR'

# --- Nouveaux Tests de Robustesse (Protocol) ---

def test_client_accept_header_invalide(client):
    # Le client demande du JSON, on ne supporte que octet-stream
    response = client.get(f'/triangulation/{VALID_UUID}', headers={'Accept': 'application/json'})
    # Doit être 406 Not Acceptable
    assert response.status_code == 406

def test_manager_timeout(client, mock_point_set_manager):
    # Simulation d'un timeout (socket.timeout souvent wrap dans URLError)
    import socket
    mock_point_set_manager.side_effect = socket.timeout("timed out")
    
    response = client.get(f'/triangulation/{VALID_UUID}')
    assert response.status_code == 503

def test_manager_bad_content_type(client, mock_point_set_manager):
    # Le manager répond 200 mais envoie du HTML
    mock_point_set_manager.return_value.__enter__.return_value.getcode.return_value = 200
    mock_point_set_manager.return_value.__enter__.return_value.read.return_value = b'<html>Error</html>'
    mock_point_set_manager.return_value.__enter__.return_value.headers = {'Content-Type': 'text/html'}

    response = client.get(f'/triangulation/{VALID_UUID}')
    
    # On attend 502 Bad Gateway (réponse invalide du upstream) ou 500
    assert response.status_code in (500, 502)

def test_reception_body_tronque(client, mock_point_set_manager):
     # Le manager renvoie moins de données que prévu
     mock_point_set_manager.return_value.__enter__.return_value.getcode.return_value = 200
     # Seulement 4 bytes
     mock_point_set_manager.return_value.__enter__.return_value.read.return_value = b'\x00\x00\x00\x01' 
     mock_point_set_manager.return_value.__enter__.return_value.headers = {'Content-Type': 'application/octet-stream'}

     response = client.get(f'/triangulation/{VALID_UUID}')
     # 500 ou 502
     assert response.status_code in (500, 502)

# --- Tests de Couverture Manquants (AJOUTE) ---

def test_manager_http_error_generic(client, mock_point_set_manager):
    # Covers app.py line 51: return jsonify({'code': 'SERVICE_UNAVAILABLE', 'message': 'Manager Error'}), 503
    # Trigger HTTPError with code != 404 (e.g. 500)
    err = urllib.error.HTTPError(
        url="http://mock", code=500, msg="Server Error", hdrs={}, fp=None
    )
    mock_point_set_manager.side_effect = err
    
    response = client.get(f'/triangulation/{VALID_UUID}')
    
    assert response.status_code == 503
    assert response.json['code'] == 'SERVICE_UNAVAILABLE'
    assert response.json['message'] == 'Manager Error'

def test_manager_unexpected_exception(client, mock_point_set_manager):
    # Covers app.py lines 54-55: except Exception as e: ...
    # Trigger a generic Exception
    mock_point_set_manager.side_effect = Exception("Surprise Error")
    
    response = client.get(f'/triangulation/{VALID_UUID}')
    
    assert response.status_code == 500
    assert response.json['code'] == 'INTERNAL_ERROR'
    assert "Surprise Error" in response.json['message']

def test_algorithm_generic_failure_mocking_triangulate(client, mock_point_set_manager):
    # Covers app.py lines 68-69: except Exception as e: return ... Algorithm failure
    
    with patch('triangulator.app.triangulate') as mock_algo:
        mock_algo.side_effect = Exception("Geometry Chaos")
        
        # Setup manager to return valid data so we reach the algo step
        mock_point_set_manager.return_value.__enter__.return_value.getcode.return_value = 200
        mock_point_set_manager.return_value.__enter__.return_value.read.return_value = creer_binaire_pointset_simule()
        mock_point_set_manager.return_value.__enter__.return_value.headers = {'Content-Type': 'application/octet-stream'}
        # Clear side_effect
        mock_point_set_manager.side_effect = None

        response = client.get(f'/triangulation/{VALID_UUID}')
        
        assert response.status_code == 500
        assert response.json['code'] == 'INTERNAL_ERROR'
        assert "Algorithm failure: Geometry Chaos" in response.json['message']
