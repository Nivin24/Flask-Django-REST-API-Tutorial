# serializers_demo.py - Django REST Framework Serializers Examples

"""
This file demonstrates different types of serializers in Django REST Framework:
- Basic Serializer
- ModelSerializer  
- Nested Serializer
- Custom Validation
"""

from rest_framework import serializers
from django.contrib.auth.models import User


# ==================== Example 1: Basic Serializer ====================
class UserBasicSerializer(serializers.Serializer):
    """Basic serializer with manually defined fields"""
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    
    def create(self, validated_data):
        """Create and return a new User instance"""
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Update and return an existing User instance"""
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


# ==================== Example 2: ModelSerializer ====================
class UserModelSerializer(serializers.ModelSerializer):
    """ModelSerializer automatically creates fields based on the model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


# ==================== Example 3: Serializer with Validation ====================
class UserSerializerWithValidation(serializers.ModelSerializer):
    """Serializer with custom field and object-level validation"""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm']
        read_only_fields = ['id']
    
    def validate_username(self, value):
        """Field-level validation for username"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        if len(value) < 4:
            raise serializers.ValidationError("Username must be at least 4 characters")
        return value
    
    def validate_email(self, value):
        """Field-level validation for email"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value
    
    def validate(self, data):
        """Object-level validation"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        """Create user with hashed password"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


# ==================== Example 4: Nested Serializer ====================
class ProfileSerializer(serializers.Serializer):
    """Example profile serializer for nested data"""
    bio = serializers.CharField()
    website = serializers.URLField(required=False)


class UserWithProfileSerializer(serializers.ModelSerializer):
    """Serializer with nested profile data"""
    profile = ProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']


# ==================== Example 5: SerializerMethodField ====================
class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer with computed fields"""
    full_name = serializers.SerializerMethodField()
    is_premium = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'is_premium']
    
    def get_full_name(self, obj):
        """Returns the full name of the user"""
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def get_is_premium(self, obj):
        """Custom logic to check if user is premium"""
        # This is just an example - implement your own logic
        return obj.groups.filter(name='Premium').exists()


# ==================== Usage Example ====================
"""
# In your views or shell:

# Serialization (Model -> JSON)
user = User.objects.get(id=1)
serializer = UserModelSerializer(user)
data = serializer.data
# {'id': 1, 'username': 'john', 'email': 'john@example.com', ...}

# Deserialization (JSON -> Model)
data = {'username': 'jane', 'email': 'jane@example.com'}
serializer = UserModelSerializer(data=data)
if serializer.is_valid():
    user = serializer.save()
else:
    print(serializer.errors)
    
# Updating
user = User.objects.get(id=1)
serializer = UserModelSerializer(user, data={'email': 'newemail@example.com'}, partial=True)
if serializer.is_valid():
    serializer.save()
"""
