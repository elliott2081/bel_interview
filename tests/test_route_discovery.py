
import pytest
import json

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

def test_index(app, client):
    """test that / path has expected params"""
    res = client.get('/')
    assert res.status_code == 200
    expected = {'mean': '/mean', 'median': '/median', 'spectrum': '/spectrum'}
    assert expected == json.loads(res.get_data(as_text=True))

def test_mean(app, client):
    """test that /mean path has expected params"""
    res = client.get('/mean')
    assert res.status_code == 200
    expected = {'params': ['dtype']}
    assert expected == json.loads(res.get_data(as_text=True))

def test_median(app, client):
    """test that /median path has expected params"""
    res = client.get('/median')
    assert res.status_code == 200
    expected = {'params': ['dtype']}
    assert expected == json.loads(res.get_data(as_text=True))

def test_median_post(app, client):
    """test that /median POST has expected values"""
    res = client.post('/median', json={"dtype": "uint8", "spectrum": "{1,2,3,900===}"})
    assert res.status_code ==200
    expected = {'median': 213.0}
    assert expected == json.loads(res.get_data(as_text=True))

def test_spectrum(app, client):
    """test that /spectrum path has expected params"""
    res = client.get('/spectrum')
    assert res.status_code == 200
    expected = {"params": ["sampling_rate", "units", "dtype"]}
    assert expected == json.loads(res.get_data(as_text=True))

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
