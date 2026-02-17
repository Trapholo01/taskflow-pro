from flask import Blueprint, request, jsonify
from app import db
from app.models import Task
from datetime import date

tasks_bp = Blueprint('tasks', __name__)

# ── GET tasks for a project ──────────────────────────────────────
@tasks_bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
def get_tasks(project_id):
    status   = request.args.get('status')    # optional filter
    priority = request.args.get('priority')  # optional filter
    query = Task.query.filter_by(project_id=project_id)
    if status:   query = query.filter_by(status=status)
    if priority: query = query.filter_by(priority=priority)
    tasks = query.order_by(Task.due_date.asc()).all()
    return jsonify([t.to_dict() for t in tasks]), 200

# ── CREATE task ──────────────────────────────────────────────────
@tasks_bp.route('/projects/<int:project_id>/tasks', methods=['POST'])
def create_task(project_id):
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'title is required'}), 400
    due = None
    if data.get('due_date'):
        due = date.fromisoformat(data['due_date'])  # expects YYYY-MM-DD
    task = Task(
        project_id=project_id,
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'todo'),
        due_date=due
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

# ── UPDATE task ──────────────────────────────────────────────────
@tasks_bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    for field in ['title','description','priority','status']:
        if field in data: setattr(task, field, data[field])
    if 'due_date' in data:
        task.due_date = date.fromisoformat(data['due_date']) if data['due_date'] else None
    db.session.commit()
    return jsonify(task.to_dict()), 200

# ── DELETE task ──────────────────────────────────────────────────
@tasks_bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'Task {id} deleted'}), 200
