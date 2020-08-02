import json

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from tinydb import TinyDB, Query


app = Flask(__name__)
api = Api(app)
db = TinyDB("db.json")


def update_repository(repository):
    """
    Takes in a dict with a new repository and updates the thing :)
    """


class Repository(Resource):

    def get(self, name):
        repository = Query()
        return db.search(repository.name == name)

    def put(self, name):
        request_data = request.get_json(force=True)
        repository = Query()
        db.upsert(request_data, repository.name == request_data["name"])
        return jsonify(request_data)


class Repositories(Resource):

    def get(self):
        repository = Query()
        return db.all()

    def post(self):
        request_data = request.get_json(force=True)
        author = request_data["author"]
        name = request_data["name"]
        repository = Query()
        db.upsert(
            {
                "name": name,
                "author": author,
                "tracked_version": request_data["tracked_version"],
                "latest_version": "To be updated",
                "latest_release_url": "To be updated",
                "latest_version_publish_date": "To be updated"
            },
            repository.name == name
        )
        return jsonify(request_data)


api.add_resource(Repositories,"/repositories")
api.add_resource(Repository,"/repository/<string:name>")
app.run(host="0.0.0.0", debug=True)
