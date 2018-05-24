from flask import Flask, request, jsonify, abort, send_file, render_template
from bson import ObjectId
from flask_swagger_ui import get_swaggerui_blueprint

from db import db, JSONEncoder
import utils

app = Flask(__name__)
app.config.from_object('settings')

# Enhance jsonify to be able to work with ObjectId
app.json_encoder = JSONEncoder

# Setup swagger UI
app.register_blueprint(get_swaggerui_blueprint(
    '/apidocs', '/swagger.json',
), url_prefix='/apidocs')


@app.route('/')
def home():
    return send_file('frontend.html')


@app.route('/level3', methods=['GET', 'POST', 'DELETE'])
def level3():
    if request.method == 'POST':
        # Add new level3 doc
        data = request.json
        data['_rundate'] = utils.parse_rundate(data['RUNDATE'])
        r = db.level3.insert_one(request.json)
        return jsonify({'id': r.inserted_id})
    if request.method == 'DELETE':
        # Add new level3 doc
        r = db.level3.delete_many({})
        return jsonify({'deleted': r.deleted_count})
    # Get all the level3 docs
    return jsonify(list(db.level3.find({}, {'level4': 0})))


@app.route('/level3/last')
def level3_last():
    # Get last record based on run date
    return jsonify(db.level3.find_one(sort=[('_rundate', -1)]))


@app.route('/level3/<id>', methods=['GET', 'POST', 'DELETE'])
def level3_item(id):
    filter = {'_id': ObjectId(id)}
    if request.method == 'POST':
        # Replace single doc with a new one
        r = db.level3.replace_one(filter, request.json)
        return jsonify({'modified': r.modified_count})
    if request.method == 'DELETE':
        # Delete the doc
        r = db.level3.delete_one(filter)
        return jsonify({'deleted': r.deleted_count})
    # Get single level3 doc by id
    doc = db.level3.find_one(filter)
    if not doc:
        abort(404)
    return jsonify(doc)


@app.route('/swagger.json')
def swagger_json():
    return send_file('./swagger.json')


if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])
