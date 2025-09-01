from services.user_service import UserService
from services.agent_service import AgentService
import getpass
from utils.helpers import print_sessions
import sys
import os

def get_agent_name(agent):
    return (
        agent.get('name') or
        agent.get('agent_name') or
        (agent.get('agent_config', {}).get('agent_name')) or
        'No Agent Name'
    )

def quick_upload(user_service, agent_service, agent_name, session_id, file_path):
    """Quick upload mode - directly upload file to specified agent and session"""
    print(f"=== Quick Upload Mode ===")
    print(f"Agent: {agent_name}")
    print(f"Session ID: {session_id}")
    print(f"File: {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print("Error: File does not exist.")
        return False
    
    # Check file extension
    allowed_extensions = ['.csv', '.json', '.xlsx', '.xls']
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext not in allowed_extensions:
        print(f"Error: Unsupported file format. Please use: {', '.join(allowed_extensions)}")
        return False
    
    # Find agent by name
    agents = agent_service.fetch_agents()
    target_agent = None
    for agent in agents:
        if get_agent_name(agent) == agent_name:
            target_agent = agent
            break
    
    if not target_agent:
        print(f"Error: Agent '{agent_name}' not found.")
        return False
    
    agent_id = target_agent.get('id', target_agent.get('_id'))
    
    # Upload file
    print("Uploading file...")
    ok, result = agent_service.upload_file_to_session(agent_id, session_id, file_path)
    if ok:
        print("File uploaded successfully!")
        return True
    else:
        print(f"File upload failed: {result}")
        return False

def main():
    # Check for quick upload mode
    if len(sys.argv) >= 3:
        # Format: python main.py email password [file_path] [agent_name] [session_id]
        email = sys.argv[1]
        password = sys.argv[2]
        file_path = sys.argv[3] if len(sys.argv) > 3 else None
        agent_name = sys.argv[4] if len(sys.argv) > 4 else None
        session_id = sys.argv[5] if len(sys.argv) > 5 else None
        
        print("=== Quick Upload Mode ===")
        
        user_service = UserService()
        success, error = user_service.login(email, password)
        if not success:
            print(f"Login failed: {error}")
            return
        
        agent_service = AgentService(user_service.token)
        
        # If agent_name is not provided, show available agents
        if not agent_name:
            print("No agent specified. Available agents:")
            agents = agent_service.fetch_agents()
            if not agents:
                print("No agents found. Please create an agent first.")
                return
            
            for idx, agent in enumerate(agents):
                print(f"{idx+1}) {get_agent_name(agent)}")
            
            try:
                agent_idx = int(input("Select agent number: ")) - 1
                if 0 <= agent_idx < len(agents):
                    selected_agent = agents[agent_idx]
                    agent_name = get_agent_name(selected_agent)
                else:
                    print("Invalid agent number.")
                    return
            except ValueError:
                print("Please enter a valid number.")
                return
        
        # If session_id is not provided, show available sessions
        if not session_id:
            # Find agent by name
            agents = agent_service.fetch_agents()
            target_agent = None
            for agent in agents:
                if get_agent_name(agent) == agent_name:
                    target_agent = agent
                    break
            
            if not target_agent:
                print(f"Error: Agent '{agent_name}' not found.")
                return
            
            agent_id = target_agent.get('id', target_agent.get('_id'))
            sessions = agent_service.fetch_sessions(agent_id)
            
            if not sessions:
                print("No sessions found for this agent.")
                return
            
            print(f"\nSessions for {agent_name}:")
            from utils.helpers import print_sessions
            print_sessions(sessions)
            
            try:
                session_idx = int(input("Select session number: ")) - 1
                if 0 <= session_idx < len(sessions):
                    selected_session = sessions[session_idx]
                    session_id = selected_session.get('id', selected_session.get('sessionID'))
                else:
                    print("Invalid session number.")
                    return
            except ValueError:
                print("Please enter a valid number.")
                return
        
        # If file_path is not provided, ask for it
        if not file_path:
            print("No file specified. Please enter file path:")
            file_path = input("File path: ")
            
            if not os.path.exists(file_path):
                print("Error: File does not exist.")
                return
            
            # Check file extension
            allowed_extensions = ['.csv', '.json', '.xlsx', '.xls']
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in allowed_extensions:
                print(f"Error: Unsupported file format. Please use: {', '.join(allowed_extensions)}")
                return
        
        quick_upload(user_service, agent_service, agent_name, session_id, file_path)
        return
    
    # Normal interactive mode
    print("=== AI Agent Login ===")
    email = input("Email: ")
    password = getpass.getpass("Password: ")

    user_service = UserService()
    success, error = user_service.login(email, password)
    if not success:
        print(f"\nLogin failed: {error}")
        return
    print(f"\nLogin successful! Welcome, {user_service.email}")

    agent_service = AgentService(user_service.token)
    selected_agent = None
    selected_session = None

    while True:
        print("\n" + "="*50)
        print("=== AI Agent Menu ===")
        print("="*50)
        
        if selected_agent:
            print(f"Selected Agent: {get_agent_name(selected_agent)}")
        if selected_session:
            task_title = (
                selected_session.get('state_holder', {})
                    .get('current_task', {})
                    .get('value', {})
                    .get('taskTitle', 'NoTask')
            )
            print(f"Selected Session: {selected_session.get('session_name', 'Unknown')} - Task: {task_title}")
        
        print("\nOptions:")
        print("1) Select Agent")
        print("2) Create New Agent")
        print("3) Select Session")
        print("4) Create New Session")
        print("5) Upload File to Session")
        print("6) View Result (Session Output)")
        print("0) Exit")
        
        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 0:
            print("Goodbye!")
            break
        elif choice == 1:
            # Select Agent
            agents = agent_service.fetch_agents()
            if not agents:
                print("\nNo agents found. Please create an agent first.")
                continue
            
            print("\nYour Agents:")
            for idx, agent in enumerate(agents):
                print(f"{idx+1}) {get_agent_name(agent)}")
            
            try:
                agent_idx = int(input("Select agent number: ")) - 1
                if 0 <= agent_idx < len(agents):
                    selected_agent = agents[agent_idx]
                    selected_session = None  # Reset session when agent changes
                    print(f"Selected agent: {get_agent_name(selected_agent)}")
                else:
                    print("Invalid agent number.")
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == 2:
            # Create New Agent
            print("\nCreate New Agent:")
            agent_name = input("Enter agent name: ")
            ok, result = agent_service.add_agent(agent_name)
            if ok:
                print(f"Agent '{agent_name}' created successfully!")
                # Optionally select the newly created agent
                agents = agent_service.fetch_agents()
                for idx, agent in enumerate(agents):
                    if get_agent_name(agent) == agent_name:
                        selected_agent = agent
                        selected_session = None
                        print(f"Selected the newly created agent: {agent_name}")
                        break
            else:
                print(f"Agent creation failed: {result}")
        
        elif choice == 3:
            # Select Session
            if not selected_agent:
                print("Please select an agent first.")
                continue
            
            agent_id = selected_agent.get('id', selected_agent.get('_id'))
            sessions = agent_service.fetch_sessions(agent_id)
            if not sessions:
                print("No sessions found for this agent.")
                continue
            
            print(f"\nSessions for {get_agent_name(selected_agent)}:")
            print_sessions(sessions)
            
            try:
                session_idx = int(input("Select session number: ")) - 1
                if 0 <= session_idx < len(sessions):
                    selected_session = sessions[session_idx]
                    
                    task_title = (
                        selected_session.get('state_holder', {})
                            .get('current_task', {})
                            .get('value', {})
                            .get('taskTitle', 'NoTask')
                    )
                    print(f"Selected session: {selected_session.get('session_name', 'Unknown')} - Task: {task_title}")
                else:
                    print("Invalid session number.")
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == 4:
            # Create New Session
            if not selected_agent:
                print("Please select an agent first.")
                continue
            
            print("\nSelect a task to start a new session:")
            tasks = [
                (1, "Product Description Writer", "Generates structured and engaging product descriptions using customer-provided data. The AI processes product attributes, customer personas, and configuration settings to create personalized descriptions. It extracts relevant details from product links and any additional product information shared by the customer, ensuring the final output aligns with the defined personas, SEO best practices, and business requirements."),
                (2, "Product Title Writer", "Creates concise and keyword-rich product titles optimized for clarity, marketplace visibility, and SEO. The AI processes product specifications, customer preferences, and configuration settings to generate compelling titles that highlight key product features while maintaining relevance for search ranking and user engagement."),
                # (3, "Product Image Selection", "Selects the most suitable primary product image based on customer personas, engagement metrics, and visual appeal. The AI optimizes image selection for Google ranking results and persona preferences. It evaluates image quality, relevance, and marketing effectiveness while ensuring alignment with branding and sales strategies. Each selection is accompanied by reasoning and comments explaining the decision.")
            ]
            for tid, title, desc in tasks:
                print(f"{tid}) {title}\n   {desc}\n")
            
            valid_choices = [1, 2]
            while True:
                try:
                    task_id = int(input("Enter task number (1/2): "))
                    if task_id in valid_choices:
                        break
                    else:
                        print("Please enter 1 or 2.")
                except ValueError:
                    print("Please enter a valid number (1 or 2).")
            
            agent_id = selected_agent.get('id', selected_agent.get('_id'))
            ok, result = agent_service.create_session(agent_id, task_id + 60)
            if ok:
                print("Session created!")
            else:
                print(f"Session creation failed: {result}")
        
        elif choice == 5:
            # Upload File to Session
            if not selected_agent:
                print("Please select an agent first.")
                continue
            
            if not selected_session:
                print("Please select a session first.")
                continue
            
            print("\nUpload File to Session:")
            print("Supported formats: CSV, JSON, Excel (.xlsx, .xls)")
            file_path = input("Enter file path: ")
            
            if not os.path.exists(file_path):
                print("File does not exist. Please check the path.")
                continue
            
            # Check file extension
            allowed_extensions = ['.csv', '.json', '.xlsx', '.xls']
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in allowed_extensions:
                print(f"Unsupported file format. Please use: {', '.join(allowed_extensions)}")
                continue
            
            agent_id = selected_agent.get('id', selected_agent.get('_id'))
            session_id = selected_session.get('id', selected_session.get('sessionID'))
            
            print("Uploading file...")
            ok, result = agent_service.upload_file_to_session(agent_id, session_id, file_path)
            if ok:
                print("File uploaded successfully!")
            else:
                print(f"File upload failed: {result}")
        
        elif choice == 6:
            # View Result (Session Output)
            if not selected_agent:
                print("Please select an agent first.")
                continue
            import time
            agent_id = selected_agent.get('id', selected_agent.get('_id'))
            print(f"\nTracking output files for all sessions of agent: {get_agent_name(selected_agent)}")
            try:
                while True:
                    sessions = agent_service.fetch_sessions(agent_id)
                    if not sessions:
                        print("No sessions found for this agent.")
                        break
                    for session in sessions:
                        session_id = session.get('id', session.get('sessionID'))
                        session_name = session.get('session_name', session_id)
                        print(f"\nSession: {session_name} ({session_id})")
                        output = session.get('output', {})
                        all_files = []
                        for file_id, file_info in output.items():
                            all_files.append(file_info)

                        if all_files and 'created_at' in all_files[0]:
                            all_files.sort(key=lambda x: x.get('created_at', 0), reverse=True)
                        else:
                            all_files = list(reversed(all_files))
                        if not all_files:
                            print("  No output files found in this session.")
                            continue
                        print("  Output File Status:")
                        for file_info in all_files:
                            fname = file_info.get('file_name', file_info.get('file_id', 'Unknown'))
                            status = file_info.get('status', 'unknown')
                            progress = file_info.get('progress', 0)
                            url = file_info.get('file_url', '')
                            bar = ''
                            if isinstance(progress, (int, float)) and 0 <= progress <= 100:
                                bar = '[' + '#' * int(progress // 5) + '-' * (20 - int(progress // 5)) + f'] {progress}%'
                            else:
                                bar = '[--------------------]'
                            print(f"    - {fname}: {status} {bar}")
                            if url:
                                print(f"      URL: {url}")
                    print("\n(Updating every 20 seconds. Press Ctrl+C to exit.)")
                    time.sleep(20)
            except KeyboardInterrupt:
                print("\nStopped tracking.")
                continue
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


#python main.py "email" "password" [file_path] [agent_name] [session_id]

#python main.py "user@example.com" "mypassword"
#python main.py "user@example.com" "mypassword" "/path/to/data.csv"
#python main.py "user@example.com" "mypassword" "/path/to/data.csv" "myagent"
#python main.py "user@example.com" "mypassword" "/path/to/data.csv" "myagent" "FySHda0scDfs1sfHVB7Hw8tl"