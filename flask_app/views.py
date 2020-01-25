import json
from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api

from .extensions import db
from .models import Task

main = Blueprint('main', __name__)
api = Api(main)

class TaskListCreate(Resource):

	def get(self):
		tasks = Task.query.all()
		return jsonify(self.parse_objects(tasks))
	
	def parse_objects(self, tasks):
		tasks_lst = []
		for task in tasks:
			obj = {}
			obj['id'] = task.id
			obj['taskname'] = task.name
			obj['created_at'] = task.created_at
			tasks_lst.append(obj)
		return tasks_lst

	def post(self):
		taskname = request.json.get("taskname")
		task = Task(name=taskname)
		db.session.add(task)
		db.session.commit()
		return jsonify(
			{
				"id":task.id, "taskname":task.name, "created_at":task.created_at
			}
		)

class TaskRUD(Resource):

	def get_object(self, id):
		task = Task.query.get_or_404(id)
		return task

	def delete(self, id):
		task = self.get_object(id)
		db.session.delete(task)
		db.session.commit()
		return jsonify({"message":"Task removed successfully"})

	def get(self, id):
		task =  self.get_object(id)
		return jsonify(
                    {
                        "id": task.id, "taskname": task.name, "created_at": task.created_at
                    }
                )
	
	def put(self, id):
		task = self.get_object(id)
		new_taskname = request.json.get("taskname")
		task.name = new_taskname
		db.session.commit()
		return jsonify(
                    {
                        "id": task.id, "taskname": task.name, "created_at": task.created_at
                    }
                )

api.add_resource(TaskListCreate, '/')
api.add_resource(TaskRUD, '/<int:id>/')
