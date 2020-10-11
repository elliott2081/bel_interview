
import pytest


@pytest.fixture
def expected_routes():
    """return expected values for all routes"""
    return {
        "spectrum": {
            "methods": {'OPTIONS', 'POST', 'GET', 'HEAD'},
            "params": {'sampling_rate', 'units', 'dtype'},
        },
        "mean": {
            "methods": {'OPTIONS', 'POST', 'GET', 'HEAD'},
            "params": {'dtype',},
        },
        "median": {
            "methods": {'OPTIONS', 'POST', 'GET', 'HEAD'},
            "params": {'dtype',},
        },
    }


def test_routes_are_available(client, app, expected_routes):
    """test that all routes are available"""
    response = client.get('/')
    assert response.status_code == 200
    routes = response.get_json()
    assert len(routes) == len(expected_routes)
    assert all(route in routes for route in expected_routes)


def test_routes_have_right_methods(client, app, expected_routes):
    """test that the routes allow the correct methods"""
    routes = client.get('/').get_json()
    for name, route in routes.items():
        expected_methods = expected_routes[name]['methods']
        response = client.options(route)
        methods = response.headers.get('Allow')
        methods = { m.strip() for m in methods.split(',') }
        assert expected_methods == methods


def test_routes_require_right_methods(client, app, expected_routes):
    """test that the routes allow the correct methods"""
    routes = client.get('/').get_json()
    for name, route in routes.items():
        expected_params = expected_routes[name]['params']
        params = set(client.get(route).get_json()['params'])
        assert params == expected_params
