from flask import Flask, jsonify, make_response, request
from .models import PointSet, Triangles
from .core import triangulate
import urllib.request
import urllib.error
import struct
import uuid
import socket

# Configuration (idéalement dans des variables d'env)
MANAGER_URL = "http://pointsetmanager:5000/pointset"

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config:
        app.config.update(test_config)

    @app.route('/triangulation/<point_set_id>', methods=['GET'])
    def get_triangulation(point_set_id):
        # 1. Validation de l'UUID
        try:
            uuid.UUID(point_set_id)
        except ValueError:
            return jsonify({'code': 'BAD_REQUEST', 'message': 'Invalid UUID format'}), 400

        # 2. Validation Accept Header (Robustesse Client)
        accept_header = request.headers.get('Accept')
        if accept_header and 'application/json' in accept_header and 'application/octet-stream' not in accept_header:
             return jsonify({'code': 'NOT_ACCEPTABLE', 'message': 'Only application/octet-stream supported'}), 406

        # 3. Récupération des points depuis le PointSetManager
        manager_url = f"{MANAGER_URL}/{point_set_id}"
        
        try:
            # Appel avec urllib + Timeout (Robustesse Manager)
            req = urllib.request.Request(manager_url)
            with urllib.request.urlopen(req, timeout=2) as response:
                
                # 4. Validation Content-Type (Robustesse Réponse)
                content_type = response.headers.get('Content-Type', '')
                if 'application/octet-stream' not in content_type:
                     # Le manager renvoie n'importe quoi (ex: page HTML erreur)
                     return jsonify({'code': 'BAD_GATEWAY', 'message': 'Invalid Content-Type from Manager'}), 502

                data = response.read()
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return jsonify({'error': 'PointSet not found'}), 404
            return jsonify({'code': 'SERVICE_UNAVAILABLE', 'message': 'Manager Error'}), 503
        except (urllib.error.URLError, socket.timeout):
            return jsonify({'code': 'SERVICE_UNAVAILABLE', 'message': 'Manager Timeout/Unreachable'}), 503
        except Exception as e:
             return jsonify({'code': 'INTERNAL_ERROR', 'message': str(e)}), 500

        # 5. Désérialisation
        try:
            point_set = PointSet.from_bytes(data)
        except ValueError as e:
            # Données corrompues ou tronquées
            return jsonify({'code': 'INTERNAL_ERROR', 'message': f'Data corruption: {str(e)}'}), 500

        # 6. Calcul de la triangulation
        try:
            triangles_indices = triangulate(point_set.points)
            triangles = Triangles(point_set.points, triangles_indices)
        except Exception as e:
            return jsonify({'code': 'INTERNAL_ERROR', 'message': f'Algorithm failure: {str(e)}'}), 500
            
        # 7. Sérialisation et Réponse
        response_data = triangles.to_bytes()
        
        response = make_response(response_data)
        response.headers.set('Content-Type', 'application/octet-stream')
        return response

    return app
