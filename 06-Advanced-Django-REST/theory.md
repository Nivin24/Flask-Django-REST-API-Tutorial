# Advanced Django REST Framework - Theory

This module covers advanced topics in Django REST Framework including class-based views, viewsets, routers, and permissions.

## 1. Class-Based Views (CBV) in DRF

### Generic Views
DRF provides several generic class-based views that implement common patterns:

#### ListAPIView
- **Purpose**: Read-only endpoint for a collection of model instances
- **Methods**: GET (list)
- **Use Case**: Display all objects

#### CreateAPIView
- **Purpose**: Create-only endpoint
- **Methods**: POST
- **Use Case**: Create new objects

#### RetrieveAPIView
- **Purpose**: Read-only endpoint for a single model instance
- **Methods**: GET (retrieve)
- **Use Case**: Display single object details

#### UpdateAPIView
- **Purpose**: Update-only endpoint
- **Methods**: PUT, PATCH
- **Use Case**: Update existing objects

#### DestroyAPIView
- **Purpose**: Delete-only endpoint
- **Methods**: DELETE
- **Use Case**: Delete objects

#### Combined Generic Views
- **ListCreateAPIView**: List + Create
- **RetrieveUpdateAPIView**: Retrieve + Update
- **RetrieveDestroyAPIView**: Retrieve + Delete
- **RetrieveUpdateDestroyAPIView**: Retrieve + Update + Delete

### APIView vs Generic Views
- **APIView**: Full control, manual implementation
- **Generic Views**: Pre-built logic, less code, faster development

## 2. ViewSets

ViewSets combine the logic for multiple related views into a single class.

### Types of ViewSets

#### ViewSet
- Base class with no actions by default
- Define your own actions using `@action` decorator

#### GenericViewSet
- Inherits from GenericAPIView
- Provides get_object(), get_queryset()
- No default actions, combine with mixins

#### ModelViewSet
- Full CRUD operations automatically
- Actions: list(), create(), retrieve(), update(), partial_update(), destroy()
- Most commonly used

#### ReadOnlyModelViewSet
- Only read operations
- Actions: list(), retrieve()
- Use for read-only APIs

### Custom Actions
```python
@action(detail=True, methods=['post'])
def custom_action(self, request, pk=None):
    # detail=True means /resource/{id}/custom_action/
    # detail=False means /resource/custom_action/
    pass
```

## 3. Routers

Routers automatically generate URL patterns for ViewSets.

### SimpleRouter
- Basic routing
- Generates: list, create, retrieve, update, partial_update, destroy

### DefaultRouter
- Extends SimpleRouter
- Adds API root view (browsable API)
- Adds format suffixes (.json)

### Router Usage
```python
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls
```

### URL Patterns Generated
- `/users/` - list, create
- `/users/{pk}/` - retrieve, update, destroy
- `/users/{pk}/custom_action/` - custom actions

## 4. Permissions

Permissions determine whether a request should be granted or denied access.

### Built-in Permission Classes

#### AllowAny
- Unrestricted access
- Default if no permission classes specified

#### IsAuthenticated
- Only authenticated users
- Common for protected APIs

#### IsAdminUser
- Only admin/staff users
- `user.is_staff == True`

#### IsAuthenticatedOrReadOnly
- Authenticated users: full access
- Anonymous users: read-only (GET, HEAD, OPTIONS)

### Custom Permissions
Create custom permission classes by subclassing `BasePermission`:

```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```

### Permission Levels
- **Global**: Applied to all views via settings
- **View-level**: Set on view/viewset class
- **Object-level**: Check permissions on specific objects

## 5. Mixins

Mixins provide reusable behavior for views:

- **ListModelMixin**: List a queryset
- **CreateModelMixin**: Create a model instance
- **RetrieveModelMixin**: Retrieve a model instance
- **UpdateModelMixin**: Update a model instance
- **DestroyModelMixin**: Delete a model instance

Combine mixins with GenericAPIView to create custom views:
```python
class UserListCreate(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

## 6. Filtering, Searching, and Ordering

### DjangoFilterBackend
- Filter querysets based on model fields
- Requires `django-filter` package

### SearchFilter
- Simple search based on single query parameter
- Searches across multiple fields

### OrderingFilter
- Allow clients to control result ordering
- Specify allowed ordering fields

## 7. Best Practices

1. **Use ViewSets** for standard CRUD operations
2. **Use Generic Views** for simple, specific endpoints
3. **Use APIView** when you need full control
4. **Set appropriate permissions** on all views
5. **Use routers** for consistent URL patterns
6. **Implement custom actions** for business logic
7. **Override queryset** methods for filtering
8. **Use pagination** for large datasets
9. **Implement proper error handling**
10. **Document your API** using schema generation

## Summary

Advanced Django REST Framework provides powerful abstractions:
- **Generic Views**: Quick implementation of common patterns
- **ViewSets**: Organize related views together
- **Routers**: Automatic URL configuration
- **Permissions**: Fine-grained access control
- **Mixins**: Reusable behavior components

These tools enable rapid development of robust, scalable REST APIs.
