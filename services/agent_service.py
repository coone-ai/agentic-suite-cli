from api.agent import list_agents, create_agent, list_sessions, create_session, upload_file

class AgentService:
    def __init__(self, token):
        self.token = token
        self.agents = []
        self.selected_agent = None
        self.sessions = []

    def fetch_agents(self):
        response = list_agents(self.token)
        if response.status_code == 200:
            self.agents = response.json().get('data', [])
            return self.agents
        else:
            return []

    def add_agent(self, agent_name):
        response = create_agent(self.token, agent_name)
        if response.status_code == 201:
            return True, response.json().get('data')
        else:
            try:
                message = response.json().get('message', 'Agent creation failed.')
            except Exception:
                message = 'Agent creation failed.'
            return False, message

    def fetch_sessions(self, agent_id):
        response = list_sessions(self.token, agent_id)
        if response.status_code == 200:
            self.sessions = response.json().get('data', [])
            return self.sessions
        else:
            return []

    def create_session(self, agent_id, task_id):
        response = create_session(self.token, agent_id, task_id)
        if response.status_code == 201:
            return True, response.json().get('data')
        else:
            try:
                message = response.json().get('message', 'Session creation failed.')
            except Exception:
                message = 'Session creation failed.'
            return False, message

    def upload_file_to_session(self, agent_id, session_id, file_path):
        response = upload_file(self.token, agent_id, session_id, file_path)
        if response.status_code == 200:
            return True, response.json().get('data')
        else:
            try:
                message = response.json().get('message', 'File upload failed.')
            except Exception:
                message = 'File upload failed.'
            return False, message 