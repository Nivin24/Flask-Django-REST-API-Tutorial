# ViewSets Example - Advanced Django REST Framework

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# 1. ModelViewSet - Full CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet provides:
    - list() - GET /books/
    - create() - POST /books/
    - retrieve() - GET /books/{id}/
    - update() - PUT /books/{id}/
    - partial_update() - PATCH /books/{id}/
    - destroy() - DELETE /books/{id}/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Custom action - GET /books/{id}/summary/
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        book = self.get_object()
        return Response({
            'title': book.title,
            'author': book.author.name,
            'pages': book.pages
        })
    
    # Custom list action - GET /books/bestsellers/
    @action(detail=False, methods=['get'])
    def bestsellers(self, request):
        bestsellers = Book.objects.filter(sales__gte=10000)
        serializer = self.get_serializer(bestsellers, many=True)
        return Response(serializer.data)

# 2. ReadOnlyModelViewSet - Read-only operations
class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnlyModelViewSet provides only:
    - list() - GET /authors/
    - retrieve() - GET /authors/{id}/
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    @action(detail=True)
    def books(self, request, pk=None):
        author = self.get_object()
        books = Book.objects.filter(author=author)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

# 3. Generic ViewSet - Custom actions only
class BookStatisticsViewSet(viewsets.ViewSet):
    """
    ViewSet allows you to define only the actions you need
    """
    
    def list(self, request):
        stats = {
            'total_books': Book.objects.count(),
            'total_authors': Author.objects.count(),
            'avg_pages': Book.objects.aggregate(Avg('pages'))['pages__avg']
        }
        return Response(stats)
    
    def retrieve(self, request, pk=None):
        book = Book.objects.get(pk=pk)
        stats = {
            'title': book.title,
            'views': book.view_count,
            'rating': book.average_rating
        }
        return Response(stats)
