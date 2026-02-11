# Practical: Django REST Framework Setup Guide

This guide covers setting up a new Django project with DRF.

## 1. Installation
First, install Django and djangorestframework:
```bash
pip install django djangorestframework
```

## 2. Create a Django Project
```bash
django-admin startproject myproject
cd myproject
python manage.py startapp api
```

## 3. Register DRF in settings.py
Add `'rest_framework'` and your new app to `INSTALLED_APPS` in `myproject/settings.py`:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'api',
]
```

## 4. Configure DRF Settings (Optional but Recommended)
Add a `REST_FRAMEWORK` dictionary to `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}
```

## 5. Basic URL Configuration
In `myproject/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), # Browser login/logout
]
```

## 6. Next Steps
- Create your models.
- Define serializers.
- Write views (APIView or ViewSets).
- Register routes.
