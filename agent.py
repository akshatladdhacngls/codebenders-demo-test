import os
import re
import docker
import json
import socket
import subprocess
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.message import AnyMessage
from langgraph.graph import StateGraph, START, END

load_dotenv("./.env")

# Enhanced OpenAI LLM configuration
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.2,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)


# Enhanced State to support conversational flow
class State(TypedDict):
    containers: dict


# ---- CORE DEVOPS TOOLS ----


@tool
def scan_projects() -> dict:
    """Scans the directory for projects and classifies them as frontend or backend."""
    detected_projects = {}
    excluded_dirs = {".venv", "node_modules", "__pycache__", ".git"}
    frontend_folder_name = "react-sample-project"
    backend_folder_name = "backend"
    folders_to_scan = [frontend_folder_name, backend_folder_name]

    for project in folders_to_scan:
        if os.path.isdir(project) and project not in excluded_dirs:
            files = [
                os.path.join(dp, f)
                for dp, _, filenames in os.walk(project)
                for f in filenames
                if not any(excl in dp for excl in excluded_dirs)
            ]

            # Project type detection
            if any(fname.endswith(("package.json")) for fname in files):
                detected_projects["frontend"] = {"path": project, "files": files}
                print(f"✅ Detected frontend project: {project}")
            elif any(fname.endswith(("requirements.txt", ".py")) for fname in files):
                detected_projects["backend"] = {"path": project, "files": files}
                print(f"✅ Detected backend project: {project}")

    if not detected_projects:
        print("⚠️ No valid project folders specified or no files found.")
        return {"error": "No valid project folders specified or no files found."}

    # print(f"✅ Detected Projects: {detected_projects}")
    return {"projects": detected_projects}


@tool
def generate_dockerfile_with_openai(project_info: str) -> str:
    """
    Uses OpenAI to generate a Dockerfile for a project.
    project_info: JSON string with keys 'project_path', 'project_type', and optional 'port'
    """
    # Parse project info
    info = json.loads(project_info)
    project_path = info["project_path"]
    project_type = info["project_type"]
    port = info.get("port", 8000 if project_type == "backend" else 3000)
    server_file = "main.py" if project_type == "backend" else None

    if project_type == "frontend":
        prompt = f"""
        Your task is to generate a **valid Dockerfile** for a frontend project named '{project_path}'.
        
        **Rules:**
        - The response must contain **only the Dockerfile content** (no explanations, no markdown formatting).
        - Use **Node.js 18 Alpine** as the base image.
        - Ensure the app starts with `npm start`.
        - The response must start with `FROM node:18-alpine` and contain only valid Docker instructions.

        **Example Output (Do NOT return in Markdown format, only the Dockerfile content):**
            FROM node:18-alpine
            WORKDIR /app
            COPY package*.json ./
            RUN npm install
            COPY . .
            EXPOSE 3000
            CMD ["npm", "start"]
        """
    else:  # Backend
        server_file_path = os.path.join(project_path, server_file)
        file_content = read_file_content(server_file_path)

        if not file_content:
            print(f"⚠️ Server file {server_file} not found. Using default entry point.")
            entry_point = "main"
            port = 8000
        else:
            entry_point = server_file.replace(".py", "")
            if "run(" in file_content:
                port_match = re.search(r"run\(.*port\s*=\s*(\d+)", file_content)
                if port_match:
                    port = int(port_match.group(1))

        prompt = f"""
        Your task is to generate a **valid Dockerfile** for a backend project named '{project_path}'.
        
        **Project Details:**
        - The backend application starts using the file `{server_file}`
        - Runs on port: {port}
        - Below is the full content of `{server_file}`:

        ```
        {file_content}
        ```

        **Rules:**
        - The response must contain **only the Dockerfile content** (no explanations, no markdown formatting).
        - Use **Python 3.10** as the base image.
        - Assume a valid `requirements.txt` file is already provided.
        - Ensure the application starts using `uvicorn {entry_point}:app --host 0.0.0.0 --port {port}` if FastAPI is detected.
        - If Flask is detected, start with `flask run --host=0.0.0.0 --port={port}`.
        - The response must start with `FROM python:3.10` and contain only valid Docker instructions.

        **Example Output (Do NOT return in Markdown format, only the Dockerfile content):**
        FROM python:3.10
        WORKDIR /app
        COPY requirements.txt .
        RUN pip install --no-cache-dir -r requirements.txt
        COPY . .
        EXPOSE {port}
        CMD ["uvicorn", "{entry_point}:app", "--host", "0.0.0.0", "--port", "{port}"]
        """

    response = llm.invoke(prompt)
    dockerfile_content = response.content.strip()

    # Save the Dockerfile
    dockerfile_path = os.path.join(project_path, "Dockerfile")
    with open(dockerfile_path, "w") as f:
        f.write(dockerfile_content + "\n")

    return dockerfile_content


