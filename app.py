import flask
from flask import jsonify, send_file, send_from_directory, abort
import os
from flask_cors import CORS

from werkzeug.utils import safe_join

# cors = flask_cors.CORS()


app = flask.Flask(__name__)
app.debug = True

CORS(app)

# cors.init_app(app)


@app.route('/')
def index():
    return {"Hello": "World"}, 200


@app.route('/model')
def export_model():
    # weights_data = {}
    # with open("models/modelvTest.json") as model_file:
    #     print("open json file ...")
    #     data = json.load(model_file)
    # with open("models/modelvTest.weights.h5") as weights_file:
    #     print("open weights json file ...")
    #     weights_data = json.load(weights_file)
    #     print(jsonify({'modelTopology': data, 'weightsManifest': weights_data}))
        
    #     return jsonify({'modelTopology': data, 'weightsManifest': weights_data })

    model_path = "../runs/detect/train22/weights/best_web_model/model.json"
    print("model path: ", model_path)
    if os.path.exists(model_path):
        return send_file(model_path, as_attachment=True)
    else:
        return jsonify({'error': 'Model file not found'}), 404


# Define the directory you want to serve files from
# UPLOAD_DIRECTORY = "../runs/detect/train22/weights/best_web_model"
UPLOAD_DIRECTORY = "yolo_tfjsmodel"
@app.route('/modelfiles/<path:filename>', methods=['GET'])
def download_file(filename):
    try:
        # Ensure the file path is safe
        file_path = safe_join(UPLOAD_DIRECTORY, filename)
        
        # Check if the file exists
        if os.path.isfile(file_path):
            return send_from_directory(UPLOAD_DIRECTORY, filename, as_attachment=True)
        else:
            abort(404)  # File not found
    except Exception as e:
        abort(500)  # Internal server error


if __name__ == '__main__':
    app.run()