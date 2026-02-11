# Django REST Framework - Theory

## 1. Introduction to Django REST Framework (DRF)

### What is Django REST Framework?
Django REST Framework is a powerful and flexible toolkit for building Web APIs in Django. It provides a comprehensive set of features for creating RESTful APIs quickly and efficiently.

### Why Use DRF?
- **Serialization**: Powerful serialization engine for converting complex data types
- **Authentication**: Built-in authentication classes (Session, Token, JWT)
- **Permissions**: Granular permission system
- **Browsable API**: Interactive web-based interface for testing
- **ViewSets & Routers**: Automatic URL routing
- **Pagination**: Built-in pagination support
- **Filtering & Searching**: Easy data filtering

### Installation
```bash
pip install djangorestframework
```

### Basic Setup
```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

---

## 2. Serializers

### What are Serializers?
Serializers allow complex data (querysets, model instances) to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types. They also provide deserialization for parsing data back to complex types.

### Types of Serializers

#### 1. Serializer (Base Class)
Most flexible, manual field definition.

```python
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    age = serializers.IntegerField()
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
```

#### 2. ModelSerializer
Automatically generates fields based on the model.

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'age']
        # Or use '__all__' for all fields
        # fields = '__all__'
        
        # Exclude specific fields
        # exclude = ['password']
        
        # Read-only fields
        read_only_fields = ['id', 'created_at']
        
        # Extra kwargs for field customization
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
```

### Field Types
```python
# Common field types
serializers.CharField()
serializers.EmailField()
serializers.URLField()
serializers.IntegerField()
serializers.FloatField()
serializers.DecimalField(max_digits=5, decimal_places=2)
serializers.BooleanField()
serializers.DateField()
serializers.DateTimeField()
serializers.TimeField()
serializers.ChoiceField(choices=['option1', 'option2'])
serializers.JSONField()

# Relational fields
serializers.PrimaryKeyRelatedField(queryset=Model.objects.all())
serializers.StringRelatedField()
serializers.SlugRelatedField(slug_field='slug', queryset=Model.objects.all())
serializers.HyperlinkedRelatedField(view_name='model-detail', queryset=Model.objects.all())
```

### Nested Serializers
```python
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'country']

class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'address']
```

### Validation
```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'age']
    
    # Field-level validation
    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError("Age must be at least 18")
        return value
    
    # Object-level validation
    def validate(self, data):
        if data['username'] == data['email']:
            raise serializers.ValidationError("Username and email cannot be same")
        return data
```

---

## 3. Views

### Function-Based Views (FBVs)
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Class-Based Views (APIView)
```python
from rest_framework.views import APIView

class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Generic Views
DRF provides pre-built generic views for common patterns.

```python
from rest_framework import generics

# List and Create
class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Retrieve, Update, Delete
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

**Available Generic Views:**
- `ListAPIView` - Read-only list
- `CreateAPIView` - Create only
- `RetrieveAPIView` - Read-only single instance
- `UpdateAPIView` - Update only
- `DestroyAPIView` - Delete only
- `ListCreateAPIView` - List and create
- `RetrieveUpdateAPIView` - Read and update
- `RetrieveDestroyAPIView` - Read and delete
- `RetrieveUpdateDestroyAPIView` - Read, update, delete

---

## 4. ViewSets

### What are ViewSets?
ViewSets combine the logic for multiple related views into a single class.

### ModelViewSet
```python
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`,
    `update()`, `partial_update()`, `destroy()` and `list()` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # Custom action
    from rest_framework.decorators import action
    
    @action(detail=False, methods=['get'])
    def recent_users(self, request):
        recent = User.objects.order_by('-created_at')[:10]
        serializer = self.get_serializer(recent, many=True)
        return Response(serializer.data)
```

### ReadOnlyModelViewSet
Provides only list() and retrieve() actions.

```python
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

---

## 5. Routers

### Automatic URL Routing
```python
# urls.py
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
]
```

**Generated URLs:**
- `GET /api/users/` - List
- `POST /api/users/` - Create
- `GET /api/users/{id}/` - Retrieve
- `PUT /api/users/{id}/` - Update
- `PATCH /api/users/{id}/` - Partial Update
- `DELETE /api/users/{id}/` - Delete

---

## 6. Authentication

### Types of Authentication

#### 1. Session Authentication
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ]
}
```

#### 2. Token Authentication
```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# Migrate to create token table
python manage.py migrate
```

#### 3. JWT Authentication (Third-party)
```bash
pip install djangorestframework-simplejwt
```

---

## 7. Permissions

### Built-in Permission Classes
```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
```

**Available Permissions:**
- `AllowAny` - No restrictions
- `IsAuthenticated` - Authenticated users only
- `IsAdminUser` - Admin users only  
- `IsAuthenticatedOrReadOnly` - Read for all, write for authenticated

### Custom Permissions
```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```

---

## 8. Pagination

### Page Number Pagination
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

### Limit Offset Pagination
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}
```

---

## 9. Filtering

### Django Filter Backend
```bash
pip install django-filter
```

```python
from django_filters.rest_framework import DjangoFilterBackend

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'email']
```

### Search Filter
```python
from rest_framework.filters import SearchFilter

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email']
```

---

## 10. Best Practices

1. **Use ModelSerializer** for model-based APIs
2. **Use ViewSets with Routers** for standard CRUD operations
3. **Implement proper permissions** on all endpoints
4. **Use pagination** for list endpoints
5. **Add filtering and searching** for better UX
6. **Write tests** for all API endpoints
7. **Use throttling** to prevent abuse
8. **Version your API** from the start
9. **Document your API** using tools like drf-spectacular
10. **Handle errors consistently** with custom exception handlers
