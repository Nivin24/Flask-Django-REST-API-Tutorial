# Filtering and Searching Example - Advanced Django REST Framework

from rest_framework import filters, viewsets
from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# 1. Basic Filtering with DjangoFilterBackend

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'author', 'published_year']
    
    # Usage:
    # GET /books/?category=fiction
    # GET /books/?author=5
    # GET /books/?published_year=2023

# 2. Custom FilterSet Class

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    published_after = django_filters.DateFilter(field_name='published_date', lookup_expr='gte')
    published_before = django_filters.DateFilter(field_name='published_date', lookup_expr='lte')
    
    class Meta:
        model = Book
        fields = ['title', 'category', 'author']

class BookFilterViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    
    # Usage:
    # GET /books/?title=django
    # GET /books/?min_price=10&max_price=50
    # GET /books/?published_after=2020-01-01

# 3. SearchFilter - Full-text search

class BookSearchViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'author__name']
    
    # Usage:
    # GET /books/?search=python
    # Searches in title, description, and author name

# 4. OrderingFilter - Sort results

class BookOrderingViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title', 'price', 'published_date', 'rating']
    ordering = ['title']  # Default ordering
    
    # Usage:
    # GET /books/?ordering=price
    # GET /books/?ordering=-price (descending)
    # GET /books/?ordering=price,title (multiple fields)

# 5. Combined Filtering, Searching, and Ordering

class CompleteBookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'price', 'published_date']
    ordering = ['-published_date']
    
    # Usage:
    # GET /books/?category=fiction&search=python&ordering=-price

# 6. Custom get_queryset() for Advanced Filtering

class CustomFilterViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        queryset = Book.objects.all()
        
        # Filter by query parameters
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by user
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(owner__username=user)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(published_date__gte=start_date)
        
        return queryset

# 7. Boolean Filtering

class BooleanFilterViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_published', 'is_featured', 'is_bestseller']
    
    # Usage:
    # GET /books/?is_published=true
    # GET /books/?is_featured=false

# 8. Multiple Choice Filtering

class MultipleChoiceFilter(django_filters.FilterSet):
    category = django_filters.MultipleChoiceFilter(
        choices=Book.CATEGORY_CHOICES,
        conjoined=False  # OR logic (default)
    )
    
    class Meta:
        model = Book
        fields = ['category']

# 9. Custom Filter Method

class CustomMethodFilter(django_filters.FilterSet):
    popular = django_filters.BooleanFilter(method='filter_popular')
    
    def filter_popular(self, queryset, name, value):
        if value:
            return queryset.filter(rating__gte=4.0, sales__gte=1000)
        return queryset
    
    class Meta:
        model = Book
        fields = ['popular']
