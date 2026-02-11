# Advanced Django REST Framework - Mind Map

## Central Concept: Advanced DRF
Building scalable, maintainable REST APIs with advanced patterns

## 1. Views Architecture

### Class-Based Views
- **APIView**: Manual control, basic HTTP methods
- **Generic Views**: Pre-built patterns
  - ListAPIView
  - CreateAPIView
  - RetrieveAPIView
  - UpdateAPIView
  - DestroyAPIView
  - Combined: ListCreateAPIView, RetrieveUpdateDestroyAPIView

### ViewSets
- **Types**:
  - ViewSet (base)
  - GenericViewSet (with mixins)
  - ModelViewSet (full CRUD)
  - ReadOnlyModelViewSet
- **Benefits**:
  - Less code
  - Automatic routing
  - Custom actions (@action decorator)
  - Consistent patterns

## 2. Routing System

### Router Types
- **SimpleRouter**: Basic URL generation
- **DefaultRouter**: Adds API root + format suffixes

### URL Patterns Generated
```
/resource/                    → list, create
/resource/{pk}/              → retrieve, update, destroy
/resource/{pk}/custom_action/ → custom actions
```

### Custom Actions
- `detail=True`: Single object (/resource/{pk}/action/)
- `detail=False`: Collection (/resource/action/)
- Methods: GET, POST, PUT, PATCH, DELETE

## 3. Permissions System

### Permission Hierarchy
1. **Global**: Settings.py (REST_FRAMEWORK)
2. **View-level**: permission_classes
3. **Object-level**: has_object_permission()

### Built-in Permissions
- **AllowAny**: No restrictions
- **IsAuthenticated**: Requires login
- **IsAdminUser**: Staff only
- **IsAuthenticatedOrReadOnly**: Read for all, write for authenticated

### Custom Permissions
```python
class IsOwnerOrReadOnly(BasePermission):
    - has_permission()
    - has_object_permission()
```

## 4. Mixins Pattern

### Available Mixins
- **ListModelMixin**: List queryset
- **CreateModelMixin**: Create instance
- **RetrieveModelMixin**: Get single object
- **UpdateModelMixin**: Update instance
- **DestroyModelMixin**: Delete instance

### Composition
```
GenericAPIView + Mixins = Custom View
Example: ListModelMixin + CreateModelMixin + GenericAPIView
```

## 5. Request Flow

### Lifecycle
1. **URL Dispatch**: Router → ViewSet
2. **Initialize**: View setup
3. **Authenticate**: Identify user
4. **Check Permissions**: View-level
5. **Throttle**: Rate limiting
6. **Parse Request**: Content negotiation
7. **Execute Action**: ViewSet method
8. **Serialize**: Format response
9. **Object Permissions**: (if applicable)
10. **Return Response**: HTTP response

## 6. Filtering & Search

### Filter Backends
- **DjangoFilterBackend**:
  - Complex field filtering
  - Requires django-filter package
  - filterset_fields / filterset_class

- **SearchFilter**:
  - Simple search
  - search_fields
  - Query param: ?search=query

- **OrderingFilter**:
  - Client-controlled ordering
  - ordering_fields
  - Query param: ?ordering=field

## 7. Advanced Patterns

### Queryset Optimization
- Override `get_queryset()`
- select_related() for ForeignKey
- prefetch_related() for M2M
- Filter based on user/permissions

### Action Decorators
```python
@action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
- Custom endpoints
- Per-action permissions
- URL kwargs access
```

### Nested Resources
- drf-nested-routers package
- Custom queryset filtering
- Parent-child relationships

## 8. Best Practices

### View Organization
1. **Standard CRUD** → ModelViewSet
2. **Specific Operations** → Generic Views
3. **Complex Logic** → APIView
4. **Reusable Behavior** → Mixins

### Security
- Always set permissions
- Use object-level permissions for ownership
- Validate user access in get_queryset()
- Implement throttling for public endpoints

### Performance
- Optimize querysets (select_related, prefetch_related)
- Implement pagination
- Use caching where appropriate
- Monitor N+1 queries

### Code Quality
- Keep views thin
- Business logic in models/services
- Consistent naming
- Document with docstrings
- Use type hints
- Write tests

## 9. Common Use Cases

### Public Read, Authenticated Write
```
permission_classes = [IsAuthenticatedOrReadOnly]
```

### Owner-Only Modification
```
Custom permission: IsOwnerOrReadOnly
Object-level permission check
```

### Admin-Only Actions
```
@action(permission_classes=[IsAdminUser])
```

### Filtered Querysets
```
def get_queryset(self):
    return Model.objects.filter(user=self.request.user)
```

## Summary

**Advanced DRF Provides**:
- **Abstraction Levels**: APIView → Generic Views → ViewSets
- **Automatic Routing**: Routers for ViewSets
- **Fine-grained Security**: Multiple permission levels
- **Reusable Components**: Mixins for composition
- **Flexible Filtering**: Multiple backend options
- **Scalable Architecture**: Clean, maintainable code patterns
