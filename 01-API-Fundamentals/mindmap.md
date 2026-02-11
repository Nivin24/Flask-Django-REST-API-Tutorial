# API Fundamentals - Mind Map

## 🎯 Core Concepts

### API (Application Programming Interface)
- Definition: Set of rules for software communication
- Purpose: Enable data exchange between applications
- Types:
  - Web APIs
  - Library APIs
  - Operating System APIs
  - Database APIs

### REST (Representational State Transfer)
- Architectural style for web services
- Uses HTTP protocol
- Resource-based approach
- Stateless communication

## 📋 REST Principles

### 1. Client-Server Architecture
- Separation of concerns
- Independent evolution
- Client: UI/UX
- Server: Data storage & business logic

### 2. Statelessness
- No client context stored on server
- Each request is independent
- Contains all necessary information
- Benefits:
  - Scalability
  - Reliability
  - Visibility

### 3. Cacheability
- Responses define cache behavior
- Improves performance
- Reduces server load
- Types:
  - Client-side caching
  - Server-side caching
  - CDN caching

### 4. Uniform Interface
- Resource identification (URIs)
- Resource manipulation via representations
- Self-descriptive messages
- HATEOAS

### 5. Layered System
- Hierarchical layers
- Each layer has specific responsibility
- Client unaware of intermediaries
- Benefits:
  - Security
  - Load balancing
  - Caching

### 6. Code on Demand (Optional)
- Server can extend client functionality
- Transfer executable code
- Example: JavaScript, applets

## 🔧 HTTP Methods

### GET
- Retrieve resources
- Read-only operation
- Safe & Idempotent
- Cacheable
- Example: `/api/users/123`

### POST
- Create new resources
- Not idempotent
- Not safe
- May return 201 Created
- Example: `/api/users`

### PUT
- Update entire resource
- Idempotent
- Requires full representation
- Example: `/api/users/123`

### PATCH
- Partial update
- Idempotent (typically)
- Only modified fields
- Example: `/api/users/123`

### DELETE
- Remove resources
- Idempotent
- Returns 204 No Content or 200 OK
- Example: `/api/users/123`

### OPTIONS
- Discover allowed methods
- CORS preflight
- Returns allowed methods in headers

### HEAD
- Like GET but no body
- Retrieve metadata only
- Check resource existence

## 📊 HTTP Status Codes

### 1xx - Informational
- 100 Continue
- 101 Switching Protocols
- 102 Processing

### 2xx - Success
- 200 OK: Request succeeded
- 201 Created: Resource created
- 202 Accepted: Request accepted for processing
- 204 No Content: Success but no content to return

### 3xx - Redirection
- 301 Moved Permanently
- 302 Found (Temporary redirect)
- 304 Not Modified (Cached)

### 4xx - Client Errors
- 400 Bad Request: Invalid syntax
- 401 Unauthorized: Authentication required
- 403 Forbidden: No permission
- 404 Not Found: Resource doesn't exist
- 405 Method Not Allowed
- 409 Conflict: Resource conflict
- 422 Unprocessable Entity: Validation error
- 429 Too Many Requests: Rate limit exceeded

### 5xx - Server Errors
- 500 Internal Server Error
- 502 Bad Gateway
- 503 Service Unavailable
- 504 Gateway Timeout

## 🔐 Key Concepts

### Idempotency
- Same result on multiple identical requests
- Idempotent: GET, PUT, DELETE, HEAD, OPTIONS
- Not idempotent: POST, PATCH (sometimes)

### Safety
- Operation doesn't modify resources
- Safe methods: GET, HEAD, OPTIONS
- Unsafe methods: POST, PUT, PATCH, DELETE

### Resource Identification
- URI (Uniform Resource Identifier)
- Resource naming conventions
- Hierarchical structure
- Query parameters for filtering

### Representations
- JSON (most common)
- XML
- HTML
- Plain text
- Binary formats

### Content Negotiation
- Client specifies preferred format
- Accept header: application/json
- Content-Type header
- Server responds with appropriate format

## 🌐 API Design Patterns

### RESTful URL Patterns
```
GET    /api/users          - List all users
GET    /api/users/123      - Get specific user
POST   /api/users          - Create user
PUT    /api/users/123      - Update user
PATCH  /api/users/123      - Partial update
DELETE /api/users/123      - Delete user
```

### Filtering & Pagination
- Query parameters
- `/api/users?role=admin&page=2&limit=10`
- Offset-based pagination
- Cursor-based pagination

### Versioning Strategies
- URL versioning: `/api/v1/users`
- Header versioning: `Accept: application/vnd.api.v1+json`
- Query parameter: `/api/users?version=1`

### Error Response Format
```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with ID 123 not found",
    "status": 404,
    "timestamp": "2026-02-11T20:00:00Z"
  }
}
```

## 🔗 Advanced Topics

### HATEOAS
- Hypermedia As The Engine Of Application State
- Include links in responses
- Dynamic API navigation
- Self-documenting

### Rate Limiting
- Prevent API abuse
- Headers:
  - X-RateLimit-Limit
  - X-RateLimit-Remaining
  - X-RateLimit-Reset

### CORS (Cross-Origin Resource Sharing)
- Browser security feature
- Allow cross-domain requests
- Preflight requests (OPTIONS)
- Headers:
  - Access-Control-Allow-Origin
  - Access-Control-Allow-Methods
  - Access-Control-Allow-Headers

### Authentication vs Authorization
- Authentication: Who are you?
- Authorization: What can you do?
- Methods:
  - API Keys
  - OAuth 2.0
  - JWT (JSON Web Tokens)
  - Basic Auth

## 📚 Best Practices

### Naming Conventions
- Use nouns for resources
- Plural for collections: `/users`
- Singular for single: `/user/123` or `/users/123`
- Lowercase URLs
- Hyphen for readability: `/user-profiles`

### Response Structure
- Consistent format
- Include metadata
- Proper error messages
- Use appropriate status codes

### Documentation
- Clear API documentation
- Examples for each endpoint
- Tools: Swagger/OpenAPI, Postman
- Keep documentation updated

### Security
- Use HTTPS
- Validate input
- Implement rate limiting
- Use authentication/authorization
- Never expose sensitive data in URLs
