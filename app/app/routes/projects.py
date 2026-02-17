from flask import Blueprint, request, jsonify
from app import db
from app.models import Project

projects_bp = Blueprint('projects', __name__)

# ── GET all projects ─────────────────────────────────────────────
@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return jsonify([p.to_dict() for p in projects]), 200

# ── GET single project ───────────────────────────────────────────
@projects_bp.route('/projects/<int:id>', methods=['GET'])
def get_project(id):
    project = Project.query.get_or_404(id)
    return jsonify(project.to_dict()), 200

# ── CREATE project ───────────────────────────────────────────────
@projects_bp.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    project = Project(name=data['name'], description=data.get('description', ''))
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict()), 201

# ── UPDATE project ───────────────────────────────────────────────
@projects_bp.route('/projects/<int:id>', methods=['PUT'])
def update_project(id):
    project = Project.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:        project.name        = data['name']
    if 'description' in data: project.description = data['description']
    db.session.commit()
    return jsonify(project.to_dict()), 200

# ── DELETE project ───────────────────────────────────────────────
@projects_bp.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': f'Project {id} deleted'}), 200
