import base64
from flask import Flask
import numpy as np
from flask import request


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def routes():
        return {
            "spectrum": "/spectrum",
            "mean": "/mean",
            "median": "/median",
        }

    @app.route('/spectrum', methods=['POST', 'GET'])
    def spectrum():
        if request.method == 'GET':
            return {'params': ['sampling_rate', 'units', 'dtype']}

        req = request.get_json()
        sr = float(req['sampling_rate'])
        units = req["units"]
        dtype = req['dtype'] if 'dtype' in req else "float64"
        spectrum = np.frombuffer(base64.b64decode(req["spectrum"].encode('utf-8')), dtype=dtype).tolist()
        samples_per_signal = len(spectrum)
        duration = samples_per_signal / sr
        return {'spectrum': spectrum}

    @app.route('/mean', methods=['POST', 'GET'])
    def mean():
        if request.method == 'GET':
            return {'params': ['dtype']}

        req = request.get_json()
        dtype = req['dtype'] if 'dtype' in req else "float64"
        spectrum = np.frombuffer(base64.b64decode(req["spectrum"].encode('utf-8')), dtype=dtype).tolist()
        samples_per_signal = len(spectrum)
        return {'mean': np.mean(spectrum)}

    @app.route('/median', methods=['POST', 'GET'])
    def median():
        if request.method == 'GET':
            return {'params': ['dtype']}

        req = request.get_json()
        dtype = req['dtype'] if 'dtype' in req else "float64"
        spectrum = np.frombuffer(base64.b64decode(req["spectrum"].encode('utf-8')), dtype=dtype).tolist()
        samples_per_signal = len(spectrum)
        return {'median': np.median(spectrum)}

    return app
