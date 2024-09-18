from flask import Blueprint, request, jsonify, make_response
from flask_bcrypt import Bcrypt
import jwt
import datetime
from functools import wraps
from sqlalchemy import text
from db.models import User
import logging
import os

bcrypt = Bcrypt()

def create_user_bp(db_session, app):
    user_bp = Blueprint('user', __name__, url_prefix='/user')


    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Set up logging
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.DEBUG)

            # Check if we're running in local development mode
            if os.environ.get('FLASK_ENV') == 'development':
                logger.debug("Development mode detected, skipping authentication")
                return f(None, *args, **kwargs)
            
            token = None
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else auth_header
            
            if not token:
                logger.warning("Token is missing in the request")
                response = jsonify({'message': 'Token is missing!', 'error': 'Unauthorized'})
                response.status_code = 401
                return response
            
            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = User.query.filter_by(id=data['user_id']).first()
                if not current_user:
                    logger.warning(f"No user found for token payload: {data}")
                    raise ValueError("Invalid user")
            except jwt.ExpiredSignatureError:
                logger.warning("Token has expired")
                response = jsonify({'message': 'Token has expired!', 'error': 'Unauthorized'})
                response.status_code = 401
                return response
            except jwt.InvalidTokenError:
                logger.warning("Invalid token")
                response = jsonify({'message': 'Invalid token!', 'error': 'Unauthorized'})
                response.status_code = 401
                return response
            except Exception as e:
                logger.error(f"Error decoding token: {str(e)}")
                response = jsonify({'message': 'Token is invalid!', 'error': 'Unauthorized'})
                response.status_code = 401
                return response
            
            return f(current_user, *args, **kwargs)
        
        return decorated

    @user_bp.route('/register', methods=['POST'])
    def register():
        data = request.get_json()

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(username=data['username'], password=hashed_password, role=data['role'])

        db_session.add(new_user)
        db_session.commit()

        return jsonify({'message': 'New user created!'}), 201

    @user_bp.route('/login', methods=['POST'])
    def login():
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return jsonify({'message': 'Could not verify'}), 401

        user = db_session.query(User).filter_by(username=auth.username).first()

        if not user:
            return jsonify({'message': 'User not found!'}), 401

        if bcrypt.check_password_hash(user.password, auth.password):
            token = jwt.encode({
                'user_id': user.id,
                'username': user.username,
                'role': user.role.value,  # Include the role in the token
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'])

            return jsonify({'for-the-team-token': token})

        return jsonify({'message': 'Could not verify'}), 401

    @user_bp.route('/logout', methods=['POST'])
    @token_required
    def logout(current_user):
        # In a stateless JWT setup, we can't invalidate the token on the server side
        # Instead, we'll return a success message and it's up to the client to remove the token
        
        response = make_response(jsonify({'message': 'Successfully logged out'}), 200)
        
        # Optionally, you can set an expired cookie to help the client clear the token
        response.set_cookie('token', '', expires=0)
        
        return response

    @user_bp.route('/protected', methods=['GET'])
    @token_required
    def protected(current_user):
        return jsonify({'message': f'Hello {current_user.username}! This is a protected route.'})

    return user_bp, token_required