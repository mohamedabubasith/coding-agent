# Project Plan

## Architecture
- **database**
  - database.py
- **models**
  - models.py
- **authentication**
  - auth.py
- **application**
  - main.py
- **dependencies**
  - requirements.txt

## Tasks
- **Create project directory structure and required files** (Agent: task)
  - Details: {'action': 'create_dirs', 'paths': ['app'], 'file_path': 'app/requirements.txt', 'prompt': 'Create empty requirements.txt file', 'command': 'mkdir -p app && touch app/requirements.txt app/database.py app/models.py app/auth.py app/main.py'}
- **Write requirements.txt with production-ready dependencies** (Agent: coding)
  - Details: {'action': 'write_file', 'file_path': 'app/requirements.txt', 'prompt': 'Write requirements.txt with the following dependencies: fastapi, uvicorn, python-dotenv, sqlalchemy, python-jose[cryptography], passlib[bcrypt], pydantic[email]'}
- **Implement database connection setup with SQLAlchemy** (Agent: coding)
  - Details: {'action': 'write_file', 'file_path': 'app/database.py', 'prompt': "Create a database.py file that sets up SQLAlchemy with SQLite. Use SQLALCHEMY_DATABASE_URL = 'sqlite:///./users.db'. Create an engine with connect_args={'check_same_thread': False}. Define a SessionLocal dependency with sessionmaker. Create a Base declarative base. Include a get_db generator function that yields a session and closes it properly. Use proper type hints and error handling."}
- **Define User model with id, email, hashed_password** (Agent: coding)
  - Details: {'action': 'write_file', 'file_path': 'app/models.py', 'prompt': "Create a User model in models.py using SQLAlchemy ORM. Include: id (Integer, primary_key=True, index=True), email (String, unique=True, index=True, nullable=False), hashed_password (String, nullable=False). Inherit from Base. Include __tablename__ = 'users'. Add proper type hints and documentation."}
- **Implement JWT token creation and password hashing functions** (Agent: coding)
  - Details: {'action': 'write_file', 'file_path': 'app/auth.py', 'prompt': "Create auth.py with the following: 1) SECRET_KEY and ALGORITHM constants (use a random 32-byte key and HS256). 2) hash_password function using passlib's bcrypt context. 3) verify_password function to compare plain password with hashed password. 4) create_access_token function that generates JWT token with user email and expires in 30 minutes. 5) decode_access_token function to validate and decode JWT token. Include proper error handling for expired or invalid tokens. Use python-jose and passlib."}
- **Implement FastAPI app with /register and /login endpoints** (Agent: coding)
  - Details: {'action': 'write_file', 'file_path': 'app/main.py', 'prompt': "Create main.py with a FastAPI app instance. Import dependencies from database, models, auth. Create Pydantic models for UserCreate (email, password) and UserResponse (id, email). Implement /register POST endpoint that: 1) validates email format, 2) checks if user exists, 3) hashes password, 4) creates user in DB, 5) returns UserResponse. Implement /login POST endpoint that: 1) validates user credentials, 2) generates JWT token, 3) returns {'access_token': token, 'token_type': 'bearer'}. Use dependency injection for get_db. Add proper HTTPException responses for invalid credentials and duplicate emails. Include docstrings and type hints. Use @app.on_event('startup') to create tables."}
- **Verify file structure and dependencies are correctly set up** (Agent: execution)
  - Details: {'action': 'run_command', 'file_path': '', 'prompt': '', 'command': 'cd app && ls -la requirements.txt database.py models.py auth.py main.py'}
- **Install dependencies and verify FastAPI app starts without errors** (Agent: execution)
  - Details: {'action': 'run_command', 'file_path': '', 'prompt': '', 'command': 'cd app && pip install -r requirements.txt && uvicorn main:app --reload --host 0.0.0.0 --port 8000'}
- **Test /register and /login endpoints with curl** (Agent: execution)
  - Details: {'action': 'run_command', 'file_path': '', 'prompt': '', 'command': 'cd app && curl -X \'POST\' \'http://127.0.0.1:8000/register\' -H \'Content-Type: application/json\' -d \'{"email":"test@example.com","password":"password123"}\' && curl -X \'POST\' \'http://127.0.0.1:8000/login\' -H \'Content-Type: application/json\' -d \'{"email":"test@example.com","password":"password123"}\''}
