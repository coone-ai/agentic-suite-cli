from api.auth import login_request

class UserService:
    def __init__(self):
        self.token = None
        self.email = None
        self.projects = []
        self.project_names = []

    def login(self, email: str, password: str):
        response = login_request(email, password)
        if response.status_code == 200:
            data = response.json()['data']
            self.token = data['token']
            self.email = email
            self.projects = data.get('projects', [])
            self.project_names = data.get('projectNames', [])
            return True, None
        else:
            try:
                message = response.json().get('message', 'Login failed.')
            except Exception:
                message = 'Login failed.'
            return False, message
