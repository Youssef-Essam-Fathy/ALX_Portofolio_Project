"""
Public Blueprint Routes

This module defines the Flask blueprint for handling routes accessible to the public.
It provides routes to display the home page.

Routes:
    - / (GET): Renders the home page.
    - /home (GET): Renders the home page.

Dependencies:
    - app: The Flask application instance.
    - Blueprint: Flask's blueprint class for grouping related routes.
"""
from flask import Blueprint, render_template

bp = Blueprint('public', __name__)


@bp.route('/home', strict_slashes=False)
@bp.route('/', strict_slashes=False)
def public():
    """
    Public endpoint that renders the home page.

    This route is accessible to all users.

    Returns:
        HTML template for the home page.
    """
    return render_template('home.html')
