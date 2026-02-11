# API Fundamentals - Theory

## 1. What is an API?

### Definition
An **Application Programming Interface (API)** is a set of rules, protocols, and tools that allows different software applications to communicate with each other. It acts as an intermediary layer that enables one system to request data or services from another system.

### Purpose
- **Enable Integration**: Connect different software systems
- **Data Exchange**: Share data between applications
- **Functionality Extension**: Allow third-party developers to build on existing platforms
- **Abstraction**: Hide complex implementation details

### Types of APIs
1. **Web APIs** (REST, SOAP, GraphQL)
2. **Library/Framework APIs** (Python standard library, React)
3. **Operating System APIs** (Windows API, POSIX)
4. **Database APIs** (JDBC, ODBC)

### Real-World Examples
- **Weather App**: Uses weather service API to fetch forecast data
- **Social Media Login**: Uses OAuth APIs (Google, Facebook) for authentication
- **Payment Processing**: Uses Stripe/PayPal APIs for transactions
- **Maps Integration**: Uses Google Maps API for location services

---

## 2. REST (Representational State Transfer)

### What is REST?
REST is an **architectural style** for designing networked applications. It was introduced by Roy Fielding in 2000 and has become the dominant approach for building web APIs.

### Key Characteristics
- Uses standard HTTP protocol
- Resource-based (everything is a resource)
- Stateless communication
- Client-server architecture
- Cacheable responses

### REST Principles

#### 1. Client-Server Architecture
- **Separation of Concerns**: Client handles UI, server handles data
- **Independent Evolution**: Client and server can evolve separately
- **Scalability**: Servers can scale independently

#### 2. Statelessness
- Each request contains all necessary information
- Server doesn't store client context between requests
- **Benefits**: Scalability, reliability, simplified server design
- **Trade-off**: Larger requests, repeated data transmission

#### 3. Cacheability
- Responses must explicitly indicate if they're cacheable
- **Benefits**: Reduces server load, improves performance
- **Implementation**: Using HTTP cache headers (Cache-Control, ETag)

#### 4. Uniform Interface
- **Resource Identification**: URIs uniquely identify resources
- **Resource Manipulation**: Use standard HTTP methods
- **Self-Descriptive Messages**: Include metadata
- **HATEOAS**: Hypermedia links in responses

#### 5. Layered System
- Client can't tell if connected directly to end server
- **Intermediaries**: Load balancers, proxies, gateways
- **Benefits**: Security, load balancing, caching

#### 6. Code on Demand (Optional)
- Server can send executable code to client
- **Examples**: JavaScript, Java applets
- **Rarely Used**: Due to security concerns

---

## 3. HTTP Methods

### GET - Retrieve Resources
- **Purpose**: Fetch data from server
- **Characteristics**: Safe, idempotent, cacheable
- **Example**: `GET /api/users/123`
- **Response Codes**: 200 OK, 404 Not Found

```http
GET /api/users/123 HTTP/1.1
Host: example.com
Accept: application/json
```

### POST - Create Resources
- **Purpose**: Create new resources
- **Characteristics**: Not safe, not idempotent
- **Example**: `POST /api/users`
- **Response Codes**: 201 Created, 400 Bad Request

```http
POST /api/users HTTP/1.1
Host: example.com
Content-Type: application/json

{"name": "John Doe", "email": "john@example.com"}
```

### PUT - Update/Replace Resources
- **Purpose**: Update entire resource or create if doesn't exist
- **Characteristics**: Idempotent
- **Example**: `PUT /api/users/123`
- **Response Codes**: 200 OK, 201 Created, 204 No Content

```http
PUT /api/users/123 HTTP/1.1
Host: example.com
Content-Type: application/json

{"id": 123, "name": "John Doe", "email": "john@example.com", "role": "admin"}
```

### PATCH - Partial Update
- **Purpose**: Update specific fields
- **Characteristics**: Typically idempotent
- **Example**: `PATCH /api/users/123`
- **Response Codes**: 200 OK, 204 No Content

```http
PATCH /api/users/123 HTTP/1.1
Host: example.com
Content-Type: application/json

{"email": "newemail@example.com"}
```

### DELETE - Remove Resources
- **Purpose**: Delete resources
- **Characteristics**: Idempotent
- **Example**: `DELETE /api/users/123`
- **Response Codes**: 200 OK, 204 No Content, 404 Not Found

```http
DELETE /api/users/123 HTTP/1.1
Host: example.com
```

### HEAD - Retrieve Headers Only
- **Purpose**: Get metadata without body
- **Use Cases**: Check if resource exists, get content length
- **Example**: `HEAD /api/users/123`

### OPTIONS - Discover Allowed Methods
- **Purpose**: Find which HTTP methods are supported
- **Use Cases**: CORS preflight requests
- **Response**: Returns Allow header

---

## 4. HTTP Status Codes

### 1xx - Informational
- **100 Continue**: Server received request headers, client should send body
- **101 Switching Protocols**: Server switching to protocol requested by client
- **102 Processing**: Server processing request but no response yet

### 2xx - Success
- **200 OK**: Request succeeded
- **201 Created**: Resource created successfully
- **202 Accepted**: Request accepted for processing
- **204 No Content**: Success but no content to return
- **206 Partial Content**: Partial GET request successful

