[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/y85avHnH)
# Software Project Management – Continuous Deployment Template

## How to run without Container:

Run following commands in bash:
```bash
source venv/bin/activate
python src/app.py
```

To Run in production:
```bash
source venv/bin/activate
gunicorn --bind 0.0.0.0:3310 --chdir src app:app

# OR in the foreground
source venv/bin/activate && gunicorn --bind 0.0.0.0:3310 --chdir src app:app

# Kill any background:
ps aux | grep gunicorn
pkill -f gunicorn
```

## Overview

This repository is a **teaching template** for a 1–2 week student project in a **Software Project Management** course. It is designed for teams of up to 3 students to learn and practice:

- Collaborative development using Git and GitHub
- Continuous Integration and Continuous Deployment (CI/CD)
- Docker containerization
- Deployment to a shared cloud VM

The primary goal is to build a simple **Todo List web application** while focusing on software engineering processes, team collaboration, and automated deployment—not on complex business logic.

---

## Application Description

### Todo List Manager

Students will build a basic todo manager with the following features:

- **Create** new todo items
- **Edit** existing todos
- **Delete** todos
- **Mark** todos as completed
- **Filter** todos by status:
  - All items
  - Active items
  - Completed items

### Technology Stack

The technology stack is **intentionally simple and flexible**. Teams may choose their preferred framework (e.g., Node.js/Express, Python/Flask, PHP, etc.) as long as they can:

- Containerize the application using Docker
- Run the application on a specific port
- Implement the basic todo features

The focus should remain on the development process, collaboration, and deployment, not on mastering a particular framework.

---

## Collaboration Workflow

All collaboration is done through **GitHub**. The repository follows a structured branching model with protected branches to ensure code quality and proper review processes.

### Branch Strategy

- **`main` branch** – Production-ready code
  - Protected: no direct pushes allowed
  - Merging to `main` triggers continuous deployment
  - Represents the current live version

- **`dev` branch** – Integration branch for development
  - Protected: no direct pushes allowed
  - Features are merged here first for testing
  - Serves as a staging environment

- **Feature branches** – Short-lived branches for individual features
  - Created from `dev`
  - Named descriptively (e.g., `feature/add-edit-functionality`, `fix/delete-button`)
  - Deleted after merging

### Development Workflow

1. **Plan**: Create GitHub Issues for tasks and features
2. **Branch**: Create a feature branch from `dev`
3. **Develop**: Implement the feature with regular commits
4. **Pull Request**: Open a PR from feature branch to `dev`
5. **Review**: Team members review the code
6. **Merge**: After approval, merge to `dev` (CI tests run)
7. **Release**: When stable, create a PR from `dev` to `main`
8. **Deploy**: Merge to `main` triggers automatic deployment

### GitHub Features

- **Issues**: Track tasks, bugs, and features
- **Pull Requests**: Code review and discussion before merging
- **Projects** (optional): Organize work in Kanban boards
- **Actions**: Automated CI/CD pipelines

---

## Deployment Process

Deployment is automated using **GitHub Actions** and **Docker** to a shared cloud VM. Each team (or team member) has a dedicated Linux user account and port range on the VM.

### Architecture

1. **GitHub Actions Workflow**: Triggered on merge to `main`
2. **Docker Build**: Creates a container image from the project
3. **SSH Connection**: Connects to the VM using stored credentials
4. **Container Deployment**: Stops old container, starts new one on assigned port

### VM Setup

Each team receives:

- A **Linux user account** on the shared VM
- A **dedicated port** or small port range (e.g., 8001-8003)
- SSH access credentials (students create their own SSH key pair)

### Port Configuration

**Important**: Your web application must be configured to listen on your team's assigned port. This is typically done in:

- Node.js: `app.listen(process.env.PORT || 8001)`
- Flask: `app.run(host='0.0.0.0', port=8001)`
- Other frameworks: Check documentation for port configuration

### CI vs CD

