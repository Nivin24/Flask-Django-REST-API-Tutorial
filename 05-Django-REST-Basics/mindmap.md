# Django REST Framework (DRF) Mind Map

## 1. Core Components
- **Serializers**: Data conversion (Model <-> JSON).
- **Views**: APIView, GenericViews, ViewSets.
- **Routers**: URL pattern generation.
- **Request/Response**: Wrappers for standard Django objects.

## 2. Request Lifecycle
1. **URL Dispatcher**: Matches request to a view.
2. **Middleware**: Standard Django middleware processing.
3. **Authentication**: Identifies the user.
4. **Permissions**: Checks if user is authorized.
5. **Throttling**: Rate limiting.
6. **View Logic**: Processes data.
7. **Serializer**: Formats output.
8. **Response**: Returns data to client.

## 3. Serialization
- **Serializer Class**: Base class.
- **ModelSerializer**: For Django models.
- **Validation**:
    - Field-level.
    - Object-level.
    - Custom validators.

## 4. Views & Logic
- **Function Based Views (FBV)**: `@api_view`.
- **Class Based Views (CBV)**: `APIView`.
- **Generic Views**: `ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`, etc.
- **ViewSets**: `ModelViewSet`, `ReadOnlyModelViewSet`.

## 5. Security & Auth
- **Auth Types**: Token, Session, JWT (SimpleJWT), Basic.
- **Permissions**: IsAuthenticated, IsAdminUser, AllowAny, Custom Permissions.

## 6. Optimization & Utilities
- **Pagination**: PageNumber, LimitOffset, Cursor.
- **Filtering**: DjangoFilterBackend, SearchFilter, OrderingFilter.
- **Throttling**: AnonRateThrottle, UserRateThrottle.
- **Versioning**: URLPathVersioning, QueryParameterVersioning.