@tool
def build_and_run_container(container_config: str) -> dict:
    """
    Builds and runs a Docker container based on provided configuration.
    container_config: JSON string with 'project_path', 'port', 'name' keys
    """
    config = json.loads(container_config)
    project_path = config["project_path"]
    port = config["port"]
    container_name = config["project_path"]
    client = docker.from_env()
    project_path = os.path.abspath(project_path)

    try:
        # Stop and remove any running container with the same name
        existing_containers = client.containers.list(
            all=True, filters={"name": container_name}
        )
        for container in existing_containers:
            print(f"\n🛑 Stopping and removing existing container {container_name}...")
            container.stop()
            container.remove()

        # # Build image
        # print(f"🐳 Building Docker image for {project_path}...")
        # image, _ = client.images.build(path=project_path, tag=container_name)

        # # Find available port if needed
        # if is_port_in_use(port):
        #     port = find_available_port()
        #     print(f"⚠️ Port {config['port']} in use. Using port {port} instead.")

        # print(f"🚀 Starting container '{container_name}' with port mapping {port}...\n")
        # # Run container
        # container = client.containers.run(
        #     image.id,
        #     detach=True,
        #     ports={f"{port}/tcp": port},
        #     name=container_name,
        # )
        print(f"✅  Successfully created the {container_name} Dockerfile.")
        return {
            "container_id": "N/A",
            "name": container_name,
            "port": port,
            "status": "Disabled the building and running the DOckerfile",
        }

    except Exception as e:
        return {"error": str(e)}


