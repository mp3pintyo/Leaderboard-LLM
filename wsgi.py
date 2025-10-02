"""
WSGI entry point for production deployment.
Use with gunicorn, waitress, or other WSGI servers.

Example usage:
    gunicorn --bind 0.0.0.0:5000 wsgi:app
    waitress-serve --port=5000 wsgi:app
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
