from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

mongo_uri = os.getenv("MONGODB_URI")

client = MongoClient(mongo_uri)

db = client["taskdb"]
tasks_collection = db["tasks"]


@app.route("/health")
def health():
    try:
        client.admin.command("ping")

        return jsonify({
            "status": "ok",
            "database": "connected"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = list(tasks_collection.find())

    for task in tasks:
        task["_id"] = str(task["_id"])

    return jsonify(tasks)


@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({
            "error": "Task title is required"
        }), 400

    task = {
        "title": data["title"],
        "completed": False
    }

    result = tasks_collection.insert_one(task)

    return jsonify({
        "message": "Task added",
        "id": str(result.inserted_id)
    }), 201


@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    from bson import ObjectId

    result = tasks_collection.delete_one({
        "_id": ObjectId(task_id)
    })

    if result.deleted_count == 0:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "message": "Task deleted"
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )