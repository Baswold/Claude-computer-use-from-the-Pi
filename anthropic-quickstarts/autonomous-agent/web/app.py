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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Autonomous Agent — Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --bg-primary: #0a0f1e;
            --bg-secondary: #111827;
            --bg-card: #1a1f35;
            --border-color: #2d3548;
            --text-primary: #ffffff;
            --text-secondary: #94a3b8;
            --text-tertiary: #64748b;
            --accent-primary: #3b82f6;
            --accent-success: #10b981;
            --accent-warning: #f59e0b;
            --accent-error: #ef4444;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        @keyframes slideIn {
            from { transform: translateX(-10px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        .header {
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            padding: 1.5rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
        }

        .header-content {
            max-width: 1600px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .logo-icon {
            font-size: 2rem;
            animation: pulse 3s ease-in-out infinite;
        }

        .logo-text h1 {
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-success));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }

        .logo-text p {
            color: var(--text-secondary);
            font-size: 0.85rem;
            margin-top: 0.125rem;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 2rem;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .card {
            background: var(--bg-card);
            border-radius: 12px;
            border: 1px solid var(--border-color);
            padding: 1.5rem;
            box-shadow: var(--shadow);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: fadeIn 0.5s ease-out;
        }

        .card:hover {
            border-color: var(--accent-primary);
            transform: translateY(-2px);
            box-shadow: 0 8px 12px -2px rgba(59, 130, 246, 0.2), 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }

        .card-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.25rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
        }

        .card-icon {
            font-size: 1.5rem;
        }

        .card h2 {
            font-size: 1.125rem;
            font-weight: 600;
            letter-spacing: -0.01em;
        }

        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.375rem 0.875rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 600;
            transition: all 0.2s;
        }

        .status-running {
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-success);
            border: 1px solid var(--accent-success);
        }

        .status-stopped {
            background: rgba(239, 68, 68, 0.15);
            color: var(--accent-error);
            border: 1px solid var(--accent-error);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            animation: pulse 2s ease-in-out infinite;
        }

        .status-running .status-dot {
            background: var(--accent-success);
            box-shadow: 0 0 8px var(--accent-success);
        }

        .status-stopped .status-dot {
            background: var(--accent-error);
        }

        .stat {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--border-color);
            transition: background 0.2s;
        }

        .stat:last-child {
            border-bottom: none;
        }

        .stat:hover {
            background: rgba(59, 130, 246, 0.05);
            padding-left: 0.5rem;
            margin-left: -0.5rem;
            border-radius: 6px;
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.9375rem;
        }

        .stat-value {
            color: var(--accent-primary);
            font-weight: 600;
            font-size: 0.9375rem;
        }

        .log-container {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            height: 500px;
            overflow-y: auto;
            font-family: 'SF Mono', 'Monaco', 'Consolas', 'Courier New', monospace;
            font-size: 0.875rem;
            scroll-behavior: smooth;
        }

        .log-container::-webkit-scrollbar {
            width: 8px;
        }

        .log-container::-webkit-scrollbar-track {
            background: var(--bg-primary);
            border-radius: 4px;
        }

        .log-container::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 4px;
        }

        .log-container::-webkit-scrollbar-thumb:hover {
            background: var(--accent-primary);
        }

        .log-entry {
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            border-left: 3px solid var(--border-color);
            padding-left: 1rem;
            border-radius: 0 4px 4px 0;
            transition: all 0.2s;
            animation: slideIn 0.3s ease-out;
        }

        .log-entry:hover {
            background: rgba(59, 130, 246, 0.05);
        }

        .log-user { border-left-color: var(--accent-primary); }
        .log-assistant { border-left-color: var(--accent-success); }
        .log-system { border-left-color: var(--accent-warning); }

        .log-time {
            color: var(--text-tertiary);
            font-size: 0.8125rem;
            margin-right: 0.625rem;
        }

        .log-role {
            color: var(--text-secondary);
            font-weight: 600;
            margin-right: 0.5rem;
        }

        .project-item {
            background: var(--bg-secondary);
            padding: 1rem;
            margin-bottom: 0.75rem;
            border-radius: 8px;
            border-left: 3px solid var(--accent-primary);
            transition: all 0.2s;
            animation: fadeIn 0.5s ease-out;
        }

        .project-item:hover {
            background: rgba(59, 130, 246, 0.05);
            transform: translateX(4px);
        }

        .project-name {
            font-weight: 600;
            margin-bottom: 0.375rem;
            color: var(--text-primary);
        }

        .project-desc {
            color: var(--text-secondary);
            font-size: 0.875rem;
            line-height: 1.5;
        }

        .empty-state {
            text-align: center;
            padding: 2rem;
            color: var(--text-tertiary);
            font-size: 0.9375rem;
        }

        .connection-status {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.375rem 0.75rem;
            background: rgba(59, 130, 246, 0.1);
            border-radius: 20px;
            font-size: 0.8125rem;
            color: var(--text-secondary);
        }

        .connection-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--accent-success);
            animation: pulse 2s ease-in-out infinite;
        }

        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }

            .grid {
                grid-template-columns: 1fr;
            }

            .header-content {
                flex-direction: column;
                gap: 1rem;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo">
                <div class="logo-icon">🤖</div>
                <div class="logo-text">
                    <h1>Claude Autonomous Agent</h1>
                    <p>Real-time Monitoring Dashboard</p>
                </div>
            </div>
            <div class="connection-status">
                <div class="connection-dot"></div>
                <span>Live</span>
            </div>
        </div>
    </header>

    <div class="container">

        <div class="grid">
            <div class="card">
                <div class="card-header">
                    <span class="card-icon">⚡️</span>
                    <h2>Agent Status</h2>
                </div>
                <div id="status-info">
                    <div class="stat">
                        <span class="stat-label">Status</span>
                        <span id="agent-status" class="status-indicator status-stopped">
                            <span class="status-dot"></span>
                            Loading...
                        </span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Last Check-in</span>
                        <span class="stat-value" id="last-checkin">—</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Total Check-ins</span>
                        <span class="stat-value" id="total-checkins">0</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Current Task</span>
                        <span class="stat-value" id="current-task">None</span>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <span class="card-icon">📁</span>
                    <h2>Active Projects</h2>
                </div>
                <div id="projects-list">
                    <div class="empty-state">Loading projects...</div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <span class="card-icon">📜</span>
                <h2>Activity Stream</h2>
            </div>
            <div class="log-container" id="log-container">
                <div class="empty-state">Connecting to live feed...</div>
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
            const statusText = status.running ? 'Running' : 'Stopped';
            const statusClass = status.running ? 'status-running' : 'status-stopped';

            badge.className = `status-indicator ${statusClass}`;
            badge.innerHTML = `
                <span class="status-dot"></span>
                ${statusText}
            `;

            const lastCheckin = status.last_checkin
                ? new Date(status.last_checkin).toLocaleString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    hour: 'numeric',
                    minute: '2-digit'
                  })
                : '—';

            document.getElementById('last-checkin').textContent = lastCheckin;
            document.getElementById('total-checkins').textContent = status.total_checkins || 0;
            document.getElementById('current-task').textContent = status.current_task || 'None';
        }

        function updateProjects(projects) {
            const container = document.getElementById('projects-list');
            if (projects.length === 0) {
                container.innerHTML = '<div class="empty-state">No active projects</div>';
                return;
            }

            container.innerHTML = projects.map(p => `
                <div class="project-item">
                    <div class="project-name">${escapeHtml(p.name)}</div>
                    <div class="project-desc">${escapeHtml(p.description || '')}</div>
                </div>
            `).join('');
        }

        function addLogEntry(role, content, timestamp) {
            const container = document.getElementById('log-container');

            // Remove empty state if it exists
            const emptyState = container.querySelector('.empty-state');
            if (emptyState) {
                emptyState.remove();
            }

            const entry = document.createElement('div');
            entry.className = `log-entry log-${role}`;

            const time = timestamp
                ? new Date(timestamp).toLocaleTimeString('en-US', {
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                  })
                : new Date().toLocaleTimeString('en-US', {
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                  });

            entry.innerHTML = `
                <span class="log-time">${time}</span>
                <span class="log-role">${role}</span>
                ${escapeHtml(content)}
            `;

            container.appendChild(entry);

            // Smooth scroll to bottom
            container.scrollTop = container.scrollHeight;

            // Limit log entries to prevent memory issues
            const entries = container.querySelectorAll('.log-entry');
            if (entries.length > 100) {
                entries[0].remove();
            }
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
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