### 3xx - Redirection
- **301 Moved Permanently**: Resource permanently moved
- **302 Found**: Temporary redirect
- **304 Not Modified**: Cached version is still valid
- **307 Temporary Redirect**: Same as 302 but method must not change
- **308 Permanent Redirect**: Same as 301 but method must not change

### 4xx - Client Errors
- **400 Bad Request**: Invalid syntax or validation failed
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Authenticated but not authorized
- **404 Not Found**: Resource doesn't exist
- **405 Method Not Allowed**: HTTP method not supported
- **409 Conflict**: Request conflicts with current state
- **422 Unprocessable Entity**: Validation error
- **429 Too Many Requests**: Rate limit exceeded

### 5xx - Server Errors
- **500 Internal Server Error**: Generic server error
- **501 Not Implemented**: Server doesn't support functionality
- **502 Bad Gateway**: Invalid response from upstream server
- **503 Service Unavailable**: Server temporarily unavailable
- **504 Gateway Timeout**: Upstream server timeout

---

## 5. Key Concepts

### Idempotency
**Definition**: An operation that produces the same result no matter how many times it's executed.

- **Idempotent Methods**: GET, PUT, DELETE, HEAD, OPTIONS
- **Non-Idempotent**: POST, PATCH (sometimes)

**Example**:
```
DELETE /api/users/123 - First call: deletes user, returns 200
DELETE /api/users/123 - Second call: user already deleted, returns 404
Result is the same: user doesn't exist
```

### Safety
**Definition**: An operation that doesn't modify resources.

- **Safe Methods**: GET, HEAD, OPTIONS
- **Unsafe Methods**: POST, PUT, PATCH, DELETE

### Resource Naming Conventions
- Use **nouns**, not verbs: `/users` not `/getUsers`
- Use **plural** for collections: `/users`
- Use **hierarchical** structure: `/users/123/orders/456`
- Use **lowercase** with hyphens: `/user-profiles`
- Avoid **file extensions**: `/users` not `/users.json`

### Query Parameters vs Path Parameters

**Path Parameters**: Identify specific resource
```
GET /api/users/123
```

**Query Parameters**: Filter, sort, paginate
```
GET /api/users?role=admin&page=2&limit=10
```

---

## 6. Content Negotiation

### Accept Header
Client specifies preferred response format:
```http
Accept: application/json
Accept: application/xml
Accept: text/html
```

### Content-Type Header
Indicates format of request body:
```http
Content-Type: application/json
Content-Type: application/x-www-form-urlencoded
Content-Type: multipart/form-data
```

### Common Media Types
- `application/json` - JSON data
- `application/xml` - XML data
- `text/html` - HTML content
- `text/plain` - Plain text
- `application/pdf` - PDF files
- `image/jpeg` - JPEG images

---

## 7. API Versioning

### Why Version APIs?
- Maintain backward compatibility
- Allow gradual migration
- Support multiple clients

### Versioning Strategies

#### URL Versioning
```
/api/v1/users
/api/v2/users
```
**Pros**: Clear, easy to implement
**Cons**: Pollutes URI space

#### Header Versioning
```http
Accept: application/vnd.example.v1+json
API-Version: 1
```
**Pros**: Clean URLs
**Cons**: Less visible, harder to test

#### Query Parameter
```
/api/users?version=1
```
**Pros**: Easy to implement
**Cons**: Can be overlooked

---

## 8. HATEOAS (Hypermedia)

### Concept
Hypermedia As The Engine Of Application State - API responses include links to related resources.

### Example Response
```json
{
  "id": 123,
  "name": "John Doe",
  "_links": {
    "self": {
      "href": "/api/users/123"
    },
    "orders": {
      "href": "/api/users/123/orders"
    },
    "edit": {
      "href": "/api/users/123",
      "method": "PUT"
    }
  }
}
```

### Benefits
- Self-documenting API
- Dynamic navigation
- Loose coupling
- Easier API evolution

---

## 9. Best Practices

### 1. Use Proper HTTP Methods
- GET for reading
- POST for creating
- PUT/PATCH for updating
- DELETE for removing

### 2. Return Appropriate Status Codes
- 2xx for success
- 4xx for client errors
- 5xx for server errors

### 3. Consistent Error Format
```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with ID 123 not found",
    "status": 404,
    "timestamp": "2026-02-11T20:00:00Z",
    "path": "/api/users/123"
  }
}
```

### 4. Implement Pagination
```
GET /api/users?page=2&limit=20
```

### 5. Support Filtering and Sorting
```
GET /api/users?role=admin&sort=created_at:desc
```

### 6. Use HTTPS
- Encrypt data in transit
- Protect sensitive information
- Required for authentication

### 7. Implement Rate Limiting
- Prevent API abuse
- Return 429 when limit exceeded
- Include rate limit headers

### 8. Document Your API
- Use OpenAPI/Swagger
- Provide examples
- Keep documentation updated

### 9. Version Your API
- Plan for changes
- Deprecate old versions gracefully
- Communicate changes clearly

### 10. Monitor and Log
- Track API usage
- Monitor performance
- Log errors for debugging

