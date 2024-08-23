from flask import jsonify


def setup_jwt_error_handlers(jwt):
    """
    Set up custom JWT error handlers for the application.

    This function defines custom responses for various JWT-related errors,
    ensuring that the client receives a consistent and informative message
    when a JWT-related issue occurs.

    Error Handlers:
    ---------------
    - Missing Authorization Header: Returns a 401 status with an 'error' message.
    - Invalid Token: Returns a 422 status with an 'error' message.
    - Expired Token: Returns a 401 status with an 'error' message.
    - Revoked Token: Returns a 401 status with an 'error' message.

    Parameters:
    -----------
    jwt : JWTManager
        The JWTManager instance to which the error handlers will be applied.

    Returns:
    --------
    None
    """

    @jwt.unauthorized_loader
    def custom_unauthorized_response(callback):
        """
        Custom response for missing Authorization Header.

        Parameters:
        -----------
        callback : function
            The function that triggered the unauthorized loader.

        Returns:
        --------
        response : Response
            JSON response with an error message and 401 status code.
        """
        return jsonify({'error': 'Missing Authorization Header'}), 401

    @jwt.invalid_token_loader
    def custom_invalid_token_response(callback):
        """
        Custom response for an invalid JWT token.

        Parameters:
        -----------
        callback : function
            The function that triggered the invalid token loader.

        Returns:
        --------
        response : Response
            JSON response with an error message and 422 status code.
        """
        return jsonify({'error': 'Invalid token'}), 422

    @jwt.expired_token_loader
    def custom_expired_token_response(callback):
        """
        Custom response for an expired JWT token.

        Parameters:
        -----------
        callback : function
            The function that triggered the expired token loader.

        Returns:
        --------
        response : Response
            JSON response with an error message and 401 status code.
        """
        return jsonify({'error': 'Token has expired'}), 401

    @jwt.revoked_token_loader
    def custom_revoked_token_response(callback):
        """
        Custom response for a revoked JWT token.

        Parameters:
        -----------
        callback : function
            The function that triggered the revoked token loader.

        Returns:
        --------
        response : Response
            JSON response with an error message and 401 status code.
        """
        return jsonify({'error': 'Token has been revoked'}), 401


    @jwt.expired_token_loader
    def custom_expired_token_response(jwt_header, jwt_payload):
        return jsonify({'message': 'The token has expired, please log in again.'}), 401
