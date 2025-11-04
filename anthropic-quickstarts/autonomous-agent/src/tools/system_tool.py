"""System monitoring tools for the autonomous agent"""

import logging
import psutil
from datetime import datetime
from typing import Any, Dict
from claude_agent_sdk import tool

logger = logging.getLogger(__name__)


@tool(
    name="check_system_health",
    description="Check the system health including CPU, memory, disk usage",
    input_schema={"type": "object", "properties": {}},
)
async def check_system_health(args: Dict[str, Any]) -> Dict[str, Any]:
    """Check system resource usage"""
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()

        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_available_gb = memory.available / (1024 ** 3)
        memory_total_gb = memory.total / (1024 ** 3)

        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_free_gb = disk.free / (1024 ** 3)
        disk_total_gb = disk.total / (1024 ** 3)

        # Uptime
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time

        health_status = "🟢 HEALTHY"
        warnings = []

        if cpu_percent > 80:
            health_status = "🟡 WARNING"
            warnings.append(f"High CPU usage: {cpu_percent}%")

        if memory_percent > 85:
            health_status = "🟡 WARNING"
            warnings.append(f"High memory usage: {memory_percent}%")

        if disk_percent > 90:
            health_status = "🔴 CRITICAL"
            warnings.append(f"Low disk space: {disk_percent}% used")

        result = f"""System Health Report - {health_status}

CPU:
  Usage: {cpu_percent}%
  Cores: {cpu_count}

Memory:
  Usage: {memory_percent}%
  Available: {memory_available_gb:.2f} GB / {memory_total_gb:.2f} GB

Disk:
  Usage: {disk_percent}%
  Free: {disk_free_gb:.2f} GB / {disk_total_gb:.2f} GB

Uptime: {uptime.days} days, {uptime.seconds // 3600} hours
"""

        if warnings:
            result += "\n⚠️ WARNINGS:\n" + "\n".join(f"  - {w}" for w in warnings)

        return {
            "content": [
                {
                    "type": "text",
                    "text": result,
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error checking system health: {e}", exc_info=True)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error checking system health: {str(e)}",
                }
            ]
        }


@tool(
    name="list_processes",
    description="List running processes, optionally filtered by name",
    input_schema={
        "type": "object",
        "properties": {
            "filter": {
                "type": "string",
                "description": "Filter processes by name (optional)",
            },
            "sort_by": {
                "type": "string",
                "enum": ["cpu", "memory", "name"],
                "description": "Sort by CPU, memory, or name",
                "default": "cpu",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of processes to return",
                "default": 10,
            },
        },
    },
)
async def list_processes(args: Dict[str, Any]) -> Dict[str, Any]:
    """List running processes"""
    try:
        filter_name = args.get("filter", "").lower()
        sort_by = args.get("sort_by", "cpu")
        limit = args.get("limit", 10)

        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                pinfo = proc.info
                if filter_name and filter_name not in pinfo['name'].lower():
                    continue
                processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Sort processes
        if sort_by == "cpu":
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
        elif sort_by == "memory":
            processes.sort(key=lambda x: x.get('memory_percent', 0), reverse=True)
        else:
            processes.sort(key=lambda x: x.get('name', ''))

        processes = processes[:limit]

        result = f"Top {len(processes)} Processes (sorted by {sort_by}):\n\n"
        result += f"{'PID':<8} {'Name':<30} {'CPU%':<8} {'MEM%':<8}\n"
        result += "-" * 60 + "\n"

        for proc in processes:
            result += f"{proc['pid']:<8} {proc['name'][:29]:<30} {proc.get('cpu_percent', 0):<8.1f} {proc.get('memory_percent', 0):<8.1f}\n"

        return {
            "content": [
                {
                    "type": "text",
                    "text": result,
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error listing processes: {e}", exc_info=True)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error listing processes: {str(e)}",
                }
            ]
        }
