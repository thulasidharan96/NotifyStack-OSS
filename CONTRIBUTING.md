# Contributing to NotifyStack-OSS

First of all, thank you for your interest in contributing to NotifyStack-OSS! As an open-source notification service, we welcome contributions from everyone.

## Getting Started

### Prerequisites
- **Python 3.13+**
- **uv**: Python package installer and resolver.
- **Docker & Docker Compose**: For infrastructure services.

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/notifystack-oss.git
   cd notifystack-oss
   ```

2. **Start the Infrastructure Dependencies**
   Run PostgreSQL, Redis, and NATS using Docker Compose:
   ```bash
   docker compose up -d postgres redis nats
   ```

3. **Install Dependencies**
   Sync all dependencies:
   ```bash
   uv sync --all-groups
   ```

4. **Environment Variables**
   Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

5. **Run the Development Server**
   ```bash
   uv run uvicorn app.main:app --app-dir backend --reload
   ```

## Development Workflow

1. **Create a branch**: `git checkout -b feature/your-feature-name`
2. **Make your changes**: Write your code and ensure it follows the project's standards.
3. **Run tests**:
   ```bash
   uv run pytest backend/tests
   ```
4. **Run linters and type checkers**:
   ```bash
   uv run ruff check backend/
   uv run mypy backend/
   ```
5. **Commit your changes**: Ensure your commit messages are descriptive.
6. **Push to your fork and submit a Pull Request**.

## Guidelines
- Follow PEP 8 style guidelines.
- Add tests for any new features or bug fixes.
- Ensure all existing tests pass before submitting your PR.
- Keep PRs focused on a single issue or feature.