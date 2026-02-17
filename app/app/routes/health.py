from flask import Blueprint, jsonify
from app import db
from sqlalchemy import text

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    """
    Health check endpoint — used by AWS ALB Target Group.
    Returns 200 OK when app AND database are reachable.
    """
    try:
        db.session.execute(text('SELECT 1'))   # Test DB connection
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503