- **CI (Continuous Integration)**: Runs on PR to `dev`
  - Runs automated tests
  - Validates code quality
  - Does NOT deploy

- **CD (Continuous Deployment)**: Runs on merge to `main`
  - Builds Docker image
  - Stops previous container instance
  - Starts new container on assigned port
  - Application becomes live

---

## Team Setup Instructions

### Prerequisites

1. Fork or clone this repository for your team
2. Receive VM credentials and port assignment from instructor
3. Install Git and basic command-line tools

### Step 1: SSH Key Setup

Each team needs to create an SSH key pair for secure deployment:

```bash
# Generate SSH key pair (do not use a passphrase)
ssh-keygen -t rsa -b 4096 -f ~/.ssh/spm_deploy_key -N ""

# Copy public key to VM (use your assigned username)
ssh-copy-id -i ~/.ssh/spm_deploy_key.pub username@vm-address
```

### Step 2: GitHub Secrets Configuration

Add the following secrets to your GitHub repository (Settings → Secrets and variables → Actions):

- `SSH_PRIVATE_KEY`: Content of your private key file (`~/.ssh/spm_deploy_key`)
- `VM_HOST`: VM IP address or hostname (provided by instructor)
- `VM_USER`: Your assigned username on the VM
- `VM_PORT`: Your assigned application port
- `DEPLOY_PATH`: Target directory on VM (e.g., `/home/username/todo-app`)

### Step 3: Workflow Configuration

The repository includes a template GitHub Actions workflow. You need to adapt:

1. User name in the workflow file
2. Target directory path
3. Port number in your application
4. SSH key secret names (if different)

### Step 4: Branch Protection

Set up branch protection rules in GitHub:

1. Go to Settings → Branches
2. Add rule for `main`:
   - Require pull request reviews before merging
   - Require status checks to pass
   - No direct pushes
3. Add rule for `dev`:
   - Require pull request reviews before merging
   - No direct pushes

### Step 5: Docker Configuration

Ensure your `Dockerfile`:

- Installs all dependencies
- Exposes the correct port
- Starts your web application
- Uses environment variables for configuration

Example `Dockerfile` structure:

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 8001
CMD ["npm", "start"]
```

---

## Development Guidelines

### Code Quality

- Write clean, readable code
- Follow your chosen language's style guide
- Add meaningful commit messages
- Keep PRs focused and small

### Testing

- Write tests for critical functionality
- Ensure all tests pass before creating a PR
- CI pipeline will run tests automatically

### Communication

- Use GitHub Issues for tracking work
- Comment on PRs with feedback
- Keep team members informed of progress
- Ask for help when stuck

### Deployment Checklist

Before merging to `main`, ensure:

- [ ] All tests pass in `dev`
- [ ] Application runs correctly in Docker
- [ ] Correct port is configured
- [ ] GitHub Secrets are set up
- [ ] SSH access to VM is working
- [ ] Previous deployments have been tested

---

## Troubleshooting

### Common Issues

**Container won't start:**
- Check Docker logs: `docker logs <container-name>`
- Verify port configuration
- Ensure all dependencies are installed

**Deployment fails:**
- Verify GitHub Secrets are set correctly
- Test SSH connection manually
- Check VM disk space and permissions

**Application not accessible:**
- Confirm correct port is exposed
- Check firewall rules on VM
- Verify container is running: `docker ps`

**Tests fail in CI:**
- Run tests locally first
- Check for environment-specific issues
- Review test logs in GitHub Actions

---

## Learning Objectives

By completing this project, students will:

1. Understand Git workflows and branching strategies
2. Practice code review and collaboration
3. Set up and use CI/CD pipelines
4. Deploy containerized applications
5. Manage cloud infrastructure
6. Work effectively in a team
7. Use project management tools

---

## Support

For questions and support:

- Open an issue in the repository
- Contact the course instructor
- Collaborate with your team members
- Refer to course materials and documentation

---

## License

This is an educational template. Students may use it for learning purposes in the Software Project Management course.
