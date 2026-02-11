# Flask Todo API - Project Guide

## 📋 Overview

A complete REST API for managing todo items built with Flask. This project demonstrates CRUD operations, data validation, error handling, and best practices for Flask API development.

## 🎯 Learning Objectives

- Implement complete CRUD operations
- Handle HTTP methods (GET, POST, PUT, DELETE)
- Validate request data
- Implement proper error handling
- Structure a Flask API project
- Test API endpoints

## 🛠️ Tech Stack

- **Framework**: Flask 3.0+
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: Flask-SQLAlchemy
- **Authentication**: Flask-JWT-Extended
- **Validation**: Flask-Marshmallow
- **Testing**: pytest

## 📁 Project Structure

```
flask-todo-api/
│
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # Database models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── todos.py         # Todo endpoints
│   │   └── auth.py          # Authentication endpoints
│   ├── schemas.py           # Marshmallow schemas
│   ├── utils.py             # Helper functions
│   └── config.py            # Configuration
│
├── tests/
│   ├── __init__.py
│   ├── test_todos.py
│   └── test_auth.py
│
├── migrations/              # Database migrations
├── requirements.txt
├── .env.example
├── run.py                   # Application entry point
└── README.md
```

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8+
pip
virtualenv (recommended)
```

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd flask-todo-api
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Run the application**:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## 📚 API Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "user123",
  "email": "user@example.com",
  "password": "securepass123"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com"
  }
}
```

### Todo Operations

#### Get All Todos
```http
GET /api/todos
Authorization: Bearer <access_token>

Response:
{
  "todos": [
    {
      "id": 1,
      "title": "Complete project",
      "description": "Finish Flask API project",
      "completed": false,
      "created_at": "2026-02-11T10:00:00Z"
    }
  ],
  "total": 1
}
```

#### Get Single Todo
```http
GET /api/todos/{id}
Authorization: Bearer <access_token>
```

#### Create Todo
```http
POST /api/todos
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "New Task",
  "description": "Task description",
  "completed": false
}
```

#### Update Todo
```http
PUT /api/todos/{id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated Task",
  "description": "Updated description",
  "completed": true
}
```

#### Delete Todo
```http
DELETE /api/todos/{id}
Authorization: Bearer <access_token>
```

## 💾 Database Models

### User Model
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Todo Model
```python
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
```

## 🧪 Testing

### Run Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=app tests/
```

### Test Examples
```python
def test_create_todo(client, auth_headers):
    response = client.post(
        '/api/todos',
        json={'title': 'Test Todo', 'description': 'Test'},
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json['title'] == 'Test Todo'
```

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Protected routes requiring authentication
- Input validation and sanitization
- CORS configuration
- Rate limiting

## 📝 Error Handling

The API returns consistent error responses:

```json
{
  "error": "Not Found",
  "message": "Todo with id 99 not found",
  "status": 404
}
```

## 🚦 Status Codes

- `200 OK` - Successful GET/PUT request
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## 🔧 Configuration

### Environment Variables
```bash
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///todos.db
CORS_ORIGINS=http://localhost:3000
```

## 📦 Dependencies

```txt
Flask==3.0.0
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.5
Flask-JWT-Extended==4.5.3
Flask-Marshmallow==0.15.0
marshmallow-sqlalchemy==0.29.0
Flask-CORS==4.0.0
bcrypt==4.1.2
python-dotenv==1.0.0
pytest==7.4.3
pytest-cov==4.1.0
```

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [REST API Best Practices](https://restfulapi.net/)

## 🐛 Troubleshooting

### Common Issues

1. **Database connection errors**
   - Check DATABASE_URL in .env
   - Ensure database migrations are up to date

2. **JWT token errors**
   - Verify JWT_SECRET_KEY is set
   - Check token expiration settings

3. **CORS errors**
   - Configure CORS_ORIGINS properly
   - Add allowed origins in config

## 🚀 Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Using Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## 📈 Future Enhancements

- [ ] Add pagination for todo list
- [ ] Implement filtering and sorting
- [ ] Add todo categories/tags
- [ ] Implement todo sharing between users
- [ ] Add due dates and reminders
- [ ] Create API documentation with Swagger
- [ ] Add file attachments to todos
- [ ] Implement search functionality

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

**Nivin Benny**
- GitHub: [@Nivin24](https://github.com/Nivin24)

---

**Happy Coding! 🚀**
