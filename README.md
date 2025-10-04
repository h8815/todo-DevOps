# 🧩 MyTodo – Flask Web App with Full DevOps Pipeline 🚀

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Docker Pulls](https://img.shields.io/docker/pulls/h8815/todowebapp)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey)
![Kubernetes](https://img.shields.io/badge/deployed%20on-Kubernetes-blue)

---

**MyTodo** started as a simple Flask to-do manager — and grew into a **production-ready, CI/CD-driven web application** deployed with modern DevOps practices.  
It combines a lightweight **Flask + Bootstrap** frontend with a robust **containerized DevOps workflow** using **Jenkins, Docker, Kubernetes, Helm, ArgoCD, Prometheus, and Grafana**.

---

## 🖥️ Application Preview

### 🚀 Live Demo
👉 Try it out: [[https://todo-list-gcpj.onrender.com](https://todo-list-gcpj.onrender.com)]

---

## ⚙️ DevOps Workflow

Here’s the complete end-to-end pipeline that powers the project:

![Workflow](assets/workflow-2.png)

### 🔧 Workflow Breakdown
1. **Developer** pushes code to **GitHub**
2. **Jenkins** pulls code → runs tests → builds Docker image → pushes to **DockerHub**
3. **ArgoCD** (GitOps) pulls updated manifests → deploys app to **Kubernetes (Helm)**
4. **Prometheus** collects metrics → **Grafana** visualizes and alerts via email  
   
Result: **Every code change automatically builds, tests, deploys, and monitors itself.**

---

## ✅ Application Features
- 🔐 **User Authentication** – Register, login, and manage your own todos
- ➕ **CRUD Operations** – Create, edit, delete tasks with timestamps
- 🔍 **Search Functionality** – Filter todos by title
- 📱 **Responsive UI** – Clean design using Bootstrap 5
- 💾 **SQLite + SQLAlchemy** – Lightweight and simple to run anywhere

---

## 🧰 DevOps Stack Highlights

| Layer | Tool | Purpose |
|-------|------|----------|
| **Version Control** | Git & GitHub | Source code management |
| **CI/CD Automation** | Jenkins | Build, test, and push Docker images |
| **Containerization** | Docker | App packaging and portability |
| **Orchestration** | Kubernetes + Helm | Declarative deployment management |
| **GitOps** | ArgoCD | Continuous deployment from Git |
| **Monitoring** | Prometheus | Metrics collection and alerting |
| **Visualization** | Grafana | Real-time dashboards |


---

## 🧪 CI/CD Pipeline Overview

1. **Code Commit:** Developer pushes code → GitHub triggers Jenkins.
2. **CI Stage:** Jenkins runs tests, builds Docker image, pushes to DockerHub.
3. **CD Stage:** ArgoCD syncs manifests → deploys latest version to Kubernetes via Helm.
4. **Monitoring:** Prometheus gathers metrics; Grafana visualizes dashboards and sends alerts.

This ensures **zero-touch, continuous delivery** from commit to production.

---

## 📦 Requirements

- Python 3.8+
- Flask 3.x
- Docker & Docker Compose
- Jenkins
- Kubernetes cluster (Minikube/EKS)
- Helm v3+
- ArgoCD
- Prometheus & Grafana stack

---

## 🛠️ Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/h8815/todo-DevOps.git
cd todo-DevOps
```
2. **Create virtual environment**

```bash 
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Run locally**
```bash
flask run
# or
python myapp/run.py
```
Then open your browser and navigate to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📊 Monitoring with Prometheus

- Metrics are available at: [http://127.0.0.1:5000/metrics](http://127.0.0.1:5000/metrics)
- Configure your Prometheus server to scrape this endpoint.

Example Prometheus scrape config:
```yaml
scrape_configs:
  - job_name: 'todo-devops'
    static_configs:
      - targets: ['localhost:5000']
```

---

---

## 🐳 Docker Setup

Build and run using Docker:
```bash
docker build -t mytodo-app .
docker run -p 5000:5000 mytodo-app
```

---

## 🚀 Deployment (DevOps Pipeline)

1. **Continuous Integration**: Jenkins pipeline (`Jenkinsfile`) builds & tests automatically.

2. **Image Registry**: Docker image is pushed to DockerHub or AWS ECR.

3. **Continuous Deployment**: ArgoCD syncs the Helm chart and deploys the latest image to Kubernetes.

4. **Monitoring & Alerts**: Prometheus scrapes `/metrics`; Grafana visualizes dashboards and sends alerts.

---

## 📁 Project Structure

```
ToDO-Devops/
│
├── myapp/
│   ├── app.py             # Main Flask application
│   ├── run.py             # EntryPoint of application
│   ├── templates/         # Jinja2 HTML templates
│   ├── static/            # CSS, JS, and static assets
│   └── instance/
│       └── todo.db        # SQLite database (auto-generated)
├── requirements.txt   # Python dependencies
├── Dockerfile             # Docker build instructions
├── Jenkinsfile            # Jenkins CI/CD pipeline
├── render.yaml            # Render deployment config
└── README.md              # Project documentation
```
---

## 🙌 Contributing

Pull requests and issues are welcome!  
Please open an issue to discuss your ideas or improvements.