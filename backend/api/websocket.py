# backend/api/websocket.py
from flask_socketio import SocketIO
from flask import request
import threading
import uuid
from typing import Dict, Any

# Create SocketIO instance
socketio = SocketIO(cors_allowed_origins="*")

# Dictionary to hold active research tasks
active_tasks = {}

def get_task_id(user_id: str, query: str) -> str:
    """Generate a unique task ID for a research query"""
    return f"{user_id}_{uuid.uuid4()}"

def register_task(user_id: str, query: str) -> str:
    """Register a new research task and return its ID"""
    task_id = get_task_id(user_id, query)
    active_tasks[task_id] = {
        "user_id": user_id,
        "query": query,
        "status": "starting",
        "progress": 0
    }
    return task_id

def progress_callback_factory(task_id: str):
    """Create a progress callback function for a specific task"""
    def progress_callback(progress_data: Dict[str, Any]):
        # Update task state
        if task_id in active_tasks:
            active_tasks[task_id].update({
                "status": progress_data.get("step", "unknown"),
                "message": progress_data.get("message", ""),
                "progress": progress_data.get("percent", 0)
            })
            
            # Emit progress update via socket
            socketio.emit(
                'research_progress', 
                {
                    "task_id": task_id,
                    "status": progress_data.get("step", "unknown"),
                    "message": progress_data.get("message", ""),
                    "progress": progress_data.get("percent", 0)
                },
                room=task_id
            )
    
    return progress_callback

def init_socketio(app):
    """Initialize SocketIO with Flask app"""
    socketio.init_app(app)
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        print(f"Client connected: {request.sid}")
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        print(f"Client disconnected: {request.sid}")
    
    @socketio.on('join_task')
    def handle_join_task(data):
        """Join a task room to receive updates for a specific research task"""
        task_id = data.get('task_id')
        if task_id:
            socketio.server.enter_room(request.sid, task_id)
            print(f"Client {request.sid} joined room {task_id}")
            
            # Send initial status if task exists
            if task_id in active_tasks:
                task_data = active_tasks[task_id]
                socketio.emit(
                    'research_progress', 
                    {
                        "task_id": task_id,
                        "status": task_data.get("status", "unknown"),
                        "message": task_data.get("message", ""),
                        "progress": task_data.get("progress", 0)
                    },
                    room=request.sid
                )
    
    return socketio
