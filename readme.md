# DEV Dashboard

<p align="center">

**Terminal Control Center for Developers**

A modern **terminal-based developer dashboard** for monitoring repositories, Docker containers, GitHub activity, and system status — all from a clean interactive CLI interface.

Built with **Python**, **Docker**, and **Textual**.

</p>

<p align="center">

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Docker](https://img.shields.io/badge/docker-supported-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![UI](https://img.shields.io/badge/ui-textual-purple.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg)

</p>

---

# Overview

**DEV Dashboard** is a lightweight terminal control center designed to give developers quick visibility into their development environment.

It provides a **multi-page terminal UI** for:

- Git repositories  
- GitHub activity  
- Docker containers  
- System monitoring  
- Developer workflow tools  

All within a **fast keyboard-driven interface**.

---

# Screenshot

![DEV Dashboard Screenshot](docs/screenshot.png)

DEV Dashboard
Terminal Control Center

System Stats GitHub Repositories
Repo Activity Todo List
Local Repos Activity Feed

# Navigation pages:

1 Dashboard

2 Repositories

3 Docker

4 Logs



---

# Features

## System Monitoring

View system statistics directly inside the dashboard.

- CPU usage
- Memory usage
- Disk usage
- System overview panel

---

## Git Repository Management

Browse and manage repositories stored in `/projects`.

Features include:

- View all local repositories
- Current branch display
- Last commit information
- Modified files detection
- Commits ahead of origin
- Pull repositories
- View commit history
- View repository status
- Clone new repositories

---

## GitHub Integration

Integrates with the GitHub API to show recent activity.

Includes:

- Push events
- Pull requests
- Issues
- Repository stars
- Activity feed panel

Authentication via **GitHub Personal Access Token**.

---

## Docker Monitoring

Manage Docker containers directly from the dashboard.

Features include:

- List all containers
- View running / stopped status
- Restart containers
- Stop containers
- View container logs
- Auto-refresh container status

---

## Developer Workflow Tools

Panels designed to support development workflows:

- Todo list panel
- Repo activity panel
- Activity event feed
- Repository overview

---

## Terminal UI

Powered by **Textual** for a modern terminal experience.

Features include:

- Interactive terminal UI
- Live updating panels
- Keyboard navigation
- Multi-page dashboard
- Lightweight design
- Clean green terminal theme

---

Each component is implemented as a **modular Textual widget**, making the dashboard easy to extend.

---

# Requirements

- Python **3.11+**
- Docker
- Git
- GitHub Personal Access Token *(optional)*

---

# Installation

Clone the repository:

git clone https://github.com/jwestgarth/dev-dashboard.git

cd dev-dashboard

# Installation (Optional)

## Install Python (Windows)

The dashboard requires **Python 3.11+**.

1. Download Python from:

https://www.python.org/downloads/

2. Run the installer.

⚠️ **Important:** Enable this option during installation:

```
Add Python to PATH
```

3. Click **Install Now**.

---

## Verify Python Installation

Open **PowerShell** and run:

```powershell
python --version
```

You should see something similar to:

```
Python 3.11.x
```

Then verify pip:

```powershell
pip --version
```

---

## Install the Dashboard CLI

Navigate to the project directory:

```powershell
cd C:\projects\dev-dashboard
```

Install the dashboard as a CLI tool:

```powershell
python -m pip install -e .
```

This installs the `dev-dashboard` command locally.

---

## Add Python Scripts to PATH (Windows)

If PowerShell cannot find the `dev-dashboard` command, you need to add the Python Scripts directory to your PATH.

1. Open **Edit Environment Variables**
2. Under **User Variables**, edit **Path**
3. Add the following entry:

```
C:\Users\<your-username>\AppData\Local\Python\pythoncore-3.14-64\Scripts
```

Restart PowerShell after saving.

---

## Run the Dashboard

Once installed, you can launch the dashboard from anywhere:

```powershell
dev-dashboard
```

This will start the terminal dashboard interface.

---

## Run with Docker (Alternative)

If you prefer using Docker:

```powershell
docker compose build -d
```

This will start the dashboard inside a container.

---

## Verify the CLI Command

You can check that the command is available by running:

```powershell
where dev-dashboard
```

Expected output:

```
C:\Users\<username>\AppData\Local\Python\pythoncore-3.14-64\Scripts\dev-dashboard.exe
```

## Configuration

Create a .env file in the project root. 

GITHUB_TOKEN=your_github_token

GITHUB_USER=your_github_username

Generate a token here:

https://github.com/settings/tokens

Recommended permissions

read:user

repo

## Run with Docker (Recommended)

Start the container: 

docker compose up -d

Launch the dashboard:

docker exec -it dev-dashboard python -m app.main

## Keyboard Shortcuts

Global Navigation

| Key | Action         |
| --- | -------------- |
| `1` | Dashboard      |
| `2` | Repositories   |
| `3` | Docker         |
| `4` | Logs           |
| `q` | Quit dashboard |

Repository Controls

| Key   | Action              |
| ----- | ------------------- |
| ↑ ↓   | Select repository   |
| `p`   | Pull repository     |
| `h`   | View commit history |
| `s`   | Git status          |
| `c`   | Clone repository    |
| `ESC` | Close output        |

Docker Controls

| Key   | Action              |
| ----- | ------------------- |
| ↑ ↓   | Select container    |
| `l`   | View container logs |
| `r`   | Restart container   |
| `s`   | Stop container      |
| `ESC` | Close logs          |

# License
MIT License

# Author
Jack Westgarth

GitHub
https://github.com/jwestgarth
