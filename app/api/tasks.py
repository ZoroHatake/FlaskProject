from flask import jsonify
import sqlalchemy as sa


from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response
from app import db
from app.models import UserTask

# Gibt alle Tasks des aktuell authentifizierten Benutzers zurück
@bp.route('/tasks', methods=['GET'])
@token_auth.login_required
def get_tasks():
    user = token_auth.current_user()
# Nur Tasks des eingeloggten Users laden
    query = sa.select(UserTask).where(UserTask.user_id == user.id)
    tasks = db.session.scalars(query).all()
# Umwandlung in JSON-Struktur
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

# Gibt einen einzelnen Task zurück mit Zugriffsschutz
@bp.route('/tasks/<int:id>', methods=['GET'])
@token_auth.login_required
def get_task(id):
    user = token_auth.current_user()
    task = db.session.get(UserTask, id)
# Fehler, falls Task nicht existiert
    if task is None:
        return error_response(404, 'Task not found')
 # Zugriff nur für eigenen Task erlaubt
    if task.user_id != user.id:
        return error_response(403, 'Forbidden')

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority
    })
