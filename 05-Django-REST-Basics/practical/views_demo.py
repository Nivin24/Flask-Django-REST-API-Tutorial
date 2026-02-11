# views_demo.py - Django REST Framework Views Examples

"""
This file demonstrates different types of views in Django REST Framework:
- Function-Based Views (FBV) with @api_view decorator
- APIView (Class-Based Views)
- Generic Views (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
- ViewSets (ModelViewSet, ReadOnlyModelViewSet)
"""

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView, 
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework import serializers


# Sample serializer for demo purposes
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


# ==================== Example 1: Function-Based View ====================
@api_view(['GET', 'POST'])
def user_list_fbv(request):
    """
    Function-based view to list all users or create a new user.
    GET: List all users
    POST: Create a new user
    """
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


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_fbv(request, pk):
    """
    Function-based view to retrieve, update, or delete a specific user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== Example 2: APIView (Class-Based) ====================
class UserListAPIView(APIView):
    """
    APIView for listing all users or creating a new user.
    """
    permission_classes = [AllowAny]  # Change as needed
    
    def get(self, request):
        """List all users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Create a new user"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    """
    APIView for retrieving, updating, or deleting a specific user.
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        """Helper method to get user by pk"""
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
    
    def get(self, request, pk):
        """Retrieve a user"""
        user = self.get_object(pk)
        if not user:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """Update a user"""
        user = self.get_object(pk)
        if not user:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Delete a user"""
        user = self.get_object(pk)
        if not user:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== Example 3: Generic Views ====================
class UserListCreateView(ListCreateAPIView):
    """
    Generic view for listing and creating users.
    Combines list() and create() functionality.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Generic view for retrieving, updating, and deleting users.
    Combines retrieve(), update(), and destroy() functionality.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# ==================== Example 4: ViewSets ====================
class UserViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet provides default `list()`, `create()`, `retrieve()`,
    `update()`, `partial_update()`, and `destroy()` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """
        Custom action to get user profile.
        Accessible at: /users/{id}/profile/
        """
        user = self.get_object()
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': f"{user.first_name} {user.last_name}".strip(),
            'is_staff': user.is_staff,
            'date_joined': user.date_joined
        })
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Custom action to get only active users.
        Accessible at: /users/active/
        """
        active_users = User.objects.filter(is_active=True)
        serializer = self.get_serializer(active_users, many=True)
        return Response(serializer.data)


class UserReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnlyModelViewSet provides only `list()` and `retrieve()` actions.
    No create, update, or delete operations.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# ==================== URL Configuration Examples ====================
"""
# In urls.py:

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# For ViewSets, use routers
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'users-readonly', views.UserReadOnlyViewSet, basename='user-readonly')

urlpatterns = [
    # Function-Based Views
    path('fbv/users/', views.user_list_fbv, name='user-list-fbv'),
    path('fbv/users/<int:pk>/', views.user_detail_fbv, name='user-detail-fbv'),
    
    # APIView
    path('apiview/users/', views.UserListAPIView.as_view(), name='user-list-apiview'),
    path('apiview/users/<int:pk>/', views.UserDetailAPIView.as_view(), name='user-detail-apiview'),
    
    # Generic Views
    path('generic/users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('generic/users/<int:pk>/', views.UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    
    # ViewSets (via router)
    path('', include(router.urls)),
]
"""
