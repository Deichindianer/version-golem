import json

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from tinydb import TinyDB, Query
from threading import Thread

from alerts import version_checks
from versions import get_latest_version


app = Flask(__name__)
api = Api(app)
db = TinyDB("db.json")


class Repository(Resource):

    def get(self, name):
        repository = Query()
        return db.search(repository.name == name)

    def put(self, name):
        request_data = request.get_json(force=True)
        author = request_data["author"]
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



api.add_resource(Repository, "/repository/<string:name>")
thread = Thread(target=version_checks, args=(db,))
thread.daemon = True
thread.start()
app.run(host="0.0.0.0", debug=True)
