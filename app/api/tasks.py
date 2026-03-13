from flask import jsonify
import sqlalchemy as sa

from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response
from app import db
from app.models import UserTask


@bp.route('/tasks', methods=['GET'])
@token_auth.login_required
def get_tasks():
    user = token_auth.current_user()
    query = sa.select(UserTask).where(UserTask.user_id == user.id)
    tasks = db.session.scalars(query).all()

    data = []
    for task in tasks:
        data.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority
        })

    return jsonify(data)


@bp.route('/tasks/<int:id>', methods=['GET'])
@token_auth.login_required
def get_task(id):
    user = token_auth.current_user()
    task = db.session.get(UserTask, id)

    if task is None:
        return error_response(404, 'Task not found')

    if task.user_id != user.id:
        return error_response(403, 'Forbidden')

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority
    })