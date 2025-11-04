"""Web dashboard for monitoring the autonomous agent"""

import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# Import managers
import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))

from session_manager import SessionManager
from project_manager import ProjectManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Claude Autonomous Agent Dashboard")

# Initialize managers
session_manager = SessionManager()
project_manager = ProjectManager()

# WebSocket connections
active_connections: List[WebSocket] = []


class ConnectionManager:
    """Manages WebSocket connections"""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(
            f"WebSocket disconnected. Total: {len(self.active_connections)}"
        )

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error sending to WebSocket: {e}")


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the main dashboard HTML"""
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Claude Autonomous Agent Dashboard</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #0f172a;
            color: #e2e8f0;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        h1 {
            color: #f97316;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #94a3b8;
            margin-bottom: 30px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: #1e293b;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #334155;
        }
        .card h2 {
            margin-top: 0;
            color: #f97316;
            font-size: 1.2em;
        }
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .status-running {
            background: #10b981;
            color: #fff;
        }
        .status-stopped {
            background: #ef4444;
            color: #fff;
        }
        .log-container {
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 15px;
            height: 400px;
            overflow-y: auto;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
        }
        .log-entry {
            margin-bottom: 10px;
            padding: 8px;
            border-left: 3px solid #334155;
            padding-left: 12px;
        }
        .log-user { border-left-color: #3b82f6; }
        .log-assistant { border-left-color: #10b981; }
        .log-system { border-left-color: #f97316; }
        .log-time {
            color: #64748b;
            font-size: 0.85em;
            margin-right: 8px;
        }
        .stat {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding: 8px 0;
            border-bottom: 1px solid #334155;
        }
        .stat-label {
            color: #94a3b8;
        }
        .stat-value {
            color: #f97316;
            font-weight: 600;
        }
        .project-item {
            background: #0f172a;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 4px;
            border-left: 3px solid #f97316;
        }
        .project-name {
            font-weight: 600;
            margin-bottom: 5px;
        }
        .project-desc {
            color: #94a3b8;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Claude Autonomous Agent</h1>
        <p class="subtitle">Real-time monitoring dashboard</p>

        <div class="grid">
            <div class="card">
                <h2>Agent Status</h2>
                <div id="status-info">
                    <div class="stat">
                        <span class="stat-label">Status:</span>
                        <span id="agent-status" class="status-badge status-stopped">Loading...</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Last Check-in:</span>
                        <span class="stat-value" id="last-checkin">-</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Total Check-ins:</span>
                        <span class="stat-value" id="total-checkins">0</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Current Task:</span>
                        <span class="stat-value" id="current-task">None</span>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2>Projects</h2>
                <div id="projects-list">
                    <p style="color: #64748b;">Loading projects...</p>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Activity Log</h2>
            <div class="log-container" id="log-container">
                <p style="color: #64748b;">Connecting to live feed...</p>
            </div>
        </div>
    </div>

    <script>
        // WebSocket connection for live updates
        const ws = new WebSocket(`ws://${window.location.host}/ws`);

        ws.onopen = () => {
            console.log('WebSocket connected');
            addLogEntry('system', 'Connected to agent monitoring');
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleUpdate(data);
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            addLogEntry('system', 'Connection error');
        };

        ws.onclose = () => {
            console.log('WebSocket disconnected');
            addLogEntry('system', 'Disconnected from agent');
        };

        function handleUpdate(data) {
            if (data.type === 'status') {
                updateStatus(data.status);
            } else if (data.type === 'message') {
                addLogEntry(data.role, data.content, data.timestamp);
            } else if (data.type === 'projects') {
                updateProjects(data.projects);
            }
        }

        function updateStatus(status) {
            const badge = document.getElementById('agent-status');
            badge.textContent = status.running ? 'Running' : 'Stopped';
            badge.className = 'status-badge ' + (status.running ? 'status-running' : 'status-stopped');

            document.getElementById('last-checkin').textContent =
                status.last_checkin ? new Date(status.last_checkin).toLocaleString() : '-';
            document.getElementById('total-checkins').textContent = status.total_checkins;
            document.getElementById('current-task').textContent = status.current_task || 'None';
        }

        function updateProjects(projects) {
            const container = document.getElementById('projects-list');
            if (projects.length === 0) {
                container.innerHTML = '<p style="color: #64748b;">No active projects</p>';
                return;
            }

            container.innerHTML = projects.map(p => `
                <div class="project-item">
                    <div class="project-name">${p.name}</div>
                    <div class="project-desc">${p.description}</div>
                </div>
            `).join('');
        }

        function addLogEntry(role, content, timestamp) {
            const container = document.getElementById('log-container');
            const entry = document.createElement('div');
            entry.className = `log-entry log-${role}`;

            const time = timestamp ? new Date(timestamp).toLocaleTimeString() : new Date().toLocaleTimeString();
            entry.innerHTML = `
                <span class="log-time">[${time}]</span>
                <strong>${role}:</strong> ${content}
            `;

            container.appendChild(entry);
            container.scrollTop = container.scrollHeight;
        }

        // Poll for updates every 5 seconds
        async function pollUpdates() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                updateStatus(data);

                const projectsResponse = await fetch('/api/projects');
                const projects = await projectsResponse.json();
                updateProjects(projects);
            } catch (error) {
                console.error('Error polling updates:', error);
            }
        }

        // Initial load
        pollUpdates();
        setInterval(pollUpdates, 5000);
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)

    try:
        # Send initial status
        status = session_manager.get_status()
        await websocket.send_json({"type": "status", "status": status})

        # Send recent messages
        for msg in session_manager.get_recent_messages(20):
            await websocket.send_json(
                {
                    "type": "message",
                    "role": msg["role"],
                    "content": msg["content"],
                    "timestamp": msg["timestamp"],
                }
            )

        # Keep connection alive
        while True:
            data = await websocket.receive_text()
            # Echo back for now
            await websocket.send_json({"type": "echo", "data": data})

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/api/status")
async def get_status():
    """Get current agent status"""
    return session_manager.get_status()


@app.get("/api/projects")
async def get_projects():
    """Get active projects"""
    return project_manager.get_active_projects()


@app.get("/api/messages")
async def get_messages(limit: int = 50):
    """Get recent messages"""
    return session_manager.get_recent_messages(limit)


def start_dashboard(host: str = "0.0.0.0", port: int = 8080):
    """Start the web dashboard"""
    logger.info(f"Starting dashboard on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_dashboard()
