from flask import jsonify


def register_error_handlers(jwt):
    # missing authorization headers
    @jwt.unauthorized_loader
    def unauthorized_response(callback):
        return jsonify({
            "error": "Authorization required",
            "message": "Missing or invalid token"
        }), 401

    # expired tokens
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "Token expired",
            "message": "Please log in again"
        }), 401

    # invalid tokens
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "error": "Invalid token",
            "message": "Token is malformed or invalid"
        }), 422

    # revoked tokens
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "Token revoked",
            "message": "This token is no longer valid"
        }), 401