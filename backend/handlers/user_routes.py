"""
This module contains the route handlers for user-related operations.
"""
from flask import Blueprint, jsonify, request
from flask_security import auth_required, login_user, logout_user, current_user, roles_required, roles_accepted
from flask_security.utils import verify_password
from db.models import User, Role
from functools import wraps
import logging


def create_user_bp(user_datastore):
    user_bp = Blueprint('user', __name__)

    def coach_or_medical_required(f):
        @wraps(f)
        @auth_required()
        @roles_accepted('coach', 'medical')
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated

    @user_bp.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = user_datastore.find_user(email=data.get('email'))

        logging.info("user in login: %s", user)
        if user and verify_password(data.get('password'), user.password):
            user_roles = [role.name for role in user.roles]
            logging.info("user roles in login: %s", user_roles)
            login_user(user)
            return jsonify({"message": "Logged in successfully"}), 200
        return jsonify({"message": "Invalid email or password"}), 401

    @user_bp.route('/logout', methods=['POST'])
    @auth_required()
    def logout():
        logout_user()
        return jsonify({"message": "Logged out successfully"}), 200

    @user_bp.route('/user', methods=['GET'])
    @auth_required()
    def get_user():
        return jsonify({
            "id": current_user.id,
            "email": current_user.email,
            "roles": [role.name for role in current_user.roles]
        }), 200

    @user_bp.route('/coach-only', methods=['GET'])
    @roles_required('coach')
    def coach_only():
        return jsonify({"message": "This is a coach-only route"}), 200

    @user_bp.route('/medical-only', methods=['GET'])
    @roles_required('medical')
    def medical_only():
        return jsonify({"message": "This is a medical-only route"}), 200

    @user_bp.route('/coach-or-medical', methods=['GET'])
    @coach_or_medical_required
    def coach_or_medical():
        return jsonify({"message": "This route is accessible by both coach and medical staff"}), 200

    @user_bp.route('/user-info', methods=['GET'])
    @auth_required()
    def user_info():
        print(f"current_user: {current_user}")
        return jsonify({
            "email": current_user.email,
            "roles": [role.name for role in current_user.roles]
        }), 200

    return user_bp

# Function to set up initial roles (call this during app initialization)


def setup_roles(user_datastore):
    """
   Set up roles in the user datastore.

   Args:
       user_datastore: The datastore to find or create roles in.
   """
    user_datastore.find_or_create_role(name="coach", description="Coach role")
    user_datastore.find_or_create_role(
        name="medical", description="Medical staff role")
    user_datastore.commit()
