# Quick Start

This guide walks through the minimum steps required to run the AI Study Assistant backend locally.

For detailed information about the architecture, deployment, testing, and API design, refer to the documentation inside the `docs` directory.

---

# Prerequisites

Before running the project, ensure the following software is installed:

- Python (latest stable version)
- Git
- Docker Desktop

---

# Clone the Repository

Clone the repository and enter the project directory.

```bash
git clone <repository-url>

cd <repository-name>
```

---

# Create a Virtual Environment

Create and activate a Python virtual environment.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

---

# Install Dependencies

Install the project dependencies.

```bash
pip install -r requirements.txt
```

---

# Configure Environment

Create a `.env` file in the project root and configure the required environment variables.

See [Environment Configuration](docs/development/environment.md) for the complete list of available settings.

---

# Start Infrastructure

Start PostgreSQL, Redis, the Flask application, and the Celery worker.

```bash
docker compose \
    -f docker/compose.yaml \
    -f docker/compose.app.yaml up -d
```

On the first startup, the embedding model configured by the application will be downloaded automatically. This may take a few minutes depending on your internet connection.

---

# Apply Database Migrations

Apply the latest database schema.

**Local**

```bash
flask db upgrade
```

**Docker**

```bash
docker compose -f docker/compose.yaml -f docker/compose.app.yaml exec app flask db upgrade
```

>[!INFO]
> For locally running migrations set the postgres and redis host to localhost in `.env`.

---

### Seed exam blueprints

Import the built-in exam blueprints (JEE, NEET, SAT, CAT, CUET, etc.) into the database.

**Local**

```bash
flask seed-exam-blueprints
```

**Docker**

```bash
docker compose -f docker/compose.yaml -f docker/compose.app.yaml exec app flask seed-exam-blueprints
```

> [!INFO]
> Change the postgres and redis host to localhost in `.env` for local sedding.

---

# Verify the Installation

After the containers become healthy and the migrations complete, the backend is ready to use.

The API is available at:

```
http://localhost:5000
```

---

# Stopping the Application

Stop all running containers.

```bash
docker compose \
    -f docker/compose.yaml \
    -f docker/compose.app.yaml down
```

To additionally remove Docker volumes:

```bash
docker compose \
    -f docker/compose.yaml \
    -f docker/compose.app.yaml down -v
```

---

# Next Steps

After the backend is running, the following documents provide more detailed information:

- [Backend Architecture](docs/architecture/Backend.md)
- [API Documentation](docs/api/Infrastructure.md)
- [Docker Deployment](docs/deployment/Docker.md)
- [Testing Guide](docs/development/Testing.md)