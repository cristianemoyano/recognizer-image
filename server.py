import os
import sys
import uuid

from flask import Flask, request, jsonify
from openalpr import Alpr

app = Flask(__name__)

alpr = Alpr("eu", "/openalpr/config/alprd.conf.defaults", "/openalpr/runtime_data")

if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(20)
alpr.set_default_region("md")


@app.route('/', methods=['POST'])
def get_plate_number():
    filename = str(uuid.uuid4())
    path_join = os.path.join("/tmp", filename)

    multipart_file = request.files['']
    multipart_file.save(path_join)
    results = alpr.recognize_file(path_join)
    os.remove(path_join)
    return jsonify(results['results'])


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run()
