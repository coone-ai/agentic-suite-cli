import requests
from config import API_BASE_URL

def list_agents(token):
    url = f"{API_BASE_URL}/agent/list"
    headers = {'Authorization': token}
    return requests.get(url, headers=headers)

def create_agent(token, agent_name):
    url = f"{API_BASE_URL}/agent/create"
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    data = {"agent_name": agent_name}
    return requests.post(url, headers=headers, json=data)

def list_sessions(token, agent_id):
    url = f"{API_BASE_URL}/agent/{agent_id}/sessions"
    headers = {'Authorization': token}
    return requests.get(url, headers=headers)

def create_session(token, agent_id, task_id):
    url = f"{API_BASE_URL}/agent/{agent_id}/session"
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    data = {"task_id": task_id}
    return requests.post(url, headers=headers, json=data)

def upload_file(token, agent_id, session_id, file_path):
    url = f"{API_BASE_URL}/agent/{agent_id}/sessions/{session_id}/files"
    headers = {'Authorization': token}
    
    with open(file_path, 'rb') as file:
        files = {'file': (file.name, file, 'application/octet-stream')}
        return requests.post(url, headers=headers, files=files) 