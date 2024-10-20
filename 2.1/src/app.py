from flask import Flask, request, jsonify
from flask_restful import Api, Resource 

from db import db
from models import Task


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db.init_app(app)

with app.app_context():
    db.create_all()


class TaskListResource(Resource):
    def get(self):
        tasks = Task.query.all()
        return jsonify([{
            'id': task.id,
            'title': task.title,
            'content': task.content,
            'done': task.done
        } for task in tasks])

    def post(self):
        data = request.json
        new_task = Task(title=data['title'], content=data.get('content', ''), done=False)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({
            'id': new_task.id,
            'title': new_task.title,
            'content': new_task.content,
            'done': new_task.done
        })


class TaskResource(Resource):
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return jsonify({
            'id': task.id,
            'title': task.title,
            'content': task.content,
            'done': task.done
        })

    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        data = request.json
        task.title = data.get('title', task.title)
        task.content = data.get('content', task.content)
        task.done = data.get('done', task.done)
        db.session.commit()
        return jsonify({
            'id': task.id,
            'title': task.title,
            'content': task.content,
            'done': task.done
        })

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return '', 204
    

api.add_resource(TaskListResource, '/')
api.add_resource(TaskResource, '/<int:task_id>')


if __name__ == '__main__':
    app.run(debug=True)

