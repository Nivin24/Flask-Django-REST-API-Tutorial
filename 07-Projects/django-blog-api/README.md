# Django Blog API - Project Guide

## 📋 Overview

A comprehensive Blog REST API built with Django REST Framework. This project demonstrates advanced DRF features including serializers, ViewSets, permissions, filtering, and relationships between models.

## 🎯 Learning Objectives

- Master Django REST Framework concepts
- Implement nested serializers and relationships
- Handle complex permissions and authentication
- Implement filtering, searching, and pagination
- Work with ViewSets and Routers
- Upload and manage media files

## 🛠️ Tech Stack

- **Framework**: Django 5.0+ with Django REST Framework
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Media Storage**: Django Storage / AWS S3
- **Testing**: pytest with pytest-django
- **Documentation**: drf-yasg (Swagger/OpenAPI)

## 📁 Project Structure

```
django-blog-api/
│
├── blog_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── posts/
│   ├── __init__.py
│   ├── models.py              # Post, Comment, Category models
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # ViewSets
│   ├── permissions.py         # Custom permissions
│   ├── filters.py             # Custom filters
│   ├── urls.py
│   └── admin.py
│
├── users/
│   ├── __init__.py
│   ├── models.py              # Custom User model
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── media/                     # User-uploaded files
├── static/                    # Static files
├── tests/
│   ├── test_posts.py
│   ├── test_comments.py
│   └── test_auth.py
│
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.10+
PostgreSQL (optional for development)
pip
virtualenv
```

### Installation

1. **Clone and setup**:
```bash
git clone <repository-url>
cd django-blog-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Database setup**:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

5. **Run development server**:
```bash
python manage.py runserver
```

API will be available at `http://localhost:8000/api/`

## 📚 API Endpoints

### Base URL: `/api/v1/`

### Authentication

```http
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
POST /api/auth/token/refresh/
GET  /api/auth/user/
```

### Posts

```http
GET    /api/posts/              # List all posts (with pagination)
POST   /api/posts/              # Create new post
GET    /api/posts/{id}/         # Get single post
PUT    /api/posts/{id}/         # Update post
PATCH  /api/posts/{id}/         # Partial update
DELETE /api/posts/{id}/         # Delete post
GET    /api/posts/{id}/comments/ # Get post comments
POST   /api/posts/{id}/like/    # Like/unlike post
```

### Comments

```http
GET    /api/comments/           # List all comments
POST   /api/comments/           # Create comment
GET    /api/comments/{id}/      # Get comment
PUT    /api/comments/{id}/      # Update comment
DELETE /api/comments/{id}/      # Delete comment
```

### Categories

```http
GET    /api/categories/         # List categories
POST   /api/categories/         # Create category
GET    /api/categories/{id}/    # Get category
GET    /api/categories/{id}/posts/ # Get posts in category
```

### Users

```http
GET    /api/users/              # List users
GET    /api/users/{id}/         # Get user profile
GET    /api/users/{id}/posts/   # Get user's posts
PUT    /api/users/profile/      # Update own profile
```

## 💾 Database Models

### User Model (Extended)
```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True)
    following = models.ManyToManyField('self', symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Post Model
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    featured_image = models.ImageField(upload_to='posts/')
    status = models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')])
    likes = models.ManyToManyField(User, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Comment Model
```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True)  # For nested comments
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## 🔐 Authentication & Permissions

### JWT Authentication
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

### Custom Permissions
```python
class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
```

## 🔍 Filtering & Search

### Query Parameters
```http
# Filtering
GET /api/posts/?category=technology&status=published

# Searching
GET /api/posts/?search=django+tutorial

# Ordering
GET /api/posts/?ordering=-created_at

# Pagination
GET /api/posts/?page=2&page_size=10
```

### Implementation
```python
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status', 'author']
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'likes']
    pagination_class = PageNumberPagination
```

## 🧪 Testing

### Run Tests
```bash
pytest
pytest --cov=. --cov-report=html
```

### Test Example
```python
def test_create_post(api_client, authenticated_user):
    data = {
        'title': 'Test Post',
        'content': 'Test content',
        'status': 'published'
    }
    response = api_client.post('/api/posts/', data)
    assert response.status_code == 201
    assert Post.objects.filter(title='Test Post').exists()
```

## 📖 API Documentation

Access interactive API documentation:

- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`

## 🔧 Advanced Features

### Nested Serializers
```python
class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = '__all__'
```

### Custom Actions
```python
@action(detail=True, methods=['post'])
def like(self, request, pk=None):
    post = self.get_object()
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return Response({'status': 'unliked'})
    post.likes.add(request.user)
    return Response({'status': 'liked'})
```

### Signals
```python
@receiver(post_save, sender=Post)
def create_post_notification(sender, instance, created, **kwargs):
    if created:
        # Send notification to followers
        pass
```

## 🚀 Deployment

### Using Gunicorn + Nginx
```bash
gunicorn blog_api.wsgi:application --bind 0.0.0.0:8000
```

### Docker Setup
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "blog_api.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 📦 Dependencies

```txt
Django==5.0.1
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
django-filter==23.5
drf-yasg==1.21.7
Pillow==10.2.0
psycopg2-binary==2.9.9
python-decouple==3.8
gunicorn==21.2.0
pytest==7.4.4
pytest-django==4.7.0
```

## 🎓 Learning Resources

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Documentation](https://docs.djangoproject.com/)
- [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)
- [Testing in DRF](https://www.django-rest-framework.org/api-guide/testing/)

## 📈 Future Enhancements

- [ ] Add tagging system for posts
- [ ] Implement bookmarks/saved posts
- [ ] Add email notifications
- [ ] Implement real-time comments (WebSockets)
- [ ] Add social media sharing
- [ ] Implement markdown support
- [ ] Add post analytics and views tracking
- [ ] Create RSS feed
- [ ] Add image optimization
- [ ] Implement rate limiting

## 🐛 Troubleshooting

### Common Issues

1. **Database errors**: Ensure PostgreSQL is running and credentials are correct
2. **Media files not loading**: Check MEDIA_URL and MEDIA_ROOT settings
3. **JWT errors**: Verify SECRET_KEY and token expiration settings
4. **CORS issues**: Configure django-cors-headers properly

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

**Nivin Benny**
- GitHub: [@Nivin24](https://github.com/Nivin24)

---

**Happy Coding! 🚀**
