# backend/api/routes.py
from flask import Blueprint, request, jsonify, current_app
from functools import wraps
import uuid
import threading
from agent.researcher import run_research_agent
from agent.history import save_research_query, get_user_history, clear_user_history
from .websocket import register_task, progress_callback_factory
from config import AVAILABLE_MODELS, DEFAULT_MODEL

api_bp = Blueprint('api', __name__)

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        incoming_key = request.headers.get('X-Api-Key')
        valid_key = current_app.config.get('API_KEY')
        
        if not valid_key:
            current_app.logger.error("API_KEY not configured in application")
            return jsonify({"error": "Server configuration error"}), 500
            
        if incoming_key != valid_key:
            current_app.logger.warning(f"Invalid API key received: {incoming_key}")
            return jsonify({"error": "Unauthorized"}), 401
            
        current_app.logger.debug("API key validation successful")
        return f(*args, **kwargs)
    return decorated_function

@api_bp.route('/models', methods=['GET'])
@require_api_key
def get_models():
    """Get available LLM models"""
    try:
        return jsonify({
            "models": list(AVAILABLE_MODELS.keys()),
            "default": DEFAULT_MODEL
        })
    except Exception as e:
        current_app.logger.error(f"Error getting models: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@api_bp.route('/research', methods=['POST'])
@require_api_key
def research():
    """Endpoint to start a research task"""
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' field in request"}), 400
    
    query = data['query']
    model = data.get('model', DEFAULT_MODEL)
    
    if model not in AVAILABLE_MODELS:
        return jsonify({"error": f"Invalid model. Available models: {', '.join(AVAILABLE_MODELS.keys())}"}), 400
    
    user_id = request.headers.get('X-User-ID') or str(uuid.uuid4())
    task_id = register_task(user_id, query)
    progress_callback = progress_callback_factory(task_id)
    
    def run_research_task():
        try:
            result = run_research_agent(query, model=model, progress_callback=progress_callback)
            save_research_query(user_id, query, result)
        except Exception as e:
            current_app.logger.error(f"Research task failed: {str(e)}")
    
    thread = threading.Thread(target=run_research_task)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        "task_id": task_id,
        "query": query,
        "model": model,
        "user_id": user_id,
        "status": "started"
    })

@api_bp.route('/history', methods=['GET'])
@require_api_key
def get_history():
    """Get research history for a user"""
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return jsonify({"error": "Missing X-User-ID header"}), 400
    
    try:
        history = get_user_history(user_id)
        return jsonify({"history": history})
    except Exception as e:
        current_app.logger.error(f"Error getting history: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@api_bp.route('/history', methods=['DELETE'])
@require_api_key
def clear_history():
    """Clear research history for a user"""
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return jsonify({"error": "Missing X-User-ID header"}), 400
    
    try:
        success = clear_user_history(user_id)
        return jsonify({"success": success})
    except Exception as e:
        current_app.logger.error(f"Error clearing history: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})
