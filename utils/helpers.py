# Helper functions for AI Agent project

def print_sessions(sessions):
    for idx, session in enumerate(sessions):
        session_id = session.get('sessionID') or session.get('id')
        session_name = session.get('session_name', 'NoName')
        task_title = (
            session.get('state_holder', {})
                   .get('current_task', {})
                   .get('value', {})
                   .get('taskTitle', 'NoTask')
        )
        print(f"{idx+1}) {session_name} | Task: {task_title}")
