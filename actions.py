
from datetime import datetime
import uuid


def create_response_task(incident, location, risk_level, actions):

    priority_mapping = {
        "CRITICAL": "P1 - IMMEDIATE",
        "HIGH": "P2 - URGENT",
        "MEDIUM": "P3 - MODERATE",
        "LOW": "P4 - NORMAL"
    }

    team_mapping = {
        "CRITICAL": "Emergency Rapid Response Team",
        "HIGH": "Rapid Response Team",
        "MEDIUM": "Field Assessment Team",
        "LOW": "Local Monitoring Team"
    }

    response_guidance = {
        "CRITICAL": "Immediate emergency assessment",
        "HIGH": "Urgent assessment required",
        "MEDIUM": "Prompt field assessment",
        "LOW": "Routine monitoring"
    }

    task_id = "ECHO-" + uuid.uuid4().hex[:8].upper()
    now = datetime.now()

    task = {
        "task_id": task_id,
        "incident": incident,
        "location": location,
        "risk_level": risk_level,

        "priority": priority_mapping.get(
            risk_level, "P4 - NORMAL"
        ),

        "recommended_team": team_mapping.get(
            risk_level, "Emergency Assessment Team"
        ),

        "response_time": response_guidance.get(
            risk_level, "Assessment required"
        ),

        "actions": actions.copy(),

        "action_progress": {
            action: False for action in actions
        },

        "created_at": now.strftime("%d-%m-%Y %H:%M:%S"),
        "created_timestamp": now.isoformat(),

        "status": "OPEN",
        "completed_at": None
    }

    return task


def update_task_status(task, status):

    allowed_status = [
        "OPEN",
        "IN PROGRESS",
        "COMPLETED"
    ]

    if status not in allowed_status:
        return {"error": "Invalid task status"}

    task["status"] = status

    if status == "COMPLETED":
        task["completed_at"] = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )
    else:
        task["completed_at"] = None

    return task


def update_action_progress(task, action, completed):

    if "action_progress" not in task:
        task["action_progress"] = {
            item: False for item in task["actions"]
        }

    if action in task["action_progress"]:

        task["action_progress"][action] = completed

        total_actions = len(task["action_progress"])

        completed_actions = sum(
            task["action_progress"].values()
        )

        if total_actions > 0 and completed_actions == total_actions:

            task["status"] = "COMPLETED"
            task["completed_at"] = datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

        elif completed_actions > 0:

            task["status"] = "IN PROGRESS"
            task["completed_at"] = None

        else:

            task["status"] = "OPEN"
            task["completed_at"] = None

    return task


def get_task_progress(task):

    action_progress = task.get("action_progress", {})

    total = len(action_progress)

    completed = sum(action_progress.values())

    percentage = (
        int((completed / total) * 100)
        if total > 0 else 0
    )

    return {
        "total_actions": total,
        "completed_actions": completed,
        "percentage": percentage
    }
