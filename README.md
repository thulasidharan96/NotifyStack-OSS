# NotifyStack-OSS

NotifyStack-OSS is a scalable, modular open-source notification system that allows you to easily manage and dispatch cross-channel notifications (e.g., email, SMS, push) to your users. The system leverages **FastAPI**, **PostgreSQL**, **Redis**, and **NATS** to handle reliable notification delivery, complex event routing, templating, and detailed analytics.

---

## 📖 Consumer Guide

This guide is intended for those looking to deploy and use NotifyStack-OSS as a service within their own infrastructure.

### Features
- **Multi-Tenant Architecture**: Supports multiple Organizations and Projects.
- **Provider Agnostic**: Integrate easily with your preferred delivery providers (SendGrid, Twilio, etc.).
- **Dynamic Templates**: Manage notification templates across different channels.
- **Event-Driven Workflows**: Trigger notifications automatically based on specific business events.

### Getting Started

NotifyStack-OSS runs via Docker Compose, which sets up the application along with its necessary infrastructure dependencies (PostgreSQL, Redis, and NATS).

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/notifystack-oss.git
   cd notifystack-oss
   ```

2. **Start the services**
   Using Docker Compose, spin up the entire stack:
   ```bash
   docker compose up -d
   ```
   This will start:
   - **Backend API**: The main FastAPI application available at `http://localhost:8000`.
   - **PostgreSQL**: The relational database for persistent storage.
   - **Redis**: In-memory data store for caching and rate limiting.
   - **NATS**: High-performance messaging system for reliable event delivery.

3. **Verify the installation**
   You can verify the backend is running by checking the health endpoint:
   ```bash
   curl http://localhost:8000/health
   # Expected output: {"ok": true}
   ```

### Core Concepts

To effectively use the API, it's helpful to understand the underlying data model:
1. **Organizations**: Top-level entity representing a company or team.
2. **Projects**: Logical groupings within an organization (e.g., "Production", "Staging", or different product lines).
3. **Providers**: Configuration for external delivery services (e.g., SMTP servers, SMS gateways).
4. **Templates**: The actual content to be sent, supporting dynamic variables and multiple channels.
5. **Events**: Triggers that indicate something happened in your system.
6. **Workflows**: Rules connecting Events to Templates and Providers, orchestrating when and how a notification is dispatched.

---

## 🛠 Developer Guide

This guide is for developers who want to contribute to the codebase or run the application locally for development and testing.

### Prerequisites

- **Python 3.13+**
- **uv**: Ultra-fast Python package installer and resolver.
- **Docker & Docker Compose**: For running infrastructure services.

### Local Development Setup

The backend is built with FastAPI and heavily utilizes modern Python async features. We use `uv` for dependency management.

1. **Start the Infrastructure Dependencies**
   It's recommended to run PostgreSQL, Redis, and NATS using Docker Compose while running the Python app natively for easier debugging:
   ```bash
   # Start only the dependencies
   docker compose up -d postgres redis nats
   ```

2. **Install Dependencies**
   Sync all dependencies, including development groups (pytest, ruff, mypy):
   ```bash
   uv sync --all-groups
   ```

3. **Configure Environment Variables**
   The application uses Pydantic Settings. You can configure it via environment variables prefixed with `NOTIFYSTACK_`.
   At a minimum, you must provide a strong JWT secret for authentication.

   Create a `.env` file or export them in your terminal:
   ```bash
   export NOTIFYSTACK_JWT_SECRET="your-super-secret-key-min-32-chars-long"
   export NOTIFYSTACK_DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/notifystack"
   ```

4. **Run the Development Server**
   Start the application with live-reload enabled:
   ```bash
   uv run uvicorn app.main:app --app-dir backend --reload
   ```

### Project Structure

The codebase follows a modular, domain-driven structure located in `backend/app/`:

- **`core/`**: System-wide configuration, logging, security, and telemetry.
- **`shared/`**: Common utilities, database setup, exception handlers, and middlewares (like `TenantMiddleware`).
- **`modules/`**: The core business logic, separated by domain:
  - `auth/`: Authentication and JWT handling.
  - `organizations/`, `projects/`: Multi-tenancy and scoping.
  - `events/`, `workflows/`: Event handling and routing rules.
  - `templates/`, `providers/`, `notifications/`: Message rendering and delivery mechanisms.

### Testing and Quality Assurance

We maintain strict code quality standards enforced via robust tooling.

- **Run Tests** (pytest):
  ```bash
  uv run pytest backend/tests
  ```

- **Run Linter** (ruff):
  ```bash
  uv run ruff check backend/
  ```

- **Type Checking** (mypy):
  ```bash
  uv run mypy backend/
  ```
