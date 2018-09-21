from flask import Flask, jsonify, abort, make_response
from google.cloud import datastore

app = Flask(__name__)

@app.route('/')
def default():
    return '<h1>It works!</h1><br>This is estamp-dev api server.'

@app.route('/api/dev/like/<string:spotId>', methods=['GET'])
def retLikeCount(spotId):
    ds = datastore.Client()
    
    entity = ds.get(ds.key('Spot', spotId))
    if entity == {}:
        result = {
            "result": False
        }
    else:
        result = {
            "result": True,
            "data": entity
        }
        
    return make_response(jsonify(result))

@app.route('/api/dev/like/<string:spotId>', methods=['PUT'])
def putLikeCount(spotId):
    ds = datastore.Client()
    
    entity = ds.get(ds.key('Spot', spotId))
    if entity == {}:
        entity['likeCount'] = 1
        create = True
    else:
        entity['likeCount'] +=  1
        create = False
    ds.put(entity)

    result = {
        "result": True,
        "create": create
    }

    return make_response(jsonify(result))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)