from flask import Flask, jsonify, abort, make_response, request
from google.cloud import datastore
import json

app = Flask(__name__)

@app.route('/')
def default():
    return '<h1>It works!</h1><br>This is estamp-dev api server.'

@app.route('/api/dev/like/<string:spotId>', methods=['GET'])
def retLikeCount(spotId):
    ds = datastore.Client()
    
    if spotId == 'all':
        query = ds.query(kind="Spot")
        query.order = ['likeCount']
        entity = list(query.fetch())
    else:
        entity = ds.get(ds.key('Spot', spotId))

    if entity == {} or entity is None:
        result = {
            "result": False,
            "data": {
                'spotId': spotId,
                'likeCount': 0
            }
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
    if entity == {} or entity is None:
        entity = datastore.Entity(ds.key('Spot', spotId))
        entity.update({
            'spotId': spotId,
            'likeCount': 1
        })
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

@app.route('/api/dev/ranking', methods=['PUT'])
def putRanking():
    ds = datastore.Client()

    if request is None:
        result = {
            'result': False
        }
    else:
        res = json.loads(request.data.decode('utf-8'))
        deviceId = res['id']

        entity = ds.get(ds.key('Ranking', res['id']))
        if entity == {} or entity is None:
            entity = datastore.Entity(ds.key('Ranking', deviceId))
            entity.update({
                'deviceId': deviceId,
                'stampCount': res['stampCount']
            })
        else:
            entity['stampCount'] = res['stampCount']
        ds.put(entity)

        query = ds.query(kind="Ranking")
        query.order = ['-stampCount']
        entity = list(query.fetch())
        rank = 0
        for i, l in enumerate(entity):
            if l['deviceId'] == deviceId:
                rank = i + 1
                break

        result = {
            'result': True,
            'data': {
                'deviceId': deviceId,
                'ranking': rank
            }
        }

    return make_response(jsonify(result))
        

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)