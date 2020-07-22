import json

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from tinydb import TinyDB, Query
from threading import Thread

from versions import get_latest_version


app = Flask(__name__)
api = Api(app)
db = TinyDB("db.json")


class Repositories(Resource):

    def get(self, name=None):
        repository = Query()
        if name is None:
            return db.all()
        return db.search(repository.name == name)

    def put(self, name=None):
        request_data = request.get_json(force=True)
        author = request_data["author"]
        name = request_data["name"]
        latest_version = get_latest_version(f"{author}/{name}")
        repository = Query()
        db.upsert(
            {
                "name": name,
                "author": author,
                "tracked_version": request_data["tracked_version"],
                "latest_version": latest_version
            },
            repository.name == name
        )
        return 200


api.add_resource(
    Repositories,
    "/repositories",
    "/repositories/<string:name>",
    defaults={"name": None}
)
app.run(host="0.0.0.0", debug=True)
