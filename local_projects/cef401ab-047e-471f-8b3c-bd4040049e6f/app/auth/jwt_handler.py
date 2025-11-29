import jwt
import datetime
from typing import Dict, Any, Optional
from functools import wraps
from flask import request, jsonify

class JWTHandler:
    def __init__(self, secret_key: str, algorithm: str = "HS256", expiration_hours: int = 24):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration_hours = expiration_hours

    def create_token(self, payload: Dict[str, Any]) -> str:
        """Create a JWT token with given payload and expiration"""
        payload_copy = payload.copy()
        payload_copy["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=self.expiration_hours)
        payload_copy["iat"] = datetime.datetime.utcnow()
        return jwt.encode(payload_copy, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token, return payload if valid, None if invalid"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def get_user_id_from_token(self, token: str) -> Optional[int]:
        """Extract user_id from token payload"""
        payload = self.verify_token(token)
        return payload.get("user_id") if payload else None

    def require_auth(self, f):
        """Decorator to require valid JWT token for endpoint"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Authorization header missing or invalid"}), 401

            token = auth_header[7:]  # Remove "Bearer " prefix
            payload = self.verify_token(token)
            if not payload:
                return jsonify({"error": "Invalid or expired token"}), 401

            # Attach user info to request context
            request.user_id = payload.get("user_id")
            request.user_email = payload.get("email")
            return f(*args, **kwargs)
        return decorated_function