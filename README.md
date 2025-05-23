# Event-Management

A RESTful API for managing events and users, built with Django, Django REST Framework, PostgreSQL, and Redis. Features include CRUD operations for events, user authentication with JWT, filtering, caching, and interactive API documentation via Swagger UI and Redoc.

## Features
- **Event Management**: Create, read, update, and delete events with title, description, date, location, and creator.
- **User Management**: User registration, authentication, and profile management using JWT.
- **Filtering**: Filter events by date, location, or creator using `django-filter`.
- **Caching**: Cache event data with Redis to improve performance.
- **API Documentation**: Interactive Swagger UI and Redoc documentation powered by `drf-spectacular`.
- **Debugging**: Django Debug Toolbar for development.
- **Testing**: Automated tests with `pytest` and `pytest-django`.

## Prerequisites
- **Python 3.11** (for local development)
- **Docker** and **Docker Compose** (for containerized deployment)
- **PostgreSQL** (for local development, version 15 recommended)
- **Redis** (for local development, version 7 recommended)
- **Git** (for cloning the repository)

## Installation

### Local Development
1. **Clone the repository**:
   ```bash
   git clone https://github.com/erikagayan/Event-Management.git
   cd EventManagement
   
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   
4. **Set up PostgreSQL and Redis locally**:
   - Install and start PostgreSQL:
   - Install and start Redis

5. **Create .env file**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with the following:
   ```plaintext
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=Events
   DB_USER=admin
   DB_PASSWORD=admin
   DB_HOST=localhost
   DB_PORT=5432
   REDIS_URL=redis://localhost:6379/
   ```
   Generate a `SECRET_KEY`:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(50))"

6. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   
8. **Access the API**:
   - Swagger UI: `http://127.0.0.1:8000/api/doc/swagger/`
   - Redoc: `http://127.0.0.1:8000/api/doc/redoc/`

### Docker
1. **Clone the repository** (if not already done):
   ```bash
   git clone <your-repo-url>
   cd EventManagement
   ```

2. **Create .env file**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with the following for Docker:
   ```plaintext
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=Events
   DB_USER=admin
   DB_PASSWORD=admin
   DB_HOST=postgres
   DB_PORT=5432
   REDIS_URL=redis://redis:6379/
   ```

3. **Build and run containers**:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

4. **Check container status**:
   ```bash
   docker-compose ps
   ```

5. **Access the API**:
   - Swagger UI: `http://127.0.0.1:8000/api/doc/swagger/`
   - Redoc: `http://127.0.0.1:8000/api/doc/redoc/`

## Running Tests
- **Local**:
  ```bash
  pytest -v
  ```
- **Docker**:
  ```bash
  docker-compose exec web pytest -v
  
## Example Endpoints
- **Register a user**:
  ```bash
  curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
  ```
- **Obtain JWT token**:
  ```bash
  curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
  ```
- **List events**:
  ```bash
  curl -X GET http://127.0.0.1:8000/api/events/ \
  -H "Authorization: Bearer <your-jwt-token>"
  ```
- **Filter events by date**:
  ```bash
  curl -X GET "http://127.0.0.1:8000/api/events/?date=2025-05-22" \
  -H "Authorization: Bearer <your-jwt-token>"