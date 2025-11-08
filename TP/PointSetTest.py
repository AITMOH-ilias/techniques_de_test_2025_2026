from unittest.mock import patch

def test_pointset_get_points_mock():
    # On crée un objet PointSet, pas besoin que get_points soit implémentée
    ps = PointSet(points=None)
    
    # On mocke la méthode get_points
    with patch.object(PointSet, "get_points", return_value=[(1.0, 2.0), (3.0, 4.0)]) as mock_get:
        points = ps.get_points()  # appel du mock
        assert points == [(1.0, 2.0), (3.0, 4.0)]
        mock_get.assert_called_once()  # vérifie que la méthode a bien été appelée
