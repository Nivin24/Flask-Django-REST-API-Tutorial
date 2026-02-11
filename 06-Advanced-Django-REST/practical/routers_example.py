# Routers Example - Advanced Django REST Framework

from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import BookViewSet, AuthorViewSet, PublisherViewSet

# 1. DefaultRouter - Provides API root view and format suffixes
router = DefaultRouter()

# Register ViewSets with the router
# Syntax: router.register(prefix, viewset, basename)
router.register(r'books', BookViewSet, basename='book')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'publishers', PublisherViewSet, basename='publisher')

# Generated URLs:
# GET /books/                   -> list all books
# POST /books/                  -> create new book
# GET /books/{id}/              -> retrieve single book
# PUT /books/{id}/              -> update book
# PATCH /books/{id}/            -> partial update
# DELETE /books/{id}/           -> delete book
# GET /books/{id}/summary/      -> custom action (if defined)
# GET /books/bestsellers/       -> custom list action (if defined)

urlpatterns = [
    path('api/', include(router.urls)),
]

# 2. SimpleRouter - No API root view
simple_router = SimpleRouter()
simple_router.register(r'books', BookViewSet)

# 3. Custom Router Configuration
from rest_framework.routers import DefaultRouter

class CustomRouter(DefaultRouter):
    """
    Custom router with additional functionality
    """
    routes = DefaultRouter.routes + [
        # Add custom routes here
    ]

custom_router = CustomRouter()
custom_router.register(r'books', BookViewSet)

# 4. Nested Routers (requires drf-nested-routers)
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')

# Nested route: /authors/{author_id}/books/
authors_router = routers.NestedDefaultRouter(router, r'authors', lookup='author')
authors_router.register(r'books', BookViewSet, basename='author-books')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(authors_router.urls)),
]

# 5. Router with Custom Actions
router = DefaultRouter()
router.register(r'books', BookViewSet)

# URLs generated for custom actions:
# If @action(detail=True): /books/{id}/action_name/
# If @action(detail=False): /books/action_name/

# 6. Multiple Routers
books_router = DefaultRouter()
books_router.register(r'books', BookViewSet)

users_router = DefaultRouter()
users_router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/library/', include(books_router.urls)),
    path('api/accounts/', include(users_router.urls)),
]

# 7. Router Configuration Options
router = DefaultRouter(
    trailing_slash=True,    # URLs end with / (default)
)

router_no_slash = DefaultRouter(
    trailing_slash=False    # URLs without trailing slash
)
