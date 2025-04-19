from flask import Flask, request
from flask_cors import CORS
import secrets
import logging
from api.routes import api_bp
from api.websocket import init_socketio
from config import DEBUG, PORT, HOST, API_KEY


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)


def create_app():
    app = Flask(__name__)
    app.logger.info("Initializing application...")

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if DEBUG else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    app.logger = logging.getLogger(__name__)
    
    # Security headers and CORS
    CORS(app, supports_credentials=True, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "X-API-Key", "X-User-ID"]
        }
    })
    
    # Secret key for session management
    app.secret_key = secrets.token_hex(32)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['API_KEY'] = API_KEY
    
    # Request logging middleware
    @app.before_request
    def log_request_info():
        if request.path != '/health':
            app.logger.info(f"Request: {request.method} {request.path} | Headers: {dict(request.headers)}")
    
    @app.after_request
    def log_response_info(response):
        if request.path != '/health':
            app.logger.info(f"Response: {response.status} {request.path}")
        return response
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Initialize SocketIO
    socketio = init_socketio(app)
    
    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    
    # Production considerations
    if not DEBUG:
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
    
    socketio.run(
        app,
        debug=DEBUG,
        host=HOST,
        port=PORT,
        allow_unsafe_werkzeug=True if DEBUG else False
    )
