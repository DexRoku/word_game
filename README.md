# 🎮 Word Game App

![Word Game Banner](https://img.shields.io/badge/Word_Game-Streamlit-blue?style=for-the-badge&logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Container-blue?style=for-the-badge&logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Cluster-blue?style=for-the-badge&logo=kubernetes)
![Helm](https://img.shields.io/badge/Helm-Package_manager-blue?style=for-the-badge&logo=helm)

---

## 🚀 Project Overview

This is a **Word Game** built using [Streamlit](https://streamlit.io/), a Python framework for creating interactive web apps.  
The app is containerized using Docker and deployed to a Kubernetes cluster using Helm charts.

---

## 🧰 Tech Stack

- **Python & Streamlit** — Interactive UI for the word game  
- **Docker** — Containerizing the app image  
- **Kubernetes** — Orchestrating container deployment  
- **Helm** — Managing Kubernetes manifests and deployments  
- **Kind** — Local Kubernetes cluster for development/testing  

---

## 🛠️ How To Run Locally

1. **Build Docker Image**

   ```bash
   docker build -t word-game-app:latest .
    ```
2. **Run Docker Container**

   ```bash
   kind load docker-image word-game-app:latest --name word-game-cluster
   ```
3. **Deploy to Kubernetes**

   ```bash
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
    ```

4. ** Port Forward Service**

   ```bash
   kubectl port-forward service/word-game-service 8501:80
   ```

4. **Access the App**

   Open your browser and go to [http://localhost:8501](http://localhost:8501) to access the Word Game app.

---

## 📦 Helm Chart

'''This project includes a Helm chart for easy deployment to Kubernetes. The chart is located in the `word-game` directory.
The chart includes templates for the deployment, service, and configmap resources.'''

```yaml
apiVersion: v2
name: word-game
description: A Helm chart for the Word Game app
type: application

# Helm Chart version
version: 0.1.0

# Application version
appVersion: "1.0"

# Define the Kubernetes resources
templates:
  - deployment.yaml
  - service.yaml
  - configmap.yaml
```

## Configuration
You can configure the Helm chart by modifying the `values.yaml` file. The following parameters can be set:

```yaml
Docker image repository & tag

Replica count

Service type and port

Environment variables (GAME_TITLE, GAME_VERSION, GAME_DEVELOPER)

```yaml
replicaCount: 3

image:
  repository: word-game-app
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8501

env:
  GAME_TITLE: "My Word Game"
  GAME_VERSION: "1.0"
  GAME_DEVELOPER: "Rohith Raju"
```