# Permissions Example - Advanced Django REST Framework

from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

# 1. Built-in Permission Classes

# AllowAny - Allow unrestricted access
from rest_framework.permissions import AllowAny

class PublicViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

# IsAuthenticated - Only authenticated users
from rest_framework.permissions import IsAuthenticated

class PrivateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

# IsAdminUser - Only admin users
from rest_framework.permissions import IsAdminUser

class AdminViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

# IsAuthenticatedOrReadOnly - Read for all, write for authenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BlogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

# 2. Custom Permission Classes

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission: only owners can edit
    """
    message = 'You must be the owner to edit this object.'
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        
        # Write permissions only for owner
        return obj.owner == request.user

class IsOwner(BasePermission):
    """
    Custom permission: only owner can access
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsSuperuserOrReadOnly(BasePermission):
    """
    Superuser can do everything, others read-only
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser

# 3. Object-level Permissions

class IsAuthorOrReadOnly(BasePermission):
    """
    Check permissions at object level
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

# 4. Multiple Permissions (AND logic)

class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    # User must be authenticated AND owner to edit

# 5. Custom Permission with Query Parameters

class HasAPIKey(BasePermission):
    """
    Check for API key in request
    """
    def has_permission(self, request, view):
        api_key = request.query_params.get('api_key')
        return api_key == 'your-secret-key'

# 6. Dynamic Permissions Based on Action

class DynamicPermissionViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        """
        Different permissions for different actions
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

# 7. Group-based Permissions

class IsInEditorGroup(BasePermission):
    """
    Check if user belongs to 'Editor' group
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Editor').exists()

# 8. Custom Permission with Error Messages

class IsPremiumUser(BasePermission):
    message = 'You need a premium subscription to access this resource.'
    
    def has_permission(self, request, view):
        return hasattr(request.user, 'subscription') and request.user.subscription.is_premium

# 9. Permission with Multiple Conditions

class CanEditPost(BasePermission):
    """
    User can edit if they are owner OR admin OR moderator
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return (
            obj.owner == request.user or
            request.user.is_staff or
            request.user.groups.filter(name='Moderator').exists()
        )