# ---- NEW DEVOPS TOOLS ----
@tool
def setup_github_actions(project_data: dict) -> str:
    """Creates GitHub Actions workflow for building Docker images and deploying to EC2 via Docker Hub."""

    if "project_path" not in project_data:
        raise ValueError("Missing required key 'project_path' in project_data")

    project_path = project_data["project_path"]
    project_name = os.path.basename(project_path)
    workflow_dir = os.path.join(os.getcwd(), ".github", "workflows")
    os.makedirs(workflow_dir, exist_ok=True)
    
    is_frontend = os.path.exists(os.path.join(project_path, "package.json"))
    port_mapping = "3000:3000" if is_frontend else "8000:8000"
    
    # Generate a fixed workflow YAML without using LLM
    workflow_content = f"""name: Build and Deploy {project_name}

on:
  push:
    branches:
      - main

jobs:
  build_and_push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{{{ secrets.DOCKER_HUB_USERNAME }}}}
          password: ${{{{ secrets.DOCKER_HUB_PASSWORD }}}}

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: ./{project_path}
          file: ./{project_path}/Dockerfile
          push: true
          tags: ${{{{ secrets.DOCKER_HUB_USERNAME }}}}/{project_name}:${{{{ github.sha }}}}

  deploy:
    needs: build_and_push
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to EC2
        uses: appleboy/ssh-action@master
        with:
          host: ${{{{ secrets.HOST }}}}
          username: ${{{{ secrets.USERNAME }}}}
          key: ${{{{ secrets.SSH_KEY }}}}
          script: |
            # Check if Docker is installed, install if not
            if ! command -v docker &> /dev/null
            then
              echo "Docker not found. Installing Docker..."
              sudo apt update
              sudo apt install -y docker.io
              sudo systemctl start docker
              sudo systemctl enable docker
              sudo usermod -aG docker $USER
              newgrp docker
            fi
            # Log in to Docker Hub
            echo "${{ secrets.DOCKER_HUB_PASSWORD }}" | sudo docker login -u "${{ secrets.DOCKER_HUB_USERNAME }}" --password-stdin
            # Pull the latest image and run the container
            sudo docker pull ${{{{ secrets.DOCKER_HUB_USERNAME }}}}/{project_name}:${{{{ github.sha }}}}
            # Stop and remove existing container if running
            if sudo docker ps -q --filter "name={project_name}"; then
              sudo docker stop {project_name}
              sudo docker rm {project_name}
            fi
            # Run the new container
            sudo docker run -d --restart always -p {port_mapping} --name {project_name} ${{{{ secrets.DOCKER_HUB_USERNAME }}}}/{project_name}:${{{{ github.sha }}}}
"""

    # Save workflow file
    workflow_filename = f"{project_name}-deploy.yml"
    workflow_path = os.path.join(workflow_dir, workflow_filename)
    with open(workflow_path, "w") as f:
        f.write(workflow_content)

    return workflow_content

# ---- HELPER FUNCTIONS ----
def read_file_content(file_path):
    """Reads the entire content of a given file and returns it."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    else:
        return None


def is_port_in_use(port):
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def find_available_port(start_port=8000, end_port=9000):
    """Find an available port within a range."""
    for port in range(start_port, end_port):
        if not is_port_in_use(port):
            return port
    raise RuntimeError("No available ports found in range!")


# ---- DIRECT DEPLOYMENT FUNCTION ----
def run_deployment_workflow(state):
    """Execute the full deployment workflow."""
    # First scan projects
    scan_result = scan_projects.invoke({})  # Use .invoke() instead of direct call
    projects = scan_result["projects"]

    # Generate dockerfiles for each project
    for role, project_data in projects.items():
        project_info = {"project_path": project_data["path"], "project_type": role}
        dockerfile = generate_dockerfile_with_openai.invoke(
            json.dumps(project_info)
        )  # Use .invoke()

    # Setup CI/CD
    cicd_results = {}
    for role, project_data in projects.items():
        cicd_results[role] = setup_github_actions.invoke(
            {"project_data": {"project_path": project_data["path"]}}
        )

    # Build and run containers
    container_results = {}
    for role, project_data in projects.items():
        default_port = 3000 if role == "frontend" else 8000
        container_config = {
            "project_path": project_data["path"],
            "port": default_port,
            "name": f"{project_data['path']}-{role}",
        }
        container_results[role] = build_and_run_container.invoke(
            json.dumps(container_config)
        )  # Use .invoke()

    return {
        "success"   : True,
        "containers": container_results,
    }


# ---- WORKFLOW CREATION ----
def create_devops_agent():
    """Create the DevOps agent workflow graph."""
    builder = StateGraph(State)
    # Add deployment node only
    builder.add_node("deployment_workflow", run_deployment_workflow)
    # Direct path from start to deployment and end
    builder.add_edge(START, "deployment_workflow")
    builder.add_edge("deployment_workflow", END)
    return builder.compile()


# Initialize agent with empty state
def get_initial_state():
    return State(
        containers={},
    )


# ---- USAGE EXAMPLES ----

if __name__ == "__main__":
    # Example 1: Conversational mode
    graph = create_devops_agent()
    initial_state = get_initial_state()
    # Deploy command example
    deploy_result = graph.invoke({**initial_state})
    # Ensure serialization before printing
    print(json.dumps(deploy_result, indent=2))