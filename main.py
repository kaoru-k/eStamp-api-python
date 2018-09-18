from flask import Flask, jsonify, abort, make_response
import peewee

db = peewee.SqliteDatabase("db/data.db")

class Spot(peewee.Model):
    spotId = peewee.IntegerField()
    likeCount = peewee.IntegerField()

    class Meta:
        database = db

app = Flask(__name__)

@app.route('/')
def default():
    return '<h1>It works!</h1><br>This is estamp-dev api server.'

@app.route('/api/dev/like/<string:spotId>', methods=['GET'])
def retLikeCount(spotId):
    try:
        spot = Spot.get(Spot.spotId == spotId)
    except Spot.DoesNotExist:
        abort(404)
    
    result = {
        "result": True,
        "data": {
            "spotId": spot.spotId,
            "likeCount": spot.likeCount
        }
    }

    return make_response(jsonify(result))

@app.route('/api/dev/like/<string:spotId>', methods=['PUT'])
def putLikeCount(spotId):
    try:
        q = Spot.update(likeCount=Spot.likeCount+1).where(Spot.spotId == spotId)
        q.execute()
    except Spot.DoesNotExist:
        abort(404)

    result = {
        "result": True,
    }
    return make_response(jsonify(result))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)