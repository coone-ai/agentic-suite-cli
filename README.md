# AI AGENT API - USER GUIDE

## REQUIREMENTS
- Python 3.6 or higher
- Internet connection
- Valid user account

## INSTALLATION
1. Download the program to your computer
2. Open Terminal/Command Prompt
3. Navigate to the program folder

## USAGE METHODS

### 1. INTERACTIVE MODE (Recommended - For first use)
Run the program without any parameters:
```bash
python main.py
```

This mode guides you step by step:
- Login with email and password
- Select or create new Agent
- Select or create new Session
- Upload file
- Track results

### 2. QUICK UPLOAD MODE
To quickly upload your file:
```bash
python main.py "email" "password" [file_path] [agent_name] [session_id]
```

**Examples:**
```bash
# Only login credentials (file, agent and session selected interactively)
python main.py "user@example.com" "mypassword"

# File path specified (agent and session selected interactively)
python main.py "user@example.com" "mypassword" "/path/to/data.csv"

# Agent name specified (session selected interactively)
python main.py "user@example.com" "mypassword" "/path/to/data.csv" "myagent"

# Both agent and session specified
python main.py "user@example.com" "mypassword" "/path/to/data.csv" "myagent" "FySHPoH0TIMHVB7Hw8tl"
```

## STEP BY STEP USAGE

### 1. LOGIN
- Enter your email address
- Enter your password (appears as asterisks for security)

### 2. AGENT MANAGEMENT
Agent is the virtual workspace where you will use AI services.

**Options:**
- View existing agents
- Create new agent
- Change agent

### 3. SESSION MANAGEMENT
Session is a work session created for a specific task.

**Available tasks:**
1. **Product Description Writer**
   - Generates structured and engaging product descriptions using customer data
   - Creates SEO-compliant and personalized content

2. **Product Title Writer**
   - Creates keyword-rich, clear and SEO-optimized product titles
   - Optimized for marketplace visibility and search ranking

### 4. FILE UPLOAD
**Supported file formats:**
- CSV (.csv)
- JSON (.json)
- Excel (.xlsx, .xls)

### 5. RESULT TRACKING
- Track the processing status of uploaded files
- View process status with progress bar
- Download completed files

## MENU OPTIONS
1. **Select Agent** - Select agent
2. **Create New Agent** - Create new agent
3. **Select Session** - Select session
4. **Create New Session** - Create new session
5. **Upload File to Session** - Upload file to session
6. **View Result (Session Output)** - View results
0. **Exit** - Exit

## EXAMPLE USAGE SCENARIOS

### SCENARIO 1: First Time Use
1. `python main.py`
2. Login with email and password
3. Select "Create New Agent" (2)
4. Enter agent name (e.g., "My E-commerce Store")
5. Select "Create New Session" (4)
6. Choose task (1 or 2)
7. Select "Upload File to Session" (5)
8. Enter file path
9. Track with "View Result" (6)

### SCENARIO 2: Quick Upload
1. `python main.py "email" "password"`
2. Program will ask for file path, agent and session selection
3. Make your selections, file will be uploaded automatically

**Alternative:** You can provide the parameters you want:
```bash
python main.py "email" "password" "file.csv"                    # File specified
python main.py "email" "password" "file.csv" "agent_name"        # Agent also specified
python main.py "email" "password" "file.csv" "agent_name" "session_id"  # All specified
```

## TROUBLESHOOTING

### Common Problems and Solutions:

1. **"Login failed" error**
   - Check your email and password
   - Check your internet connection

2. **"File does not exist" error**
   - Check the file path
   - Make sure the file actually exists

3. **"Unsupported file format" error**
   - Only CSV, JSON, Excel files are supported
   - Check the file extension

4. **"Agent not found" error**
   - Make sure you typed the agent name correctly
   - Pay attention to case sensitivity

5. **"Session not found" error**
   - Check the session ID
   - Make sure the session is still active

## TECHNICAL SUPPORT
When you encounter problems:
1. Note the error message
2. Save the command you used
3. Specify the file format and size
4. Contact the technical support team

## CONTACT
For technical support and questions:
- **Email:** semih.durgun@co-one.co
