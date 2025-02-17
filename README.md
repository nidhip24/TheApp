# Web Application with Load Balancing

## Overview

This project contains a containerized web application built using **FastAPI**, **PostgreSQL** for data storage, and **Nginx** as a reverse proxy for load balancing. The web application exposes API endpoints to create and fetch user data, and it is horizontally scalable across multiple instances. The database stores user data, initialized with a `users` table, and Docker Compose is used to manage all services.

## Services

- **Web Application (FastAPI)**: Provides an API to create and fetch user data (POST `/user` and GET `/user/{id}`).
- **Database (PostgreSQL)**: Stores user data securely and initializes the database with the `users` table.
- **Reverse Proxy (Nginx)**: Distributes incoming requests evenly across multiple web application containers for load balancing.

## Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/nidhip24/TheApp.git
cd TheApp
```

### Step 2: Build and Start Containers

To build and start all the services (web, database, and reverse proxy), run:

```bash
docker-compose up --d
```

This will:
- Build the **web** container from the `Dockerfile`.
- Set up the **PostgreSQL** database container and initialize it with the `init.sql` script.
- Set up the **Nginx** reverse proxy to load balance the web application.
- Scale the web application container to 3 replicas.

### Step 3: Access the Application

- **Web Application**: The web application will be accessible via `http://localhost:8000`.
- **API Endpoints**:
  - `POST /user`: Create a new user.
  - `GET /user/{id}`: Retrieve user data by ID.
  
### Step 4: View Logs

Logs for the web application will be saved to `./app/logs/` on your local machine due to the bind mount specified in `docker-compose.yml`.

---

## Docker Configuration Explanation

### **Dockerfile**

```dockerfile
FROM python:3.9-slim

# Set a non-root user
RUN addgroup --system appgroup && adduser --system --group appuser

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Set proper ownership
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the port on which the application will run
EXPOSE 8080

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

- **Purpose**: 
  - This `Dockerfile` builds the container image for the FastAPI application.
  - A non-root user (`appuser`) is created for security reasons, and the necessary dependencies are installed from `requirements.txt`.
  - The FastAPI app is run using `uvicorn` on port `8080`.

### **docker-compose.yml**

```yaml
networks:
  app_network:
    driver: bridge

services:
  nginx:
    image: nginx:latest
    restart: always
    ports:
      - "8000:8000"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
    networks:
      - app_network

  web:
    build: ./app/
    deploy:
      replicas: 3  # Scale to 3 instances
    ports:
      - "8001-8003:8080"
    volumes:
      - ./app/logs/:/app/logs/
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/userdb
    restart: always
    depends_on:
      - db
    networks:
      - app_network

  db:
    image: postgres:13
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=userdb
    ports:
      - "5432:5432"
    networks:
      - app_network

volumes:
  postgres_data:
```

- **Purpose**:
  - The `docker-compose.yml` file orchestrates the web, database, and Nginx services.
  - The **web** service builds from the Dockerfile, scales to 3 replicas, and connects to the PostgreSQL database.
  - The **nginx** service acts as a reverse proxy, handling incoming traffic and load balancing across the web application instances.
  - The **db** service sets up a PostgreSQL container with the necessary environment variables and initializes the database with the `init.sql` file.
  - **Volumes**: Ensures persistent database storage and log file storage on the local machine.

### **Nginx Configuration (nginx.conf)**

```nginx
events {
    worker_connections 1024;
}

http {
    upstream web_servers {
        server web:8080;
        server web_1:8080;
        server web_2:8080;
    }

    server {
        listen 8000;

        location / {
            proxy_pass http://web_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```

- **Purpose**:
  - This Nginx configuration sets up a reverse proxy to distribute incoming requests across three instances of the **web** service (FastAPI containers).
  - The `proxy_pass` directive sends the request to one of the `web_servers` (web containers) based on Nginx's load balancing mechanism.

---

## Scaling and Load Balancing

- **Scaling**: The web application is scaled to 3 instances using Docker Compose's `deploy.replicas` directive under the **web** service.
- **Load Balancing**: Nginx is configured to balance the incoming traffic between the three `web` instances. The requests are distributed evenly using round-robin load balancing.

---

## Security Measures

1. **Non-root User**: The FastAPI application container runs as a non-root user (`appuser`) to mitigate security risks associated with running as root.
2. **Environment Variables**: Sensitive data like the database URL and credentials are passed as environment variables to the containers. You should avoid hardcoding sensitive information in the codebase.
3. **Database Security**: The PostgreSQL container is configured with a secure password and environment variables for authentication.

---

