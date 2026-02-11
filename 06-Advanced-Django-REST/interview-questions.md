# Advanced Django REST Framework - Interview Questions & Answers

## 1. What is the difference between GenericAPIView and APIView?
**Answer**: APIView provides the base functionality for handling HTTP requests but requires manual implementation of all methods. GenericAPIView extends APIView and provides commonly used attributes like `queryset`, `serializer_class`, and methods like `get_object()`, `get_queryset()`, making it easier to work with database models. GenericAPIView is typically used with mixins to create generic views.

## 2. Explain ViewSets and their advantages.
**Answer**: ViewSets combine the logic for multiple related views (list, create, retrieve, update, destroy) into a single class. Advantages include:
- **Less code**: One class handles all CRUD operations
- **Automatic routing**: Works seamlessly with routers
- **Consistency**: Standard operations follow consistent patterns
- **Custom actions**: Easy to add custom endpoints with `@action` decorator
- **Cleaner code organization**: Related functionality grouped together

## 3. What are the different types of ViewSets in DRF?
**Answer**:
- **ViewSet**: Base class with no actions, define your own
- **GenericViewSet**: Inherits GenericAPIView, provides get_object/get_queryset, no default actions
- **ModelViewSet**: Full CRUD (list, create, retrieve, update, partial_update, destroy)
- **ReadOnlyModelViewSet**: Only list and retrieve operations
You can also create custom ViewSets by mixing GenericViewSet with specific mixins.

## 4. What is the purpose of Routers in DRF?
**Answer**: Routers automatically generate URL patterns for ViewSets, eliminating the need to manually define URLs for each action. They provide:
- **Automatic URL generation**: Creates standard RESTful URLs
- **Consistency**: Ensures URL patterns follow conventions
- **Less code**: No need to manually wire up URLs
- **SimpleRouter**: Basic routing
- **DefaultRouter**: Adds API root view and format suffixes

## 5. How do you implement custom actions in ViewSets?
**Answer**: Use the `@action` decorator:
```python
@action(detail=True, methods=['post', 'get'])
def custom_action(self, request, pk=None):
    # detail=True: /resource/{id}/custom_action/
    # detail=False: /resource/custom_action/
    obj = self.get_object()
    # Custom logic here
    return Response({'status': 'success'})
```
The `detail` parameter determines if the action applies to a single object (True) or the collection (False).

## 6. Explain permission classes in DRF and how they work.
**Answer**: Permission classes determine whether a request should be granted or denied access. DRF checks permissions at two levels:
- **View-level**: Checked before calling the handler method
- **Object-level**: Checked when accessing specific objects

Built-in classes include:
- `AllowAny`: No restrictions
- `IsAuthenticated`: Authenticated users only
- `IsAdminUser`: Admin/staff users only
- `IsAuthenticatedOrReadOnly`: Authenticated for write, anyone for read

Custom permissions inherit from `BasePermission` and implement `has_permission()` and/or `has_object_permission()`.

## 7. What are Mixins in DRF and how are they used?
**Answer**: Mixins provide reusable behavior that can be composed with GenericAPIView:
- **ListModelMixin**: Provides `list()` method
- **CreateModelMixin**: Provides `create()` method
- **RetrieveModelMixin**: Provides `retrieve()` method
- **UpdateModelMixin**: Provides `update()` and `partial_update()` methods
- **DestroyModelMixin**: Provides `destroy()` method

Example:
```python
class UserListCreate(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
```

## 8. How do you implement filtering in DRF?
**Answer**: DRF supports multiple filtering backends:
1. **DjangoFilterBackend**: Complex filtering using django-filter
```python
filter_backends = [DjangoFilterBackend]
filterset_fields = ['username', 'email']
```

2. **SearchFilter**: Simple search across fields
```python
filter_backends = [SearchFilter]
search_fields = ['username', 'email']
```

3. **OrderingFilter**: Allow result ordering
```python
filter_backends = [OrderingFilter]
ordering_fields = ['date_joined', 'username']
```

## 9. What is the difference between SimpleRouter and DefaultRouter?
**Answer**:
- **SimpleRouter**: 
  - Basic routing functionality
  - Generates standard CRUD URLs
  - No API root view

- **DefaultRouter**:
  - Extends SimpleRouter
  - Adds API root view (browsable API homepage)
  - Adds format suffixes (.json, .api)
  - Provides more features for API exploration

## 10. How do you implement custom permission classes?
**Answer**: Create a class inheriting from `BasePermission`:
```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for owner
        return obj.owner == request.user
```

Permissions can check:
- Request method
- User authentication status
- User role/group
- Object ownership
- Custom business logic

## 11. Explain the lifecycle of a DRF request with ViewSets and Routers.
**Answer**: 
1. **URL Routing**: Router matches URL pattern to ViewSet action
2. **Dispatch**: Request is dispatched to the appropriate ViewSet method
3. **Authentication**: Authenticates the user
4. **Permissions**: Checks view-level permissions
5. **Throttling**: Applies rate limiting
6. **Content Negotiation**: Determines response format
7. **Action Method**: Executes the ViewSet action (list, retrieve, etc.)
8. **Serialization**: Serializes the data
9. **Object Permissions**: Checks object-level permissions (if applicable)
10. **Response**: Returns the formatted response

## 12. How do you handle nested routes in DRF?
**Answer**: While DRF doesn't have built-in nested routing, you can:
1. **Use drf-nested-routers package**:
```python
from rest_framework_nested import routers
router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'posts', PostViewSet)
```

2. **Custom ViewSet with filtered querysets**:
```python
class PostViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user_id = self.kwargs.get('user_pk')
        return Post.objects.filter(user_id=user_id)
```

## 13. What are the best practices for organizing DRF views?
**Answer**:
1. **Use ViewSets for standard CRUD**: Less code, automatic routing
2. **Use Generic Views for simple endpoints**: When you need specific operations
3. **Use APIView for complex logic**: Full control when needed
4. **Keep views thin**: Move business logic to models/services
5. **Use mixins for reusability**: Compose behavior as needed
6. **Implement proper permissions**: Secure all endpoints
7. **Use action decorators**: For custom ViewSet actions
8. **Override get_queryset**: For dynamic filtering
9. **Document endpoints**: Use docstrings and schema generation
10. **Follow RESTful conventions**: Proper HTTP methods and status codes
