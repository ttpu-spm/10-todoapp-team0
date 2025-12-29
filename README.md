# Todo List Web Application

## Overview

Bu loyiha **Software Project Management** kursi uchun tayyorlangan **Todo List web application** shablonidir.  
Maqsad: Flask va Docker orqali **CRUD todo** funksiyalarini yaratish va CI/CD workflow bilan deploy qilish.

---

## Features

- Create new todo items  
- Edit existing todos  
- Delete todos  
- Mark todos as completed  
- Filter todos by status: All, Active, Completed  
- Persistent storage via `todos.json` (agar qo‘shilsa)

---

## Technology Stack

- Python / Flask  
- HTML / CSS (frontend)  
- JSON (simple storage)  
- Docker / Docker Compose  
- Unittest (optional)

---

## Running the Application

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
python src/app.py
```

3. Access in browser:
```
http://localhost:3310
```

### Docker

Build and run:
```bash
docker compose up --build -d
```

Access in browser (on assigned port, e.g. 3314):
```
http://<your-vm-ip>:3314
```

Stop containers:
```bash
docker compose down
```

Check running containers:
```bash
docker ps
```

View logs if needed:
```bash
docker logs <container-name>
```

---

## Development Workflow

- Create a feature branch from `dev`  
- Implement the feature with regular commits  
- Open a Pull Request to `dev`  
- Team review and merge to `dev` (CI runs)  
- Merge `dev` → `main` triggers CD to VM

---

## Deployment Notes

- Docker container runs on your assigned port (e.g., `3314`).  
- Ensure `Dockerfile` exposes the correct port and starts the Flask app.  
- Verify ports and firewall settings on the VM if inaccessible.
- Persist `todos.json` using a Docker volume if needed.